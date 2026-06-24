"""三大业务线 SubGraph 节点 — Sprint 2 step 3:接 estimate_*_quote 工具 + L2 导购包装。

节点内部流程(per business_line):
1. extract_slots(L0) → 抽 is_quote_intent / area_sqm / business_type
2. 若 is_quote_intent 且 area_sqm 齐 → 调 estimate_*_quote → 把格式化报价作为"必须原样引用"
   的 quote_block 注入 L2 system context;L2 只负责前后包装开场白/导购话术
3. 否则走引导分支:把已抽到的部分槽位告知 L2,避免重复追问

WHY 单次 L2 调用而非"L2 开场 + 工具结果 + L2 收尾"两阶段:
- 两阶段会让 SSE 体验出现"卡顿—数据—卡顿"的拼接感,且 L2 调用成本翻倍
- 单次调用 + Guardrail(step 4)校验 quote_block 是否原文出现,合规风险由后置兜底而非前置 prompt

WHY 把 format_quote_for_chat 整段(含 DISCLAIMER)塞进 quote_block 而非分字段:
- DESIGN §7.3 第 8 条要求免责声明"原文不可改写";最稳的方式是把整个合规模板作为不可分割单元
- 让 L2 在 quote_block 外做导购话术,数字与免责由代码控,符合"LLM 做创作、规则做合规"的边界

WHY stream_writer 而非 node return + 后置 SSE:
- LangGraph node 是 sync semantics(return state diff),没法在 return 之前流式推 token
- stream_writer 是 langgraph 0.2.30+ escape hatch:节点内任意时刻 writer(payload),
  外层 `graph.astream(..., stream_mode="custom")` 实时拿到 — token-level streaming 与
  state-level orchestration 的官方解耦方式
"""
from __future__ import annotations

import logging
from typing import Any, Callable, Coroutine

from langgraph.config import get_stream_writer

from app.graphs.slots import extract_slots
from app.graphs.state import BusinessLine, ChatState
from app.guardrails.quote_sanity import validate as guardrail_validate
from app.infra.llm_client import get_llm_client
from app.tools.quote import (
    QuoteResult,
    estimate_office_quote,
    estimate_residential_quote,
    estimate_storefront_quote,
    format_quote_for_chat,
)
from app.tools.rag import (
    QuoteExample,
    format_examples_for_prompt,
    retrieve_quote_examples,
)

# WHY 追加而非覆盖:用户已看到流式 token,直接覆盖会让前面消失造成困惑;
#     追加"权威版本"保留过程感的同时提供 fallback,合规问题不暴露给用户
GUARDRAIL_CORRECTION_PREFIX = "\n\n———\n[系统校准] 经合规审查,以下为权威报价:\n\n"

log = logging.getLogger("graphs.subgraphs")


def _merge_slots(prev: dict[str, Any] | None, new: dict[str, Any] | None) -> dict[str, Any]:
    """跨轮槽位 monotonic 合并 — Sprint 2 step 6 multi-turn 核心。

    规则:
    - 已知字段保留(prev 是 truthy 时不被本轮"抽不到"覆盖)
    - 新值若 truthy 则覆盖(用户改主意:"200 平,啊不 250 平" 尊重 latest)
    - is_quote_intent 是 bool,True 锁定不被 False 覆盖(对话状态单调):
      用户问过价之后,后续闲聊话术也要保留报价分支机会

    WHY 没用简单 dict.update:
    - LLM 在第二轮抽取时只看本轮 user_msg("200 平米"),会得到 area_sqm=200 但
      business_type=None;朴素 update 会把上轮抽到的"火锅店"抹成 None,违反用户预期
    - DESIGN §11.4 工程纪律:state 演化要 monotonic,丢失信息只能由用户显式覆盖
    """
    out: dict[str, Any] = dict(prev) if prev else {}
    for k, v in (new or {}).items():
        if k == "is_quote_intent":
            # bool 字段:True 锁定;之前没设过则取本轮值
            if v is True:
                out[k] = True
            elif k not in out:
                out[k] = bool(v)
        elif v not in (None, "", 0, 0.0, False, [], {}):
            out[k] = v
    return out


# WHY 字典分发而非 if/elif:三业务线对称,加一条仅需新增映射;后续若要 dry-run 替换报价函数
#     (如灰度新口径),也只需在此层 swap
QUOTE_FN: dict[BusinessLine, Callable[..., QuoteResult]] = {
    "storefront": estimate_storefront_quote,
    "office": estimate_office_quote,
    "residential": estimate_residential_quote,
}

