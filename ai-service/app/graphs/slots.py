"""槽位提取节点 — 从 user_msg 中抠 area_sqm / business_type + is_quote_intent。

DESIGN 锚点:
- §3 Sprint 2 step 3:SubGraph 报价前置 — 槽位齐了才调 estimate_*_quote
- §11.4 工程纪律:LLM 抽取必须有正则兜底,防止单点 JSON 失败让整轮报价坍塌

WHY L0 + 正则兜底双层而非纯 LLM:
- L0 抽 JSON 在中文长尾表达上(如"两百来平")更鲁棒,但偶尔输出带引号/解释/markdown 围栏
- 正则兜底确保即使 LLM 输出完全无法解析,关键字段(面积/常见业态)仍能落到 slots
- mock 模式下纯靠正则也能让端到端可演示(MockLLM 不会输出 JSON)

WHY business_type 主要服务 storefront:
- estimate_*_quote 的 by_type bucket 只对 storefront 细分(火锅店/饭店/茶馆/...)
- office/residential 走 by_line/industry_default,业态抽到也只用于导购话术(不参与报价分桶)
"""
from __future__ import annotations

import json
import logging
import re
from typing import Any, TypedDict

from app.graphs.state import BusinessLine
from app.infra.llm_client import get_llm_client

log = logging.getLogger("graphs.slots")


class Slots(TypedDict, total=False):
    is_quote_intent: bool
    area_sqm: float
    business_type: str
    tier: str  # 'basic' | 'mid' | 'premium' — 用户选的档次

    # Sprint A 扩展(2026-06-23):per-business-line 深化需求字段,
    # 收集到的让 quote prompt 注入 needs 段,L2 在导购话术里 acknowledge
    site_condition: str    # 'raw'(毛坯/新房) | 'renovation'(二手翻新) - 通用
    is_chain: bool         # 是否品牌连锁 - storefront 专属
    turnover_intensity: str  # 'low' | 'high' - 翻台强度 - storefront 专属
    team_size: int         # 团队规模 - office 专属
    image_focus: bool      # 是否注重前台/会客形象 - office 专属
    layout: str            # 户型 "3室2厅" - residential 专属
    household: str         # 居住人口/特殊群体 "1 老人 1 小孩" - residential 专属
    style_pref: str        # 风格倾向 "新中式/极简" - residential / storefront 通用

    # skip 信号:用户说"先出报价/不细说/算了" → chat 跳过追问直接 quote
    skip_to_quote: bool


SLOT_PROMPT = """从用户消息中提取装修咨询相关字段,严格输出 JSON,不要解释、不要 markdown 围栏。
**重要**:不在消息里出现的字段一律填 null,严禁猜测!

已知业务线:{bl_zh}

【关键字段】
- is_quote_intent: 用户是否在问价格/报价/预算/多少钱(boolean)
- area_sqm: 面积平方米(数字 或 null)。"80平"/"两百平米"/"90 个平方"转数字;"85"这种纯数字也算面积
- business_type: 业态细分(仅门面房有意义)。如:火锅店/饭店/茶馆/咖啡店/眼镜店/服装店/便利店/美容院
  ⚠️ 没明确说,一律 null,不要反推
- tier: 档次 'basic'(基础/经济/简装) | 'mid'(中端/标准/品质) | 'premium'(高端/旗舰/精装) | null

【深化字段(Sprint A,2026-06-23)】
- site_condition: 'raw'(新房/毛坯/新铺) | 'renovation'(二手/翻新/旧房) | null
- is_chain: 是否品牌连锁/多店 (boolean 或 null) — storefront 用
- turnover_intensity: 'high'(翻台快/排队/客流大) | 'low'(慢餐/精致/低翻台) | null — storefront 用
- team_size: 团队规模数字 — office 用,"30 人团队"→30
- image_focus: 是否注重前台/会客/品牌形象 (boolean 或 null) — office 用
- layout: 户型字符串 — residential 用,"三室两厅"/"3 室 2 厅"原样填
- household: 居住人口/特殊群体 — residential 用,"有老人小孩"/"两口之家"原样填
- style_pref: 风格倾向 — "新中式"/"极简北欧"/"工业风"原样填

【跳过信号】
- skip_to_quote: 用户表达"先看报价/直接出/算了不细说/不知道/差不多就行"等想跳过追问 (boolean)

示例:
- "200 平沙拉店,新铺" → {{"is_quote_intent": false, "area_sqm": 200, "business_type": "沙拉店", "site_condition": "raw"}}
- "85" → {{"is_quote_intent": false, "area_sqm": 85}}
- "中端" → {{"tier": "mid"}}
- "我们 30 人小团队,注重形象" → {{"team_size": 30, "image_focus": true}}
- "三室两厅,有老人和小孩,想要新中式" → {{"layout": "三室两厅", "household": "有老人和小孩", "style_pref": "新中式"}}
- "快出报价吧" → {{"skip_to_quote": true, "is_quote_intent": true}}
- "二手房翻新" → {{"site_condition": "renovation"}}
- "品牌连锁,翻台快" → {{"is_chain": true, "turnover_intensity": "high"}}

用户消息:{msg}
JSON:"""

