<template>
  <div class="home-footer-shell">
    <footer class="home-footer">
      <div class="home-footer__inner">
        <div>
          <h2 class="home-footer__contact-title">保持联系</h2>
          <div class="home-footer__email-row">
            <input
              type="tel"
              placeholder="请输入电话"
              class="home-footer__email-input"
            />
            <button type="button" class="home-footer__email-submit" aria-label="提交">
              <PaperPlaneIcon class="home-footer__submit-icon" />
            </button>
          </div>
          <p class="home-footer__contact-hint">我们的总工程师将尽快联系您，为您排忧。</p>
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
            <span class="home-footer__muted">商务·办公</span>
            <span class="home-footer__muted">精品家装</span>
          </nav>
          <address class="home-footer__address">
            <div class="home-footer__addr-line">
              <el-icon><Location /></el-icon>
              <span>河南省郑州市 · 示例地址 88 号</span>
            </div>
            <div class="home-footer__addr-line">
              <el-icon><Phone /></el-icon>
              <span>400-000-0000</span>
            </div>
          </address>
        </div>

        <div class="home-footer__legal" role="contentinfo" aria-label="网站备案与版权信息">
          <span class="home-footer__legal-text">© 2026 美恺装饰版权所有</span>
          <span class="home-footer__legal-sep" aria-hidden="true">|</span>
          <a
            class="home-footer__legal-link"
            href="https://beian.miit.gov.cn/"
            target="_blank"
            rel="noopener noreferrer"
          >
            豫ICP备12345678号-1
          </a>
          <span class="home-footer__legal-sep" aria-hidden="true">|</span>
          <span class="home-footer__legal-text">豫公网安备 11010502XXXXXX号</span>
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
  </div>
</template>

<script setup lang="ts">
import { Location, Phone } from '@element-plus/icons-vue'

import PaperPlaneIcon from '@/components/icons/PaperPlaneIcon.vue'
import logoImg from '@source/logo/logo.png'
import ziImg from '@source/logo/zi.png'
</script>

<style scoped>
/* 与 Gallery / CTA 同宽对齐的左右留白 */
.home-footer-shell {
  padding-inline: max(1.5rem, calc((100vw - 67.5rem) / 2));
  box-sizing: border-box;
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

.home-footer__contact-title {
  margin: 0;
  text-align: center;
  font-size: clamp(2rem, 5vw + 0.75rem, 3.25rem);
  font-weight: 600;
  line-height: 1.15;
  letter-spacing: -0.02em;
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

.home-footer__muted {
  cursor: default;
  color: rgba(255, 255, 255, 0.72);
  white-space: nowrap;
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
</style>
