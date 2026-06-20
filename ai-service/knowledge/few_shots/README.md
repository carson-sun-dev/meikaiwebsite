# L4 Few-shot 池(DESIGN §5.5)

按业态分目录存放真实对话样本。Sprint 1 收集 30+ 条:每业态至少 10 条覆盖"询价 → 槽位 → 报价 → 留资引导"全流程。

## 文件命名规范

```
few_shots/{business_line}/YYYYMMDD-{seq}-{业态}-{档次}.md
例:few_shots/storefront/20260601-001-咖啡店-mid.md
     few_shots/residential/20260601-005-三居-premium.md
     few_shots/office/20260601-012-互联网-100人-mid.md
```

## 内容结构

```markdown
---
business_line: storefront
business_type: 咖啡店
tier: mid
area_sqm: 80
per_sqm_yuan: 1800
---

USER: 我想开一家咖啡店,80 平。
ASSISTANT: 咖啡店是美恺常做业态。有几个关键信息 ...
USER: ...
ASSISTANT: ...
```

## 自动化来源(DESIGN §11.2)

每周 cron 从 `ai_feedback.score = -1` 的会话导出 Markdown 草稿,人工 10 分钟改写为标准样本入此目录,触发 Qdrant 重建。
