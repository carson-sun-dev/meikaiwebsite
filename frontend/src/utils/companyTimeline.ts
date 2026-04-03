/** 美恺创立年份（全站「写活」文案以此为准） */
export const COMPANY_FOUNDED_YEAR = 2017

export function getCurrentYear(): number {
  return new Date().getFullYear()
}

/**
 * 自创立年至当前自然年，含首尾共历几个日历年（2017 年成立 → 2017 年为第 1 年）
 */
export function getYearsSinceFoundedInclusive(): number {
  return Math.max(1, getCurrentYear() - COMPANY_FOUNDED_YEAR + 1)
}

/** 首页/关于页「2017—今年」 */
export function formatFoundedToCurrentRange(sep: string = '—'): string {
  return `${COMPANY_FOUNDED_YEAR}${sep}${getCurrentYear()}`
}

/** 1–99 转中文数字，用于「X载」「X年之旅」 */
export function toChineseNumeral(n: number): string {
  const d = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九'] as const
  const pick = (i: number) => d[i] ?? ''
  if (!Number.isFinite(n) || n <= 0) return '一'
  if (n < 10) return pick(n) || '一'
  if (n === 10) return '十'
  if (n < 20) return '十' + (n % 10 ? pick(n % 10) : '')
  if (n < 100) {
    const t = Math.floor(n / 10)
    const o = n % 10
    return pick(t) + '十' + (o ? pick(o) : '')
  }
  return String(Math.floor(n))
}

/** 关于页标题：深耕中原X载 */
export function getZhYearsZaiPhrase(): string {
  return `${toChineseNumeral(getYearsSinceFoundedInclusive())}载`
}

/** 公司卡片标题：X年之旅 */
export function getJourneyCardTitle(): string {
  return `${toChineseNumeral(getYearsSinceFoundedInclusive())}年旅程`
}

/** 数据卡片：X年+ */
export function getMetricYearsPlus(): string {
  return `${getYearsSinceFoundedInclusive()}年+`
}
