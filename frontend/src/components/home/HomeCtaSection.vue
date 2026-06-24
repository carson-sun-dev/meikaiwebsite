<template>
  <section class="cta-wrap">
    <div class="cta-card">
      <div class="cta-bg" aria-hidden="true">
        <img :src="bgImg" alt="" class="cta-img" />
        <div class="cta-overlay"></div>
        <div class="cta-watermark" :style="{ backgroundImage: `url(${logoImg})` }"></div>
      </div>
      <div class="cta-inner">
        <span class="cta-eyebrow">Get Your Quote</span>
        <h2 class="cta-title">即刻获取您的专属报价</h2>
        <p class="cta-sub">
          {{ scheduleYear }} 年工程排期已开启 · 留下手机号，总工程师 24 小时内主动联系
        </p>

        <form class="cta-form" @submit.prevent="onSubmit">
          <input
            v-model="name"
            type="text"
            class="cta-input"
            placeholder="您的称呼(选填)"
            maxlength="32"
            autocomplete="name"
            :disabled="submitting"
          />
          <input
            v-model="phone"
            type="tel"
            class="cta-input"
            placeholder="手机号"
            maxlength="32"
            autocomplete="tel"
            aria-label="联系电话"
            :disabled="submitting"
          />
          <button type="submit" class="mk-btn mk-btn--primary cta-submit" :disabled="submitting">
            <PaperPlaneIcon class="cta-submit-icon" />
            <span>{{ submitting ? '提交中...' : '立刻获取报价' }}</span>
          </button>
        </form>
        <p v-if="errorMsg" class="cta-err" role="alert">{{ errorMsg }}</p>
      </div>
    </div>

    <!-- 提交成功 modal -->
    <div
      v-if="showSuccess"
      class="cta-modal"
      role="dialog"
      aria-modal="true"
      aria-label="提交成功"
      @click.self="showSuccess = false"
    >
      <div class="cta-modal-card">
        <div class="cta-modal-title">提交成功</div>
        <div class="cta-modal-body">
          感谢您的信任,我们的总工程师将根据您的信息尽快联系您。
        </div>
        <button type="button" class="mk-btn mk-btn--ink cta-modal-close" @click="showSuccess = false">
          知道了
        </button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import PaperPlaneIcon from '@/components/icons/PaperPlaneIcon.vue'
import bgImg from '@/source/homepage/4/1.webp'
import logoImg from '@/source/logo/logo.webp'
import { submitFooterPhone } from '@/api/leads'
import { validatePhone } from '@/utils/phoneValidation'
import { getCurrentYear } from '@/utils/companyTimeline'

const scheduleYear = getCurrentYear()

const name = ref('')
const phone = ref('')
const submitting = ref(false)
const errorMsg = ref('')
const showSuccess = ref(false)

async function onSubmit() {
  if (submitting.value) return
  errorMsg.value = ''
  const rawPhone = phone.value.trim()
  if (!rawPhone) {
    errorMsg.value = '请填写联系电话'
    return
  }
  if (!validatePhone(rawPhone)) {
    errorMsg.value = '请填写正确的手机号'
    return
  }
  submitting.value = true
  try {
    // 当前后端 /api/leads/footer-phone 只收 phone;name 暂时仅前端展示,
    // 后端扩展字段后再传(2026-06-22 一期不破后端 API)
    await submitFooterPhone(rawPhone)
    showSuccess.value = true
    name.value = ''
    phone.value = ''
  } catch (e) {
    errorMsg.value = e instanceof Error ? e.message : '提交失败,请稍后重试'
  } finally {
    submitting.value = false
  }
}

// onQuoteClick 兼容旧 emit 接口(避免父组件断链);现已弃用,改走内嵌表单
defineEmits<{ quoteClick: [] }>()
</script>

<style scoped>
.cta-wrap {
  padding: 56px 24px 80px;
  background: var(--mk-paper);
}

