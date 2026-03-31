export type HomePricingPlan = {
  title: string
  price: string
  lines: string[]
}

export const homePricingPlans: HomePricingPlan[] = [
  {
    title: '品牌店装',
    price: '1500￥/m²',
    lines: ['概念与平面方案', '主要空间效果图', '材料与色彩方向说明'],
  },
  {
    title: '商务·办公',
    price: '1200￥/m²',
    lines: ['全套施工图与节点', '软装清单与采购协助', '现场交底与巡检配合'],
  },
  {
    title: '精品家装',
    price: '1200￥/m²',
    lines: ['设计+施工+主材统筹', '工期与品质双控', '适合全托管需求客户'],
  },
]
