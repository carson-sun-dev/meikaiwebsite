export type HomePricingPlan = {
  title: string
  price: string
  lines: string[]
}

export const homePricingPlans: HomePricingPlan[] = [
  {
    title: '品牌店装',
    price: '1200￥/m²',
    lines: ['重点打造极具冲击力的品牌门头', 
      '保证解决消防报审与监控网线组网', 
      '强化水电的抗损性能，确保运营无忧。'],
  },
  {
    title: '商务·办公',
    price: '600￥/m²',
    lines: ['专业隔断平衡隐私与协作', '集成吊顶与工学灯具，创造低噪音环境', '确保水电、洁具等隐蔽工程高标准落地'],
  },
  {
    title: '精品家装',
    price: '700￥/m²',
    lines: ['总工程师全托管客户需求', '精选全球环保瓷砖、洁具与灯具。', '涵盖水电、吊顶等核心工项，拎包入住。' ],
  },
]
