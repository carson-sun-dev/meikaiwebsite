<template>
  <section class="home-why">
    <div class="home-why__inner">
      <header class="home-why__head">
        <h2 class="home-why__title">为什么选择美恺装饰？</h2>
        <p class="home-why__promise">我们承诺！</p>
      </header>
      <div class="why-hover-list" role="list" @mouseleave="accordionActive = null">
        <div
          v-for="row in homeWhyItems"
          :key="row.name"
          class="why-hover-item"
          role="listitem"
          @mouseenter="accordionActive = row.name"
        >
          <div
            class="why-hover-item__header"
            :aria-expanded="accordionActive === row.name"
          >
            <span class="why-item__head">
              <span class="why-item__heading">{{ row.title }}</span>
              <span class="why-item__num" aria-hidden="true">{{ row.num }}</span>
            </span>
            <el-icon
              class="why-hover-item__arrow"
              :class="{ 'is-open': accordionActive === row.name }"
              aria-hidden="true"
            >
              <ArrowRight />
            </el-icon>
          </div>
          <div
            class="why-hover-item__panel-anim"
            :class="{ 'is-open': accordionActive === row.name }"
          >
            <div class="why-hover-item__panel-inner">
              <div class="why-hover-item__panel">
                <p class="home-why__body">{{ row.body }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ArrowRight } from '@element-plus/icons-vue'
import { ref } from 'vue'

import { homeWhyItems } from '@/data/homeWhyItems'

/** 当前悬停展开的面板，移出列表区域后全部收起 */
const accordionActive = ref<string | null>(null)
</script>

<style scoped>
.why-hover-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.why-hover-item {
  overflow: hidden;
  border-radius: 0.75rem;
  background: rgb(245 245 245);
}

.why-hover-item__header {
  display: flex;
  align-items: center;
  min-height: 3.5rem;
  padding: 1rem 1.25rem;
  font-size: 1rem;
  font-weight: 400;
  color: rgb(23 23 23);
  cursor: default;
  user-select: none;
}

.why-item__head {
  display: flex;
  flex: 1;
  min-width: 0;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.why-item__heading {
  flex: 1;
  min-width: 0;
  font-weight: 700;
  text-align: left;
}

.why-item__num {
  flex-shrink: 0;
  margin-right: 1rem;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  color: #171717;
}

.why-hover-item__arrow {
  flex-shrink: 0;
  font-size: 1rem;
  transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  color: rgb(23 23 23);
}

.why-hover-item__arrow.is-open {
  transform: rotate(90deg);
}

/* 高度过渡：0fr → 1fr，避免 v-show 瞬间切换 */
.why-hover-item__panel-anim {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.why-hover-item__panel-anim.is-open {
  grid-template-rows: 1fr;
}

.why-hover-item__panel-inner {
  overflow: hidden;
  min-height: 0;
}

.why-hover-item__panel {
  padding: 0 1.25rem 1.25rem;
  padding-top: 0;
}
</style>
