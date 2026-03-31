export type HomePricingPlan = {
  title: string
  price: string
  lines: string[]
}

export const homePricingPlans: HomePricingPlan[] = [
  {
    title: '设计方案',
    price: '20￥/m²',
    lines: ['概念与平面方案', '主要空间效果图', '材料与色彩方向说明'],
  },
  {
    title: '全案设计',
    price: '80￥/m²',
    lines: ['全套施工图与节点', '软装清单与采购协助', '现场交底与巡检配合'],
  },
  {
    title: '整装套餐',
    price: '面议',
    lines: ['设计+施工+主材统筹', '工期与品质双控', '适合全托管需求客户'],
  },
]
