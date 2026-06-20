"""离线评测包 — Sprint 3 骨架(2026-06-16)。

DESIGN 锚点(§10.4):
- 评测集驱动:每次改 prompt/换模型/调 RAG 都跑一遍,防止 regression
- 当前阶段:10 条手写 case + Guardrail 硬规则评分,不接 LangFuse Dataset
- V2(下下轮):扩到 50 条 + LangFuse Dataset 集成 + LLM-as-judge

WHY 独立包 evals/ 而非塞进 tests/:
- 评测是"产品质量",pytest 是"代码正确性",语义不同(case 失败不等于代码 bug)
- evals 可独立演进(扩 case、换 judge、出报告),不污染 pytest 文件
- tests/test_evals_smoke.py 抽 2-3 条 case 在 pytest 跑,确保 runner 接口不腐烂

WHY mock 模式作主路径:
- 零 LLM token 消耗,CI / 本地秒过
- mock 下 Guardrail 必触发(L2 echo prompt 没原样输出 quote_block),所以 final_text
  在报价分支下必含完整三档报价 + 免责声明 — 这反而让评测断言更确定
- 真 LLM 路径(LLM_MODE=live)留给 V2 配合 LangFuse trace 跑
"""