BL_ZH: dict[BusinessLine, str] = {
    "storefront": "门面房/店铺装修(餐饮、零售、服务业)",
    "office": "办公空间装修(写字楼/商务楼/学校办公)",
    "residential": "住宅家装(自住房、新房、翻新、别墅)",
    "unknown": "装修(未明确业务线)",
}

# 引导分支的"必填槽位"清单(用于话术中告知用户缺什么)
REQUIRED_SLOTS: dict[BusinessLine, tuple[str, ...]] = {
    "storefront": ("业态细分(火锅/茶馆/快餐/零售)", "面积(㎡)", "档次(基础/中端/高端)"),
    "office": ("面积(㎡)", "工位数", "是否需要弱电改造", "档次"),
    "residential": ("面积(㎡)", "户型(几室几厅)", "档次(基础/中端/高端)"),
    "unknown": ("业务线", "面积(㎡)", "档次"),
}


def _build_quote_prompt(
    quote: QuoteResult,
    user_msg: str,
    business_line: BusinessLine,
    tier: str | None = None,
    examples: list[QuoteExample] | None = None,
) -> str:
    """报价分支 prompt — quote_block 必须被 L2 原样输出,前后允许导购包装。

    WHY 强约束"不编用户未提细节"(2026-06-23 用户反馈):
        之前 L2 会自由发挥说"您关注的吊顶/门头工艺我们都有丰富经验" — 但用户根本没提
        吊顶/门头。改 prompt 显式禁止编造未提及的工艺/材料/具体细节。
    """
    quote_text = format_quote_for_chat(quote, tier=tier)  # type: ignore[arg-type]
    bl_zh = BL_ZH.get(business_line, "装修")

    examples_block = ""
    if examples:
        examples_text = format_examples_for_prompt(examples)
        examples_block = (
            "\n【历史案例参考(仅作业内素材,严禁复述其中任何金额/具体规格/工艺细节)】\n"
            f"{examples_text}\n"
        )

    return (
        f"你是河南郑州美恺装饰公司的 AI 客服,核心业务是{bl_zh}。"
        f"系统已经基于历史数据为客户算好了下面这份参考报价,你的任务是用亲切、专业、像真人的口吻呈现给客户。\n\n"
        "【严格规则】\n"
        "1. <quote_block> 内部的文字必须一字不改原样输出(数字、档位、空间分项、免责声明都不可改)\n"
        "2. 可以在 <quote_block> 之前加 1 句开场白(15 字内,总结业态 + 面积 + 档次)\n"
        "3. 可以在 <quote_block> 之后加 1 句导购话术,引导用户:'若需更精准方案,可留下联系方式我们的设计师与您细聊'\n"
        "4. 全文不要使用 markdown 围栏,直接以普通文本输出\n"
        "5. ⚠️ **严禁编造用户未提及的细节**:不要说'您关注的XX工艺/材料/品牌',因为用户从未提过具体工艺细节\n"
        "6. ⚠️ **严禁复述历史案例的任何具体内容**(金额、规格、品牌、面积、工期),案例仅供你心里参考\n"
        "7. 导购话术 ≤ 1 句(原本可以 1-2 句,缩到 1 句让回复更精炼)\n"
        "8. 全文最多 1 个 emoji(开场白前或导购末尾),严禁堆砌;<quote_block> 内部不许加 emoji\n"
        f"{examples_block}\n"
        "<quote_block>\n"
        f"{quote_text}\n"
        "</quote_block>\n\n"
        f"用户消息:{user_msg}\n"
        "回复:"
    )


