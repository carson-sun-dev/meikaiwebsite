<template>
  <div class="home-footer-shell">
    <footer class="home-footer">
      <div class="home-footer__inner">
        <div class="home-footer__contact-block">
          <h2 class="home-footer__contact-title">保持联系</h2>
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
          <p class="home-footer__contact-hint">我们的总工程师将尽快联系您，为您排忧。</p>
          <div class="home-footer__wechat-wrap">
            <img :src="wechatQrImg" alt="微信扫码联系" class="home-footer__wechat-qr" width="88" height="88" loading="lazy" />
          </div>
        </div>

        <div class="home-footer__bottom">
          <router-link to="/home" class="home-footer__logo-link" aria-label="美恺装饰">
            <img :src="logoImg" alt="" class="home-footer__logo-mark" />
            <img :src="ziImg" alt="美恺装饰" class="home-footer__logo-word" />
          </router-link>
          <nav class="home-footer__nav" aria-label="页脚快速链接">
            <router-link class="home-footer__link" to="/">网站首页</router-link>
            <router-link class="home-footer__link" to="/store">
              品牌店装
            </router-link>
            <router-link class="home-footer__link" to="/business">商务·办公</router-link>
            <router-link class="home-footer__link" to="/residential">精品家装</router-link>
          </nav>
          <address class="home-footer__address">
            <div class="home-footer__addr-line">
              <el-icon><Phone /></el-icon>
              <span>13393736352</span>
            </div>
            <div class="home-footer__addr-line">
              <el-icon><Location /></el-icon>
              <span>河南省郑州市管城回族区南台路9号</span>
            </div>
          </address>
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
            href="https://beian.mps.gov.cn/#/query/webSearch?recordcode=11010502000000"
            target="_blank"
            rel="noopener noreferrer"
          >
            豫公网安备 （暂时占位）XXXXXX号
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
import { Location, Phone } from '@element-plus/icons-vue'

import { submitFooterPhone } from '@/api/leads'
import PaperPlaneIcon from '@/components/icons/PaperPlaneIcon.vue'
import logoImg from '@/source/logo/logo.png'
import ziImg from '@/source/logo/zi.png'
import wechatQrImg from '@/source/wechat.png'
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
/* 与 Gallery / CTA 同宽对齐的左右留白 */
.home-footer-shell {
  padding-inline: max(1rem, calc((100vw - 67.5rem) / 2));
  box-sizing: border-box;
}

@media (min-width: 768px) {
  .home-footer-shell {
    padding-inline: max(1.5rem, calc((100vw - 67.5rem) / 2));
  }
}

.home-footer {
  background: #000;
  padding: 3.25rem 1.5rem;
  color: #fff;
  border-top-left-radius: 1.25rem;
  border-top-right-radius: 1.25rem;
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
}

.home-footer__contact-title {
  margin: 0;
  text-align: center;
  font-size: clamp(2rem, 5vw + 0.75rem, 3.25rem);
  font-weight: 600;
  line-height: 1.15;
  letter-spacing: -0.02em;
}

/* 与输入框（max-width 28rem）右缘对齐留白，absolute 不参与居中计算 */
.home-footer__wechat-wrap {
  position: absolute;
  left: calc(50% + 14rem + 0.75rem);
  /* 与 max-width 28rem 的输入条垂直居中对齐（标题 + 1.75rem margin 后取行高一半） */
  top: 7.05rem;
  width: 5.25rem;
  height: 5.25rem;
  transform: translateY(-50%);
}

.home-footer__wechat-qr {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: 0.35rem;
  object-fit: contain;
  background: #fff;
}

@media (max-width: 767px) {
  .home-footer__wechat-wrap {
    position: static;
    left: auto;
    top: auto;
    width: 5.25rem;
    height: 5.25rem;
    margin: 1.25rem auto 0;
    transform: none;
  }
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
  background: rgba(255, 255, 255, 0.05);
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
  color: rgba(255, 255, 255, 0.4);
}

.home-footer__email-submit {
  display: inline-flex;
  height: 2.25rem;
  width: 2.25rem;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  padding: 0;
  border: none;
  border-radius: 9999px;
  background: #fff;
  color: #000;
  cursor: pointer;
  line-height: 0;
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

.home-footer__bottom {
  margin-top: 3rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 2rem;
}

@media (min-width: 768px) {
  .home-footer__bottom {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}

.home-footer__logo-link {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  align-self: center;
  box-sizing: border-box;
  text-decoration: none;
}

@media (min-width: 768px) {
  .home-footer__logo-link {
    transform: translateY(-0.25rem);
  }
}

.home-footer__logo-mark {
  width: 56px;
  height: 52px;
  flex-shrink: 0;
  object-fit: contain;
  pointer-events: none;
}

.home-footer__logo-word {
  width: 105px;
  height: 52px;
  flex-shrink: 0;
  object-fit: contain;
  pointer-events: none;
}

.home-footer__nav {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 0.5rem 1.25rem;
  font-family:
    Manrope,
    'Noto Sans JP',
    'Noto Sans SC',
    system-ui,
    sans-serif;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.2;
  letter-spacing: -0.14px;
}

.home-footer__link {
  color: #fff;
  text-decoration: none;
  white-space: nowrap;
}

.home-footer__link:hover {
  opacity: 0.92;
}

.home-footer__address {
  margin: 0;
  font-size: 0.875rem;
  font-style: normal;
  color: rgba(255, 255, 255, 0.65);
}

.home-footer__addr-line {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.home-footer__addr-line + .home-footer__addr-line {
  margin-top: 0.5rem;
}

.home-footer__addr-line :deep(.el-icon) {
  margin-top: 0.125rem;
  flex-shrink: 0;
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
