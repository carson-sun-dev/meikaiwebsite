<template>
  <div class="home-footer-shell">
    <!-- 单一深色 footer:全宽无圆角,内部依次:保持联系 → 4 列网格 → 备案 -->
    <footer class="home-footer">
      <div class="home-footer__inner">
        <!-- 顶部:保持联系(原独立 section,移入 footer) -->
        <div class="home-footer__contact-block">
          <div class="home-footer__contact-eyebrow">Keep in Touch</div>
          <h2 class="home-footer__contact-title">请和我们保持联系</h2>
          <form class="home-footer__email-row" @submit.prevent="onSubmitPhone">
            <input
              v-model="phone"
              type="tel"
              name="footer-phone"
              maxlength="32"
              autocomplete="tel"
              placeholder="请输入您的电话"
              class="home-footer__email-input"
              aria-label="联系电话"
              :disabled="footerSubmitting"
            />
            <button
              type="submit"
              class="home-footer__email-submit"
              aria-label="提交电话"
              :disabled="footerSubmitting"
            >
              <PaperPlaneIcon class="home-footer__submit-icon" />
            </button>
          </form>
          <p v-if="footerError" class="home-footer__error" role="alert">{{ footerError }}</p>
          <p class="home-footer__contact-hint">我们的总工程师将尽快为您排忧。</p>
          <!-- 二维码移到"联系"列地址下方(用户反馈) -->
        </div>

        <!-- v2 风格 4 列网格(brand / 业务 / 关于 / 联系) -->
        <div class="home-footer__cols">
          <div class="home-footer__brand-col">
            <router-link to="/home" class="home-footer__logo-link" aria-label="美恺装饰">
              <img :src="totalLogoImg" alt="美恺装饰" class="home-footer__brand-logo" />
            </router-link>
            <!-- 用户反馈:去掉 logo 下面文字 -->
          </div>

          <div class="home-footer__col">
            <h4 class="home-footer__col-title">业 务</h4>
            <router-link class="home-footer__link" to="/store">品牌店装</router-link>
            <router-link class="home-footer__link" to="/business">商务办公</router-link>
            <router-link class="home-footer__link" to="/residential">精品家装</router-link>
          </div>

          <div class="home-footer__col">
            <h4 class="home-footer__col-title">关 于</h4>
            <router-link class="home-footer__link" to="/about">公司简介</router-link>
            <a class="home-footer__link" href="javascript:void(0)" role="button" @click="openChat">报价咨询</a>
            <router-link class="home-footer__link" to="/home">网站首页</router-link>
          </div>

          <div id="site-contact" class="home-footer__col home-footer__col--contact">
            <h4 class="home-footer__col-title">联 系</h4>
            <address class="home-footer__address">
              <div class="home-footer__addr-line home-footer__addr-line--phone">
                <PhoneIcon class="home-footer__addr-icon" />
                <a class="home-footer__tel" href="tel:13393736352">13393736352</a>
              </div>
              <div class="home-footer__addr-line">
                <LocationIcon class="home-footer__addr-icon" />
                <span>河南省郑州市管城回族区南台路9号</span>
              </div>
            </address>
            <!-- 二维码:贴在联系信息下方 -->
            <div class="home-footer__wechat-wrap">
              <img :src="wechatQrImg" alt="微信扫码联系" class="home-footer__wechat-qr" width="96" height="96" loading="lazy" />
            </div>
          </div>
        </div>

        <div class="home-footer__legal" role="contentinfo" aria-label="网站备案与版权信息">
          <span class="home-footer__legal-text">© {{ currentYear }} 美恺装饰版权所有</span>
          <span class="home-footer__legal-sep" aria-hidden="true">|</span>
          <a
            class="home-footer__legal-link"
            href="https://beian.miit.gov.cn/"
            target="_blank"
            rel="noopener noreferrer"
          >
          豫ICP备2026012727号
          </a>
          <span class="home-footer__legal-sep" aria-hidden="true">|</span>
          <a
            class="home-footer__legal-link"
            href="https://beian.mps.gov.cn/#/query/webSearch?recordcode=41010402003541"
            target="_blank"
            rel="noopener noreferrer"
          >
            豫公网安备41010402003541号
          </a>
          <span class="home-footer__legal-sep home-footer__legal-sep--fullwidth" aria-hidden="true">｜</span>
          <a
            class="home-footer__legal-link"
            href="https://github.com/carson-sun-dev"
            target="_blank"
            rel="noopener noreferrer"
          >
            技术支持
          </a>
        </div>
      </div>
    </footer>

    <div
      v-if="showSuccessModal"
      class="home-footer__modal"
      role="dialog"
      aria-modal="true"
      aria-label="提交成功弹窗"
    >
      <div class="home-footer__modal-card">
        <div class="home-footer__modal-title">提交成功</div>
        <div class="home-footer__modal-body">
          感谢您的信任，我们的总工程师将根据您的信息尽快联系您！
        </div>
        <button type="button" class="home-footer__modal-close" @click="showSuccessModal = false">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import LocationIcon from '@/components/icons/LocationIcon.vue'