def _build_chat_prompt(
    user_msg: str,
    business_line: BusinessLine,
    slots: dict[str, Any],
    line_confident: bool = True,
) -> str:
    """引导分支 prompt — 按"业态 → 面积 → 档次"顺序追问,绝不假设。

    WHY 严格按优先级单字段追问(2026-06-23 用户反馈):
        之前 prompt 把所有缺失字段一次性问出来,L2 容易合并发问甚至自行假设业态
        (用户没说"餐饮",AI 直接说"餐饮店铺 120 平") → 用户大怒"我什么时候说餐饮了"。
        改成 missing 列表只塞**第一个**缺失项,L2 只能问那一个,得到后再下一个。
        档次也从 quote 阶段提到 chat 阶段:不收齐 tier 不出报价,避免一口气列三档。
    """
    bl_zh = BL_ZH.get(business_line, "装修")

    known_lines = []
    if slots.get("business_type"):
        known_lines.append(f"- 业态细分:{slots['business_type']}")
    if slots.get("area_sqm"):
        known_lines.append(f"- 面积:{slots['area_sqm']:g} ㎡")
    if slots.get("tier"):
        tier_zh = {"basic": "基础档", "mid": "中端档", "premium": "高端档"}.get(slots["tier"], slots["tier"])
        known_lines.append(f"- 档次:{tier_zh}")
    known_block = "\n".join(known_lines) if known_lines else "(暂无)"

    # 严格优先级 — 每次只追问一个缺失项,避免合并发问 + 防 L2 自行假设
    # Sprint A:business_line_confident=False 时(router 兜底,用户没明说),
    # 优先级 0:先问业务线;之后才是 业态 → 面积 → 档次
    next_question = ""
    if not line_confident:
        next_question = (
            "⚠️ 用户尚未告诉我们想装修哪类空间。请友好询问:\n"
            "'您是想了解哪类装修呢?我们主要做三块:\n"
            "  · 店铺装修(餐饮、零售、美容等门面)\n"
            "  · 商务办公(写字楼、企业办公)\n"
            "  · 精品家装(自住、新房、二手翻新)'\n"
            "⚠️ 绝不允许自己假设(例如不要直接说'您的店铺')"
        )
    elif business_line == "storefront" and not slots.get("business_type"):
        next_question = (
            "请追问业态:'请问您想装修的是什么类型的店铺?例如餐饮、零售、美容、教育培训等?'\n"
            "⚠️ 绝不允许自己假设业态(例如不要说'您的餐饮店')"
        )
    elif not slots.get("area_sqm"):
        next_question = "请追问店铺/房屋的面积(平方米)。"
    elif not slots.get("tier"):
        next_question = (
            "请追问档次:'您想看哪个档次的预算参考?\n"
            "- 基础档:满足基本功能,经济实惠\n"
            "- 中端档:兼顾品质与预算,大多数客户选择\n"
            "- 高端档:用料工艺升级,体验更佳'"
        )
    else:
        next_question = (
            "⚠️ 信息已齐!**只**说一句简短过渡话术(≤15 字),"
            "如'好的,这就为您整理报价~' 或 '稍等,这就出方案~'。"
            "**严禁追问任何其他问题**(包括设计感/耐用性/品牌偏好等),"
            "**严禁重复用户已说过的信息**。"
        )

    return (
        f"你是河南郑州美恺装饰公司的 AI 客服,本轮对话方向是{bl_zh}。\n"
        "用专业、温暖、口语化的中文回答,像真人在线服务,**只回复 1-2 句话**,不要长篇大论。\n\n"
        f"【已知信息】\n{known_block}\n\n"
        f"【本轮任务】{next_question}\n\n"
        "【严格规则】\n"
        "1. ⚠️ 已经出现在【已知信息】里的字段,**绝对禁止**再向用户问一遍\n"
        "2. ⚠️ 严禁假设/猜测用户未明确说过的内容(业态、品牌偏好、装修目的等都不许猜)\n"
        "3. 本轮只追问【本轮任务】里指定的字段,不要合并发问\n"
        "4. 不要凭空编造价格数字\n"
        "5. 如果用户在打招呼/咨询服务范围/闲聊,正常回应 1 句,再按【本轮任务】追问\n"
        "6. 全文最多 1 个 emoji(😊 👌 📐 🏠 ✨),严禁堆砌\n\n"
        f"用户消息:{user_msg}\n"
        "回复:"
    )


