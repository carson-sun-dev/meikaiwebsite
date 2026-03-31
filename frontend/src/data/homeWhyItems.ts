/** 首页「为什么选择我们」手风琴列表，可在此追加条目 */
export interface HomeWhyItem {
  name: string
  /** 右侧序号，如 01 */
  num: string
  /** 主题标题（不含序号） */
  title: string
  body: string
}

export const homeWhyItems: HomeWhyItem[] = [
  {
    name: '1',
    num: '01',
    title: '全链路设计落地',
    body: '从概念方案到施工图与现场配合，设计团队与项目经理协同，减少返工与沟通成本，保证效果可落地。',
  },
  {
    name: '2',
    num: '02',
    title: '透明报价与材料',
    body: '清单式报价与主材可选范围清晰标注，关键节点书面确认，让您对预算与选材心中有数。',
  },
  {
    name: '3',
    num: '03',
    title: '工艺与验收标准',
    body: '沿用行业与自有工艺标准，多阶段验收与影像记录，隐蔽工程可追溯。',
  },
  {
    name: '4',
    num: '04',
    title: '售后与维保',
    body: '竣工后提供维保建议与响应渠道，长期陪伴您的居住与使用体验。',
  },
]
