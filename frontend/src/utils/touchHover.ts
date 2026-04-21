const TOUCH_HOVER_CLASS = 'is-touch-hover'

const TOUCH_HOVER_SELECTORS = [
  '.company-intro-card',
  '.company-intro__link',
  '.about-metric',
  '.timeline-item__card',
  '.about-intro__btn',
  '.store-btn',
  '.store-highlight-card',
  '.store-price-card',
  '.business-btn',
  '.business-highlight-card',
  '.business-price-card',
  '.res-btn',
  '.res-highlight-card',
  '.res-price-card',
  '.home-price-card',
  '.home-price-card__btn',
  '.home-gallery__marquee-item',
  '.home-gallery__contact-link',
  '.home-business__accent',
] as const

const SELECTOR_QUERY = TOUCH_HOVER_SELECTORS.join(', ')

function supportsTouchHover(): boolean {
  if (typeof window === 'undefined' || typeof window.matchMedia !== 'function') return false
  return window.matchMedia('(hover: none), (pointer: coarse)').matches
}

function clearActive(activeEl: HTMLElement | null) {
  activeEl?.classList.remove(TOUCH_HOVER_CLASS)
}

export function setupTouchHover() {
  if (!supportsTouchHover() || typeof document === 'undefined') return

  let activeEl: HTMLElement | null = null

  document.addEventListener(
    'pointerdown',
    (event) => {
      const target = event.target instanceof Element ? event.target.closest<HTMLElement>(SELECTOR_QUERY) : null

      if (!target) {
        clearActive(activeEl)
        activeEl = null
        return
      }

      if (activeEl && activeEl !== target) {
        clearActive(activeEl)
      }

      target.classList.add(TOUCH_HOVER_CLASS)
      activeEl = target
    },
    { passive: true },
  )
}

