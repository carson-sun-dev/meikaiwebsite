<template>
  <section class="contact-unitref" aria-label="参考单价">
    <div class="contact-unitref__wrap">
      <h2 class="contact-unitref__page-title">装修单价</h2>
      <div class="contact-unitref__grid" role="list">
        <div
          v-for="p in plans"
          :key="p.key"
          class="contact-unitref__cell"
          :class="{ 'contact-unitref__cell--active': p.key === activeKey }"
          role="listitem"
        >
          <div class="contact-unitref__title">{{ p.title }}</div>
          <UnitPrice :value="p.unitPrice" />
          <ul class="contact-unitref__bullets">
            <li v-for="b in p.bullets" :key="b">{{ b }}</li>
          </ul>
        </div>
      </div>

      <p class="contact-unitref__note">
        *该单价仅供参考，详情请致电咨询
      </p>
    </div>
  </section>
</template>

<script setup lang="ts">
import UnitPrice from './UnitPrice.vue'

export type ContactUnitRefPlan = {
  key: 'store' | 'business' | 'residential'
  title: string
  unitPrice: number
  bullets: string[]
}

defineProps<{
  plans: ContactUnitRefPlan[]
  activeKey: ContactUnitRefPlan['key']
}>()
</script>

<style scoped>
.contact-unitref {
  margin-top: 1.25rem;
}

.contact-unitref__page-title {
  margin: 0 0 1.5rem;
  text-align: center;
  font-weight: 900;
  letter-spacing: -0.03em;
  font-size: clamp(1.4rem, 2vw + 0.9rem, 2rem);
  color: #111;
}

.contact-unitref__wrap {
  width: 100%;
  max-width: 1080px;
  margin-left: auto;
  margin-right: auto;
  padding: 0 1.5rem;
  box-sizing: border-box;
}

.contact-unitref__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.25rem;
}

@media (max-width: 980px) {
  .contact-unitref__grid {
    grid-template-columns: 1fr;
  }
}

.contact-unitref__cell {
  background: #f1f1f1;
  border-radius: 10px;
  padding: 1.4rem 1.25rem 1.25rem;
  box-sizing: border-box;
}

.contact-unitref__cell--active {
  box-shadow: inset 0 0 0 2px rgba(0, 0, 0, 0.08);
}

.contact-unitref__title {
  font-weight: 700;
  color: #111;
  margin-bottom: 0.9rem;
  font-size: 1rem;
}

.contact-unitref__bullets {
  margin: 0.75rem 0 0;
  padding-left: 1.25rem;
  font-size: 0.875rem;
  color: rgba(0, 0, 0, 0.6);
  line-height: 1.6;
}

.contact-unitref__bullets li + li {
  margin-top: 0.25rem;
}

.contact-unitref__note {
  margin: 1rem 0 0;
  text-align: center;
  font-weight: 800;
  font-size: 0.85rem;
  color: #000;
}
</style>

