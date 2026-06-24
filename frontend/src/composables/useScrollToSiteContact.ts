/** footer「联系」列锚点 id，与 HomeFooter 保持一致 */
export const SITE_CONTACT_ID = 'site-contact'

/** fixed 导航栏高度 + 呼吸间距，避免锚点被顶栏遮住 */
const NAV_SCROLL_OFFSET = 88

export function scrollToSiteContact() {
  const el = document.getElementById(SITE_CONTACT_ID)
  if (!el) return

  const top = el.getBoundingClientRect().top + window.scrollY - NAV_SCROLL_OFFSET
  window.scrollTo({ top: Math.max(0, top), behavior: 'smooth' })
}