import PhoneIcon from '@/components/icons/PhoneIcon.vue'
import { submitFooterPhone } from '@/api/leads'
import PaperPlaneIcon from '@/components/icons/PaperPlaneIcon.vue'
import totalLogoImg from '@/source/logo/total_logo.webp'
import wechatQrImg from '@/source/wechat.webp'
import { useChatWidget } from '@/composables/useChatWidget'

const { open: openChat } = useChatWidget()
import { validatePhone } from '@/utils/phoneValidation'
import { getCurrentYear } from '@/utils/companyTimeline'

const currentYear = getCurrentYear()

const phone = ref('')
const footerError = ref('')
const showSuccessModal = ref(false)
const footerSubmitting = ref(false)

async function onSubmitPhone() {
  if (footerSubmitting.value) return
  footerError.value = ''
  showSuccessModal.value = false

  const raw = phone.value.trim()
  if (!raw) {
    footerError.value = '请填写联系电话'
    return
  }
  if (!validatePhone(raw)) {
    footerError.value = '请填写正确的联系电话（手机号）'
    return
  }

  footerSubmitting.value = true
  try {
    await submitFooterPhone(raw)
    showSuccessModal.value = true
    phone.value = ''
  } catch (e) {
    footerError.value = e instanceof Error ? e.message : '提交失败，请稍后重试'
  } finally {
    footerSubmitting.value = false
  }
}
</script>

<style scoped>
.home-footer-shell {
  box-sizing: border-box;
}

/* === 单一深色 footer:全宽 + 无圆角(用户反馈) === */
.home-footer {
  background: #0e0e0e;
  padding: 4.5rem 1.5rem 2rem;
  color: #fff;
  width: 100%;
  /* 无 max-width / margin-inline / border-radius — 全宽方角 */
}
@media (min-width: 768px) {
  .home-footer { padding: 5rem 2rem 2.5rem; }
}

@media (min-width: 768px) {
  .home-footer {
    padding-top: 4rem;
    padding-bottom: 4rem;
  }
}

.home-footer__inner {
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}

@media (min-width: 768px) {
  .home-footer__inner {
    padding-left: 2rem;
    padding-right: 2rem;
  }
}

.home-footer__contact-block {
  position: relative;
  color: rgba(255, 255, 255, 0.92);
  padding-bottom: 3rem;
  margin-bottom: 3rem;
  /* 用户反馈:此处去掉 border-bottom 横线,只保留 footer 底部 legal 之上那一条 */
}