.cta-card {
  position: relative;
  overflow: hidden;
  max-width: var(--mk-container);
  min-height: 440px;
  margin: 0 auto;
  border-radius: 8px;
  display: flex;
}

.cta-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}
.cta-img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.cta-overlay {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(135deg, rgba(26, 26, 26, 0.88) 0%, rgba(26, 26, 26, 0.62) 70%, rgba(26, 26, 26, 0.75) 100%);
}
.cta-watermark {
  position: absolute;
  top: -80px;
  right: -80px;
  width: 420px;
  height: 420px;
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0.07;
}

.cta-inner {
  position: relative;
  z-index: 2;
  padding: 72px 56px;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  width: 100%;
  max-width: 760px;
  margin: 0 auto;
}

.cta-eyebrow {
  display: inline-block;
  font-family: var(--mk-font-en);
  font-style: italic;
  font-size: 13px;
  color: rgba(184, 134, 11, 0.95);
  letter-spacing: 0.4em;
  text-transform: uppercase;
  margin-bottom: 18px;
}
.cta-eyebrow::before { content: '— '; }
.cta-eyebrow::after { content: ' —'; }

.cta-title {
  margin: 0;
  font-family: var(--mk-font-serif);
  font-size: clamp(28px, 4vw, 44px);
  font-weight: 600;
  letter-spacing: 0.05em;
  line-height: 1.3;
}

.cta-sub {
  margin: 18px 0 36px;
  font-size: 15px;
  color: rgba(255, 255, 255, 0.78);
  letter-spacing: 0.06em;
  line-height: 1.7;
  max-width: 560px;
}

.cta-form {
  display: flex;
  gap: 12px;
  max-width: 640px;
  width: 100%;
  flex-wrap: wrap;
  justify-content: center;
}
.cta-input {
  flex: 1;
  min-width: 200px;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 4px;
  color: white;
  font-family: inherit;
  font-size: 14px;
  letter-spacing: 0.05em;
  outline: none;
  transition: border-color 0.3s ease, background-color 0.3s ease;
}
.cta-input::placeholder { color: rgba(255, 255, 255, 0.5); }
.cta-input:focus {
  background: rgba(255, 255, 255, 0.12);
  border-color: var(--mk-brand);
}
.cta-input:disabled { opacity: 0.6; cursor: not-allowed; }

.cta-submit {
  flex: 0 0 auto;
  padding: 16px 32px;
  font-size: 14px;
}
.cta-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none !important;
}
.cta-submit-icon {
  width: 14px;
  height: 14px;
  color: currentColor;
}

.cta-err {
  margin: 14px 0 0;
  font-size: 13px;
  color: #ffb3b3;
  letter-spacing: 0.04em;
}

/* Modal */
.cta-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 9998;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.25rem;
  backdrop-filter: blur(4px);
}
.cta-modal-card {
  width: 100%;
  max-width: 480px;
  background: var(--mk-paper-pure);
  border-radius: 8px;
  padding: 32px 28px 24px;
  box-shadow: 0 24px 56px rgba(0, 0, 0, 0.24);
}
.cta-modal-title {
  font-family: var(--mk-font-serif);
  font-size: 22px;
  font-weight: 600;
  color: var(--mk-ink);
  letter-spacing: 0.05em;
}
.cta-modal-body {
  margin-top: 14px;
  font-size: 14.5px;
  color: var(--mk-ink-2);
  line-height: 1.7;
}
.cta-modal-close {
  margin-top: 24px;
  width: 100%;
  justify-content: center;
}

@media (max-width: 768px) {
  .cta-card { min-height: 360px; }
  .cta-inner { padding: 56px 28px; }
  .cta-watermark { width: 240px; height: 240px; top: -40px; right: -40px; }
  .cta-form { flex-direction: column; }
  .cta-input { width: 100%; }
  .cta-submit { width: 100%; }
}
</style>
