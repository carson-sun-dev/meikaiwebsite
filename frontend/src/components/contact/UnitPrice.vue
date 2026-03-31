<template>
  <div class="unit-price" aria-label="单价">
    <div class="unit-price__value">{{ value }}¥</div>
    <div class="unit-price__unit">/平方米</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  value: number
}>()
</script>

<style scoped>
.unit-price {
  display: flex;
  gap: 4px;
  align-items: flex-end;
  justify-content: flex-start;
}

.unit-price__value {
  font-family: Manrope, 'Noto Sans SC', 'Noto Sans JP', system-ui, sans-serif;
  font-weight: 800;
  font-size: 2rem;
  line-height: 1;
  letter-spacing: -0.03em;
  color: #000;
}

.unit-price__unit {
  font-family: Manrope, 'Noto Sans SC', 'Noto Sans JP', system-ui, sans-serif;
  font-weight: 600;
  font-size: 1rem;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: rgba(0, 0, 0, 0.75);
  padding-bottom: 0.25rem;
}
</style>