.home-footer__contact-eyebrow {
  text-align: center;
  font-family: 'EB Garamond', serif;
  font-style: italic;
  font-size: 13px;
  color: var(--mk-gold, #b8860b);
  letter-spacing: 0.4em;
  text-transform: uppercase;
  margin-bottom: 14px;
}
.home-footer__contact-eyebrow::before { content: '— '; }
.home-footer__contact-eyebrow::after { content: ' —'; }

.home-footer__contact-title {
  margin: 0;
  text-align: center;
  font-family: 'Noto Serif SC', serif;
  font-size: clamp(2rem, 5vw + 0.75rem, 3rem);
  font-weight: 600;
  line-height: 1.15;
  letter-spacing: 0.05em;
  color: #fff;
}

/* 二维码:放在"联系"列地址下方,跟字段一起堆叠 */
.home-footer__wechat-wrap {
  margin-top: 1.25rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}
.home-footer__wechat-qr {
  display: block;
  width: 96px;
  height: 96px;
  border-radius: 4px;
  object-fit: contain;
  background: #fff;
  padding: 4px;
  box-sizing: border-box;
  margin-left: 10%;
}
.home-footer__wechat-cap {
  margin: 0;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.45);
  letter-spacing: 0.2em;
}

.home-footer__contact-hint {
  margin: 1rem auto 0;
  max-width: 28rem;
  text-align: center;
  font-size: 0.9375rem;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.55);
}

.home-footer__email-row {
  margin: 1.75rem auto 0;
  display: flex;
  max-width: 28rem;
  align-items: center;
  gap: 0.5rem;
  border-radius: 9999px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.06);
  padding: 0.5rem 1rem;
}

.home-footer__error {
  margin: 0.5rem auto 0;
  max-width: 28rem;
  text-align: center;
  font-size: 0.875rem;
  line-height: 1.4;
  color: #ff8a8a;
}

.home-footer__email-input {
  min-width: 0;
  flex: 1;
  border: none;
  background: transparent;
  font-size: 0.875rem;
  color: #fff;
  outline: none;
}

.home-footer__email-input::placeholder {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.4);
  text-align: center;
}

.home-footer__email-submit {
  display: inline-flex;
  height: 2.25rem;
  width: 2.25rem;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  padding-left: 3px;
  border: none;
  border-radius: 9999px;
  background: #c41e3a;
  color: #fff;
  cursor: pointer;
  line-height: 0;
  transition: background-color 0.3s ease, transform 0.3s ease;
}
.home-footer__email-submit:hover {
  background: #8b1424;
  transform: scale(1.05);
}

.home-footer__email-submit:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.home-footer__submit-icon {
  display: block;
  width: 0.95rem;
  height: 0.95rem;
}

/* v2 风格 4 列网格 — 桌面 4 列;移动端聪明嵌套(用户反馈:不能粗暴堆叠) */
.home-footer__cols {
  margin-top: 3rem;
  display: grid;
  grid-template-columns: 1.6fr 1fr 1fr 1.4fr;
  gap: 3rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 3rem;
}
/* ≤900:brand 跨满居中 / 业务+关于 2 列并排居中 / 联系(含二维码) 跨满居中 */
@media (max-width: 900px) {
  .home-footer__cols { grid-template-columns: 1fr 1fr; gap: 2.8rem 2rem; }

  /* brand col:跨满 + logo 与内部水平居中 */
  .home-footer__brand-col {
    grid-column: 1 / -1;
    align-items: center;
    text-align: center;
  }
  .home-footer__brand-col .home-footer__logo-link {
    align-self: center;
    justify-content: center;
  }
  /* 重置 PC 端 margin-left: 60% / margin-top: 15% 偏移,否则 mobile 仍偏右 */
  .home-footer__brand-col .home-footer__brand-logo {
    margin: 0;
  }

  /* 业务 + 关于 col:标题与链接水平居中(用户反馈) */
  .home-footer__col:nth-of-type(2),
  .home-footer__col:nth-of-type(3) {
    align-items: center;
    text-align: center;
  }
  .home-footer__col:nth-of-type(2) .home-footer__link,
  .home-footer__col:nth-of-type(3) .home-footer__link {
    /* 取消默认 hover 的 padding-left 偏移(居中布局下会让链接跳到偏右) */
    padding-left: 0 !important;
    text-align: center;
    width: auto;
  }

  /* 联系 col:跨满 + 地址/二维码水平居中 */
  .home-footer__col:nth-of-type(4) {
    grid-column: 1 / -1;
    align-items: center;
    text-align: center;
  }
  .home-footer__col:nth-of-type(4) .home-footer__wechat-wrap {
    align-items: center;
  }
  .home-footer__col:nth-of-type(4) .home-footer__address,
  .home-footer__col:nth-of-type(4) .home-footer__addr-line {
    justify-content: center;
  }
}
/* ≤480 业务/关于 仍 2 列(短链接撑得下),不再继续拆 */