BL_ZH: dict[BusinessLine, str] = {
    "storefront": "门面房/店铺",
    "office": "办公空间",
    "residential": "住宅家装",
    "unknown": "未确认",
}

# WHY 兜底正则:LLM 失败时确保"我家 80 平"这类消息仍能抽到面积
#     单位覆盖:平米/平方米/平方/平/㎡/m2/m²;允许 "80个平米"/"100 平" 这类口语
AREA_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:个)?\s*(?:平方米|平米|平方|平|㎡|m2|m²)")
# WHY 纯数字也当面积:用户在 AI 问完"面积多少"后常只回一个数字(截图证据 2026-06-22),
#     带单位识别已覆盖 95% 的初次表达,这条覆盖剩下 5% 的"对话中简答"场景。
#     边界:5-100000 ㎡,小于 5 是噪声(不是合理面积),大于 10万 是误识别(可能是预算/年份)
PURE_NUMBER_RE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*$")
QUOTE_KEYWORDS = ("报价", "多少钱", "价格", "预算", "费用", "造价", "估价", "多钱", "贵不贵", "便宜")
# WHY tier 正则兜底:用户对"档次"的口语表达,LLM 失败时仍能识别
TIER_KEYWORDS = {
    "basic":   ("基础", "经济", "最便宜", "简装", "便宜的", "入门"),
    "mid":     ("中端", "中档", "标准", "品质", "中等", "中间"),
    "premium": ("高端", "高档", "旗舰", "豪华", "顶级", "精装", "顶配", "最贵"),
}

# Sprint A 扩展正则兜底 — LLM 失败时关键深化字段仍能识别
SITE_RAW = ("毛坯", "新房", "新铺", "新店", "新场地", "新拿的", "刚拿到")
SITE_RENO = ("二手", "翻新", "旧房", "老房", "改造", "原有", "之前装修过")
CHAIN_YES = ("连锁", "品牌", "分店", "多店", "加盟", "总部")
TURNOVER_HIGH = ("翻台", "排队", "客流大", "高翻台", "快餐", "外卖", "高流量")
TURNOVER_LOW = ("精致", "慢餐", "私厨", "低翻台", "私享", "包间")
IMAGE_FOCUS_YES = ("注重形象", "重视形象", "前台", "会客", "品牌墙", "logo")
SKIP_TO_QUOTE = ("快出", "直接出", "直接报价", "先看报价", "不想细说", "算了", "差不多就行", "不知道")
STYLE_KEYWORDS = (
    "新中式", "中式", "极简", "北欧", "日式", "工业风", "现代", "轻奢",
    "美式", "欧式", "田园", "地中海", "复古", "宜家",
)
LAYOUT_RE = re.compile(r"([一二三四五六12345六]+)室([一二两12两]+)厅")
TEAM_SIZE_RE = re.compile(r"(\d+)\s*(?:个)?人(?:团队|的团队|公司)?")
# WHY 按"长在前"匹配:"火锅店" 必须先于 "店" 检测,防止 "我开火锅店" 抽成 business_type="店"
BUSINESS_TYPES = (
    "火锅店", "茶馆", "咖啡店", "奶茶店", "饮品店",
    "面馆", "烧烤店", "酒吧", "饭店", "餐厅",
    "眼镜店", "服装店", "便利店", "美容院", "理发店",
    "诊所", "工作室", "酒店", "民宿",
)


