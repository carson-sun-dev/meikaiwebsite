<template>
  <section class="home-process" aria-label="从咨询到交付">
    <div class="home-process__wrap">
      <div class="home-process__head">
        <h2 class="home-process__title">从咨询到交付，4步走完</h2>
        <p class="home-process__subtitle">让你清楚知道每个节点正在做什么。</p>
      </div>

      <div class="home-process__grid">
        <div v-for="s in steps" :key="s.no" class="home-step">
          <div class="home-step__no">{{ s.no }}</div>
          <div class="home-step__title">{{ s.title }}</div>
          <div class="home-step__desc">{{ s.desc }}</div>
          <div class="home-step__glow" aria-hidden="true" />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const steps = [
  {
    no: '01',
    title: '需求沟通',
    desc: '确认装修目标、风格偏好与预算范围，让方案从源头更准确。',
  },
  {
    no: '02',
    title: '方案设计',
    desc: '提供可落地的设计与结构说明，并配合关键节点的对齐确认。',
  },
  {
    no: '03',
    title: '施工实施',
    desc: '用工艺标准推进每一道工序，保证质量与进度可视化。',
  },
  {
    no: '04',
    title: '验收交付',
    desc: '完成细节收口与整体复核，让结果一次到位更省心。',
  },
] as const
</script>

<style scoped>
.home-process {
  padding: 5rem 1.5rem;
  background: #fff;
}

@media (min-width: 768px) {
  .home-process {
    padding-top: 6rem;
    padding-bottom: 6rem;
  }
}

.home-process__wrap {
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1.5rem;
  padding-right: 1.5rem;
  box-sizing: border-box;
}

@media (min-width: 768px) {
  .home-process__wrap {
    padding-left: 2rem;
    padding-right: 2rem;
  }
}

.home-process__head {
  text-align: center;
}

.home-process__title {
  margin: 0;
  font-size: clamp(1.6rem, 2.8vw + 0.7rem, 2.4rem);
  font-weight: 900;
  letter-spacing: -0.03em;
}

.home-process__subtitle {
  margin: 1rem auto 0;
  max-width: 36rem;
  color: rgba(0, 0, 0, 0.55);
  font-size: 0.95rem;
  line-height: 1.7;
}

.home-process__grid {
  margin-top: 2rem;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
}

.home-step {
  position: relative;
  border-radius: 16px;
  background: #f1f1f1;
  padding: 1.1rem 1rem 1.2rem;
  box-sizing: border-box;
  overflow: hidden;
}

.home-step__no {
  font-weight: 900;
  font-size: 1rem;
  letter-spacing: -0.02em;
  color: rgba(0, 0, 0, 0.7);
}

.home-step__title {
  margin-top: 0.65rem;
  font-weight: 900;
  letter-spacing: -0.02em;
}

.home-step__desc {
  margin-top: 0.55rem;
  color: rgba(0, 0, 0, 0.6);
  line-height: 1.7;
  font-size: 0.9rem;
}

.home-step__glow {
  position: absolute;
  left: -30%;
  bottom: -40%;
  width: 160%;
  height: 120%;
  background: radial-gradient(circle at 20% 30%, rgba(255, 84, 73, 0.18), transparent 60%);
  pointer-events: none;
}

@media (max-width: 980px) {
  .home-process__grid {
    grid-template-columns: 1fr;
  }
}
</style>