.home-footer__brand-col {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.home-footer__logo-link {
  display: inline-flex;
  align-self: flex-start;
  text-decoration: none;
  pointer-events: auto;
}

.home-footer__brand-logo {
  width: auto;
  height: 140px;          /* 没了文字,适当增大让 logo 撑住第一列 */
  object-fit: contain;
  pointer-events: none;
  margin-top: 15%;
  margin-left: 60%;
}

.home-footer__col {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.home-footer__col-title {
  margin: 0 0 1rem;
  font-family: 'Noto Serif SC', serif;
  font-size: 15px;
  font-weight: 500;
  color: #fff;
  letter-spacing: 0.18em;
}

.home-footer__link {
  display: block;
  padding: 6px 0;
  font-size: 13.5px;
  font-family: 'Noto Sans SC', system-ui, sans-serif;
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  white-space: nowrap;
  letter-spacing: 0.04em;
  transition: color 0.3s ease, padding-left 0.3s ease;
}
.home-footer__link:hover {
  color: #c41e3a;
  padding-left: 6px;
}

.home-footer__address {
  margin: 0;
  font-size: 13.5px;
  font-style: normal;
  color: rgba(255, 255, 255, 0.6);
}

.home-footer__addr-line {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  line-height: 1.6;
}

.home-footer__addr-line + .home-footer__addr-line {
  margin-top: 0.75rem;
}

.home-footer__col--contact {
  scroll-margin-top: 88px;
}

.home-footer__tel {
  color: inherit;
  text-decoration: none;
}

.home-footer__tel:hover {
  color: #fff;
  text-decoration: underline;
}

.home-footer__addr-icon {
  margin-top: 0.18rem;
  flex-shrink: 0;
  width: 1.05em;
  height: 1.05em;
  color: #c41e3a;
}

.home-footer__legal {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 0.35rem 0.5rem;
  margin-top: 2.25rem;
  padding-top: 1.25rem;
  border-top: 1px solid rgba(255, 255, 255, 0.12);
  font-size: 0.75rem;
  line-height: 1.45;
  text-align: center;
}

.home-footer__legal-text {
  color: rgba(255, 255, 255, 0.45);
}

.home-footer__legal-sep {
  color: rgba(255, 255, 255, 0.32);
  user-select: none;
}

.home-footer__legal-sep--fullwidth {
  color: rgba(255, 255, 255, 0.28);
}

.home-footer__legal-link {
  color: rgba(255, 255, 255, 0.5);
  text-decoration: none;
  white-space: nowrap;
}

.home-footer__legal-link:hover {
  color: rgba(255, 255, 255, 0.75);
  text-decoration: underline;
}

/* 与联系页报价表单「提交成功」弹窗一致 */
.home-footer__modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.25rem;
  box-sizing: border-box;
}

.home-footer__modal-card {
  width: 100%;
  max-width: 520px;
  background: #fff;
  border-radius: 16px;
  padding: 1.25rem 1.25rem 1rem;
  box-sizing: border-box;
  box-shadow: 0 20px 50px rgb(0 0 0 / 0.2);
}

.home-footer__modal-title {
  font-weight: 900;
  letter-spacing: -0.02em;
  font-size: 1.1rem;
  color: #111;
}

.home-footer__modal-body {
  margin-top: 0.75rem;
  font-size: 0.95rem;
  color: rgba(0, 0, 0, 0.8);
  line-height: 1.6;
}

.home-footer__modal-close {
  margin-top: 1.1rem;
  height: 42px;
  width: 100%;
  border-radius: 999px;
  border: none;
  cursor: pointer;
  background: #111;
  color: #fff;
  font-weight: 800;
  font-size: 0.95rem;
}
</style>