def _make_node(business_line: BusinessLine) -> Callable[[ChatState], Coroutine]:
    """工厂方法 — 用闭包绑定 business_line,生成 LangGraph 兼容的 async node。

    WHY 工厂模式而非三个独立 def:
    - 三业务线 95% 逻辑相同(只差 quote_fn 与 system 文案);独立 def 会让"加 token 计数"
      "接 langfuse trace" 这类共同改动散到三处
    - 后期某条业务线需要走独立流程(比如 storefront 接 RAG)时,把它从工厂里拆出来即可
    """

    async def node(state: ChatState) -> dict:
        writer = get_stream_writer()
        llm = get_llm_client()
        user_msg = state.get("user_msg", "")

        # 1. 槽位 + 意图抽取(双层:L0 LLM + 正则兜底,见 slots.py)
        # Sprint 2 step 6:把上一轮槽位 merge 进来 — checkpointer 已持久化 state.slots,
        # 本轮本地抽取与历史 monotonic 合并,用户不必重复说"火锅店"或"200 平米"
        new_slots = await extract_slots(user_msg, business_line)
        slots = _merge_slots(state.get("slots"), new_slots)

        # 2. 报价分支判定 — area_sqm 齐就走;business_type 缺失会走 by_line 兜底
        # WHY 去掉 is_quote_intent gate(2026-06-22):实测 Doubao Lite L0 在"装个 85 平沙拉店"
        #     这种长尾消息上常判 is_quote_intent=False(理解成"咨询"而非"求价"),再被
        #     _merge_slots 的"False 不被升级"语义卡死 → 后续即便用户说"中端吧""那预算多少"
        #     也永远卡在 chat 分支重复追问已知槽位。业务上"用户报了面积" 本身就是强报价信号,
        #     远比 LLM 判 intent 可靠;intent 字段仍保留用于其他启发(如 chat 分支语气)
        # WHY area + tier 都齐才出报价(2026-06-23 用户反馈):
        # 之前 area 齐就出,L2 被迫一口气列 basic/mid/premium 三档,用户感觉信息超载;
        # 现在 chat 分支会先追问 tier,收齐后才进 quote 分支,只出选中档
        # storefront 还要 business_type 齐(避免 AI 用'未确认业态'蒙猜)
        quote_payload: QuoteResult | None = None
        # 业务线未确认时绝不出报价(防止 unknown 兜底被路由到 storefront 误出店铺报价)
        line_confident = bool(state.get("business_line_confident", True))
        bt_ready = business_line != "storefront" or bool(slots.get("business_type"))
        if line_confident and slots.get("area_sqm") and slots.get("tier") and bt_ready:
            try:
                quote_payload = QUOTE_FN[business_line](
                    area_sqm=float(slots["area_sqm"]),
                    business_type=slots.get("business_type"),
                )
            except Exception:
                # WHY 报价工具异常不应阻断对话:降级回引导分支让 L2 自然话术承接
                log.exception(
                    "estimate_%s_quote raised, fallback to chat path; slots=%s",
                    business_line, slots,
                )

        # 3. Sprint 2 step 5:报价分支取 top-k 历史案例作为 L2 导购话术素材
        # WHY 在 quote_payload 命中后再调 RAG:引导分支(缺槽位)还没到"展示报价"阶段,
        #     案例素材无处用;只有要给出报价时,案例才有价值帮 L2 包装"有据可依"的导购话术
        # WHY 外层再 try 一次:rag.py 内部已 catch-all,但 SubGraph 是报价主路径,必须做
        #     防御性兜底(双层 try)— 后续有人误删 rag 内部 try 时,这里仍能让流不崩
        rag_examples: list[QuoteExample] = []
        if quote_payload is not None:
            try:
                rag_examples = await retrieve_quote_examples(
                    user_msg=user_msg,
                    business_line=business_line,
                    business_type=slots.get("business_type"),
                )
            except Exception:
                log.exception(
                    "retrieve_quote_examples raised unexpectedly,跳过 RAG 注入 (%s)",
                    business_line,
                )

        if quote_payload is not None:
            prompt = _build_quote_prompt(
                quote_payload, user_msg, business_line,
                tier=slots.get("tier"),
                examples=rag_examples,
            )
            branch = "quote"
        else:
            prompt = _build_chat_prompt(user_msg, business_line, slots, line_confident=line_confident)
            branch = "chat"

        # 3. L2 流式 — token 通过 writer 推 SSE,聚合一份用于 Guardrail + final_text 快照
        text_buf = ""
        async for chunk in llm.stream(prompt, level="l2"):
            writer({"kind": "delta", "text": chunk})
            text_buf += chunk

        # 4. Guardrail 输出侧审查(DESIGN §5.7.7) — 流式已推完,违规时追加权威版本而非覆盖
        result = guardrail_validate(text_buf, quote_payload)
        final_text = text_buf
        if not result.ok:
            log.warning(
                "guardrail override branch=%s violations=%s tail=%r",
                branch, result.violations, text_buf[-80:],
            )
            if result.authoritative_text:
                correction = GUARDRAIL_CORRECTION_PREFIX + result.authoritative_text
                for ch in correction:
                    writer({"kind": "delta", "text": ch})
                final_text = text_buf + correction

        log.info(
            "subgraph[%s] branch=%s slots=%s rag=%d reply_len=%d guardrail_ok=%s",
            business_line, branch, slots, len(rag_examples), len(final_text), result.ok,
        )
        # WHY 把 slots + quote + rag_examples 落到 state:
        #     - Sprint 2 step 6 multi-turn checkpointer 时,上一轮抽到的槽位可作为下一轮的
        #       "已知信息"复用(用户不必重复说面积)
        #     - rag_examples 落 state 便于评测/日志回溯"L2 看到了哪些案例素材"
        return {
            "slots": slots,
            "final_text": final_text,
            "quote": quote_payload,
            "rag_examples": list(rag_examples),
        }

    node.__name__ = f"{business_line}_node"
    return node


storefront_node = _make_node("storefront")
office_node = _make_node("office")
residential_node = _make_node("residential")
