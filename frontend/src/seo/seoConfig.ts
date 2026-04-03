/**
 * 全站 SEO：标题、描述、关键词（含业务词与品牌保护词的自然组合）
 * 生产环境请在 .env 配置 VITE_SITE_ORIGIN（无末尾 /），用于 canonical 与 Open Graph
 */
export const SITE_ORIGIN = (import.meta.env.VITE_SITE_ORIGIN as string | undefined)?.replace(/\/$/, '') ?? ''

export type PageSeo = {
  title: string
  description: string
  keywords: string
}

const BRAND =
  '美恺装饰官方网站,河南美恺装饰,美恺装饰联系方式,河南美恺装饰评价'

const STORE_KW =
  '郑州店装公司,河南精品店铺装修,网红店设计装修,餐饮店装修效果图,商铺门头设计施工,洛阳店铺装修,开封店铺装修'

const OFFICE_KW =
  '郑州办公室装修设计,写字楼装修公司,商务办公空间规划,郑州工装公司推荐'

const HOME_KW =
  '郑州家装全包价格,河南室内装修公司,三室两厅装修预算,简约风装修案例'

const REGION = '河南美恺装饰,郑州装修公司哪家好,全省服务'

const seoHome: PageSeo = {
  title: '河南美恺装饰官网｜郑州装修公司·店装·办公·家装',
  description:
    '河南美恺装饰官方网站，服务郑州及河南全省：精品店铺装修、写字楼办公设计、家装整装。涵盖郑州店装公司、网红店设计、办公室装修设计、家装全包价格与案例。可查询美恺装饰联系方式、河南美恺装饰评价与工程排期。',
  keywords: `${REGION},${STORE_KW},${OFFICE_KW},${HOME_KW},${BRAND}`,
}

const seoStore: PageSeo = {
  title: '品牌店装｜郑州店装·餐饮门头·网红店设计｜河南美恺装饰',
  description:
    '河南美恺装饰店装案例与施工：郑州店装公司、河南精品店铺装修、网红店设计装修、餐饮店装修效果图参考、商铺门头设计施工。洛阳、开封店铺装修与全省项目可咨询美恺装饰联系方式。',
  keywords: `${STORE_KW},${BRAND}`,
}

const seoBusiness: PageSeo = {
  title: '商务办公装修｜郑州办公室设计·写字楼装修｜河南美恺装饰',
  description:
    '郑州办公室装修设计、写字楼装修公司级交付标准，商务办公空间规划与工位动线优化。郑州工装公司推荐参考河南美恺装饰，获取办公报价与美恺装饰联系方式。',
  keywords: `${OFFICE_KW},${BRAND},${REGION}`,
}

const seoResidential: PageSeo = {
  title: '精品家装｜郑州家装全包·三室两厅预算·简约风案例｜美恺装饰',
  description:
    '郑州家装全包价格咨询、河南室内装修公司美恺装饰：三室两厅装修预算、简约风装修案例与实景。了解河南美恺装饰评价与售后，通过美恺装饰联系方式预约量房。',
  keywords: `${HOME_KW},${BRAND},${REGION}`,
}

const seoContact: PageSeo = {
  title: '联系美恺装饰｜获取报价·美恺装饰联系方式｜河南美恺装饰官网',
  description:
    '美恺装饰官方网站一键估价与电话提交：店装、办公、家装全品类。河南美恺装饰联系方式面向郑州及全省，欢迎咨询郑州装修公司哪家好与各类装修需求。',
  keywords: `${BRAND},${REGION},郑州店装公司,郑州办公室装修设计,郑州家装全包价格`,
}

const seoAbout: PageSeo = {
  title: '关于美恺装饰｜河南美恺装饰评价·企业历程｜官方网站',
  description:
    '了解河南美恺装饰发展历程、工程标准与口碑。河南美恺装饰评价、团队与案例尽在美恺装饰官方网站；预约沟通请使用页面内美恺装饰联系方式。',
  keywords: `河南美恺装饰评价,美恺装饰官方网站,河南美恺装饰,美恺装饰联系方式,${REGION}`,
}

const byRouteName: Record<string, PageSeo> = {
  home: seoHome,
  store: seoStore,
  business: seoBusiness,
  residential: seoResidential,
  contact: seoContact,
  about: seoAbout,
}

export function getSeoForRoute(routeName: string | symbol | null | undefined): PageSeo {
  const key = typeof routeName === 'string' ? routeName : ''
  return byRouteName[key] ?? seoHome
}

export function canonicalUrl(path: string): string | undefined {
  if (!SITE_ORIGIN) {
    return undefined
  }
  const p = path === '/' ? '/home' : path
  return `${SITE_ORIGIN}${p.startsWith('/') ? p : `/${p}`}`
}

/** Organization JSON-LD（部署后配置 VITE_SITE_ORIGIN 则写入 url） */
export function organizationJsonLd(): Record<string, unknown> {
  const base: Record<string, unknown> = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: '河南美恺装饰',
    alternateName: '美恺装饰',
    description: '河南美恺装饰官方网站，提供郑州及全省店装、商务办公、精品家装设计与施工服务。',
    address: {
      '@type': 'PostalAddress',
      addressLocality: '郑州',
      addressRegion: '河南',
      streetAddress: '河南省郑州市管城回族区南台路9号',
      addressCountry: 'CN',
    },
    telephone: '+86-13393736352',
  }
  if (SITE_ORIGIN) {
    base.url = SITE_ORIGIN
  }
  return base
}
