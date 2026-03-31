<template>
  <section class="home-pricing">
    <div class="home-pricing__inner">
      <h2 class="home-pricing__title">装修单价</h2>
      <div class="home-pricing__grid">
        <div v-for="plan in plans" :key="plan.title" class="home-price-card">
          <h3 class="home-price-card__title">{{ plan.title }}</h3>
          <p class="home-price-card__price">{{ plan.price }}</p>
          <ul class="home-price-card__list">
            <li v-for="line in plan.lines" :key="line" class="home-price-card__item">
              <span class="home-price-card__dot" />
              <span>{{ line }}</span>
            </li>
          </ul>
          <el-button round class="home-price-card__btn">了解详情</el-button>
        </div>
      </div>

      <p class="home-pricing__note">
        *该单价仅供参考，详情请致电咨询
      </p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import type { HomePricingPlan } from '@/data/homePricingPlans'
import { homePricingPlans } from '@/data/homePricingPlans'

const props = withDefaults(
  defineProps<{
    /** 传入则覆盖默认首页套餐数据 */
    plans?: HomePricingPlan[]
  }>(),
  {
    plans: undefined,
  },
)

const plans = computed(() => props.plans ?? homePricingPlans)
</script>

<style scoped>
.home-pricing {
  background: #fafafa;
  padding: 5rem 1.5rem;
}

@media (min-width: 768px) {
  .home-pricing {
    padding-top: 6rem;
    padding-bottom: 6rem;
  }
}

.home-pricing__inner {
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}

@media (min-width: 768px) {
  .home-pricing__inner {
    padding-left: 2rem;
    padding-right: 2rem;
  }
}

.home-pricing__title {
  margin: 0 0 2rem;
  text-align: center;
  font-size: clamp(1.6rem, 2.8vw + 0.7rem, 2.4rem);
  font-weight: 900;
  letter-spacing: -0.03em;
  color: #111;
}

.home-pricing__grid {
  display: grid;
  gap: 2rem;
}

@media (min-width: 768px) {
  .home-pricing__grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.home-price-card {
  display: flex;
  flex-direction: column;
  border-radius: 1rem;
  background: rgba(245, 245, 245, 0.9);
  padding: 2rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.home-price-card__title {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #171717;
}

.home-price-card__price {
  margin-top: 1rem;
  font-size: 1.875rem;
  font-weight: 700;
  color: #171717;
}

.home-price-card__list {
  margin: 1.5rem 0 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: #525252;
}

.home-price-card__item {
  display: flex;
  gap: 0.5rem;
}

.home-price-card__dot {
  margin-top: 0.5rem;
  height: 0.375rem;
  width: 0.375rem;
  flex-shrink: 0;
  border-radius: 9999px;
  background: #a3a3a3;
}

.home-price-card__btn {
  margin-top: 2rem;
}

.home-price-card__btn.el-button {
  border: 0;
  background: #171717;
  color: #fff;
}

.home-pricing__note {
  margin-top: 1.5rem;
  text-align: center;
  font-weight: 800;
  color: #000;
  font-size: 0.95rem;
}
</style>