def _heuristic_extract(user_msg: str) -> dict[str, Any]:
    """正则兜底 — 不调任何模型,作为 LLM 失败的安全垫。"""
    out: dict[str, Any] = {"is_quote_intent": False}

    m = AREA_RE.search(user_msg)
    if m:
        try:
            out["area_sqm"] = float(m.group(1))
        except ValueError:
            pass
    else:
        # 带单位没命中 → 试纯数字(用户对话中简答场景)
        m_pure = PURE_NUMBER_RE.match(user_msg)
        if m_pure:
            try:
                val = float(m_pure.group(1))
                if 5 <= val <= 100000:
                    out["area_sqm"] = val
            except ValueError:
                pass

    for bt in BUSINESS_TYPES:
        if bt in user_msg:
            out["business_type"] = bt
            break

    # tier 兜底:按"长在前"匹配,避免"标准"被"高端"前缀干扰
    for tier_key, keywords in TIER_KEYWORDS.items():
        if any(kw in user_msg for kw in keywords):
            out["tier"] = tier_key
            break

    # Sprint A 扩展字段兜底
    if any(kw in user_msg for kw in SITE_RAW):
        out["site_condition"] = "raw"
    elif any(kw in user_msg for kw in SITE_RENO):
        out["site_condition"] = "renovation"

    if any(kw in user_msg for kw in CHAIN_YES):
        out["is_chain"] = True

    if any(kw in user_msg for kw in TURNOVER_HIGH):
        out["turnover_intensity"] = "high"
    elif any(kw in user_msg for kw in TURNOVER_LOW):
        out["turnover_intensity"] = "low"

    if any(kw in user_msg for kw in IMAGE_FOCUS_YES):
        out["image_focus"] = True

    m_team = TEAM_SIZE_RE.search(user_msg)
    if m_team:
        try:
            size = int(m_team.group(1))
            if 1 <= size <= 100000:
                out["team_size"] = size
        except ValueError:
            pass

    m_layout = LAYOUT_RE.search(user_msg)
    if m_layout:
        out["layout"] = m_layout.group(0)

    for style in STYLE_KEYWORDS:
        if style in user_msg:
            out["style_pref"] = style
            break

    if any(kw in user_msg for kw in SKIP_TO_QUOTE):
        out["skip_to_quote"] = True

    if any(kw in user_msg for kw in QUOTE_KEYWORDS):
        out["is_quote_intent"] = True
    # WHY 没命中关键词但有"面积+业态"也算报价意图
    elif "area_sqm" in out and "business_type" in out:
        out["is_quote_intent"] = True

    return out


def _parse_llm_json(raw: str) -> dict[str, Any] | None:
    """尽力抠 LLM 输出中的 JSON 对象 — 容忍 markdown 围栏、前后解释、单引号。"""
    s = raw.strip()
    # 剥 ```json ... ``` 围栏
    m = re.search(r"```(?:json)?\s*(\{.+?\})\s*```", s, re.DOTALL)
    if m:
        s = m.group(1)
    else:
        # 取最外层 { ... }
        start = s.find("{")
        end = s.rfind("}")
        if start < 0 or end <= start:
            return None
        s = s[start : end + 1]

    try:
        return json.loads(s)
    except json.JSONDecodeError:
        # 二次尝试:单引号 → 双引号
        try:
            return json.loads(s.replace("'", '"'))
        except json.JSONDecodeError:
            return None


def _merge(llm_slots: dict[str, Any] | None, heur_slots: dict[str, Any]) -> dict[str, Any]:
    """LLM 字段优先,正则字段兜底缺失项。"""
    out = dict(heur_slots)
    if not llm_slots:
        return out

    if isinstance(llm_slots.get("is_quote_intent"), bool):
        out["is_quote_intent"] = llm_slots["is_quote_intent"]

    area = llm_slots.get("area_sqm")
    if isinstance(area, (int, float)) and area > 0:
        out["area_sqm"] = float(area)

    bt = llm_slots.get("business_type")
    # WHY 显式过滤 "null"/"None" 字符串:L0 偶尔会照抄 schema 里的 null 当字符串输出
    if isinstance(bt, str) and bt.strip() and bt.strip().lower() not in ("null", "none", "未知", "无"):
        out["business_type"] = bt.strip()

    tier = llm_slots.get("tier")
    if isinstance(tier, str) and tier.strip().lower() in ("basic", "mid", "premium"):
        out["tier"] = tier.strip().lower()

    return out


async def extract_slots(user_msg: str, business_line: BusinessLine) -> dict[str, Any]:
    """双层抽取:L0 LLM 出 JSON + 正则兜底,合并后返回 slots dict。

    返回字段语义(契约,见 Slots TypedDict):
    - is_quote_intent: bool(必有,默认 False)
    - area_sqm: float(可缺;> 0 才落)
    - business_type: str(可缺;空串/'null' 等噪声值会被丢弃)
    """
    heur = _heuristic_extract(user_msg)

    llm = get_llm_client()
    bl_zh = BL_ZH.get(business_line, "未确认")
    prompt = SLOT_PROMPT.format(bl_zh=bl_zh, msg=user_msg)

    raw = ""
    try:
        async for chunk in llm.stream(prompt, level="l0"):
            raw += chunk
    except Exception as e:
        # WHY catch-all:LLM 网络/鉴权异常都不应阻断整轮对话,正则兜底保证 SubGraph 仍能走
        log.warning("slots LLM call failed,纯走正则兜底:%s", e)
        return heur

    parsed = _parse_llm_json(raw)
    if parsed is None:
        log.info("slots LLM JSON 解析失败,正则兜底:raw=%r", raw[:120])
    merged = _merge(parsed, heur)
    log.info("slots(user=%r,line=%s) → %s", user_msg[:40], business_line, merged)
    return merged
