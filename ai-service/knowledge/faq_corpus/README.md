# L5 RAG 知识库语料(DESIGN §5.5)

行业术语 + 消防/物业常识 + 施工工艺常识,**Markdown 切块后入 Qdrant `knowledge_faq` collection**。

## 文件清单(Sprint 1 待补)

| 文件 | 主题 | 切块策略 |
|---|---|---|
| `terms.md` | 弱电 / 消电检 / VAV / 隔墙 / 防火等级 等术语解释 | 按 `## 词条` 切 |
| `regulations.md` | 消防、物业、商场常见硬性要求 | 按 `## 场景` 切 |
| `techniques.md` | 施工工艺常识:水电改造、防水、吊顶、瓦工 | 按 `## 工艺` 切 |

## 灌库命令

```bash
python -m etl.build_index --faq knowledge/faq_corpus/
```

(待 `etl/build_index.py` 在 Sprint 1 后期补 FAQ 入口)
