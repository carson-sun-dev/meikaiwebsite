<template>
  <div class="store-page">
    <div class="store-page__navbg" aria-hidden="true">
      <NavigationBar />
    </div>

    <main class="store-page__main">
      <section class="store-cases">
        <div class="store-cases__wrap">
          <h1 class="store-cases__title">品牌店铺装修案例</h1>

          <article
            v-for="(item, idx) in cases"
            :key="item.title"
            class="store-case"
            :class="{ 'store-case--reverse': idx % 2 === 1 }"
          >
            <div class="store-case__left">
              <h2 class="store-case__name">{{ item.title }}</h2>
              <div class="store-case__images">
                <img :src="item.imageA" alt="" class="store-case__img store-case__img--a" />
                <img :src="item.imageB" alt="" class="store-case__img store-case__img--b" />
              </div>
            </div>

            <div class="store-case__right">
              <p class="store-case__desc">{{ item.desc }}</p>
              <p class="store-case__date">{{ item.date }}</p>
            </div>
          </article>
        </div>
      </section>
    </main>

    <HomeFooter />
  </div>
</template>

<script setup lang="ts">
import NavigationBar from '@/components/navigationBar.vue'
import HomeFooter from '@/components/home/HomeFooter.vue'

import storeImg1 from '@/source/store/1_1.jpg'
import storeImg2 from '@/source/store/1_2.jpg'

const cases = [
  {
    title: '福状元 吾悦广场店',
    imageA: storeImg1,
    imageB: storeImg2,
    desc: 'In September 2023, 10 young people aged 16-18 from Belfast curated a photo exhibition showcasing how public spaces like parks, restaurants, and buses shape their experiences of community relations. The event featured their reflections on growing up in the city and how shared spaces influence intergroup interactions.',
    date: '19/09-19/10',
  },
  {
    title: 'Shared Spaces Through Young Eyes',
    imageA: storeImg2,
    imageB: storeImg1,
    desc: 'Held in June 2024, this exhibition presented photographs and narratives from youth in Bradford, exploring how shared public environments affect social cohesion and their sense of belonging in a multicultural city.',
    date: '18/09-19/10',
  },
  {
    title: 'Peachtree Shared Space Demonstration Project Launch',
    imageA: storeImg1,
    imageB: storeImg2,
    desc: 'A temporary transformation of three blocks on Peachtree Street in Atlanta to test shared space concepts. The project aimed to prioritize pedestrians and assess how reduced vehicle dominance could enhance urban vibrancy and inform final design decisions.',
    date: '19/09-19/10',
  },
  {
    title: 'Good Relations - Shared Spaces Project Showcase',
    imageA: storeImg2,
    imageB: storeImg1,
    desc: 'During Good Relations Week 2023, a physical exhibition was held to present findings from the Shared Spaces Project, including youth photography and interviews. The event highlighted how public spaces impact youth perceptions of community relations in Belfast.',
    date: '18/09-19/10',
  },
] as const
</script>

<style scoped>
.store-page {
  min-height: 100dvh;
  background: #efefef;
  color: #000;
}

.store-page__navbg {
  background: #000;
}

.store-page__main {
  padding: 1.5rem 0 2.5rem;
}

.store-cases__wrap {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
  box-sizing: border-box;
}

.store-cases__title {
  margin: 0;
  text-align: center;
  font-size: clamp(2rem, 3.2vw + 0.8rem, 3rem);
  font-weight: 900;
  letter-spacing: -0.03em;
}

.store-case {
  display: grid;
  grid-template-columns: minmax(0, 657px) minmax(320px, 1fr);
  gap: clamp(1.25rem, 4vw, 72px);
  align-items: stretch;
  padding: 3rem 0;
}

.store-case + .store-case {
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}

.store-case--reverse {
  grid-template-columns: minmax(320px, 1fr) minmax(0, 657px);
}

.store-case--reverse .store-case__left {
  grid-column: 2;
  grid-row: 1;
}

.store-case--reverse .store-case__right {
  grid-column: 1;
  grid-row: 1;
  align-items: flex-start;
}

.store-case__left {
  display: flex;
  min-width: 0;
  flex-direction: column;
  gap: 1.25rem;
}

.store-case__name {
  margin: 0;
  font-size: 1.5rem;
  line-height: 1.2;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.store-case__images {
  display: grid;
  grid-template-columns: minmax(0, 373px) minmax(0, 1fr);
  gap: 20px;
}

.store-case__img {
  width: 100%;
  height: 248px;
  object-fit: cover;
  background: #d9d9d9;
}

.store-case__right {
  display: flex;
  min-width: 0;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-end;
  gap: 1.5rem;
  /* 与图片区顶部对齐，而不是与工程名顶部对齐 */
  padding-top: 3.1rem;
}

.store-case__desc {
  margin: 0;
  font-size: 1rem;
  line-height: 1.55;
  letter-spacing: -0.01em;
}

.store-case__date {
  margin: 0;
  font-size: 0.75rem;
  text-decoration: underline;
  text-underline-offset: 0.18em;
  letter-spacing: -0.01em;
}

@media (max-width: 980px) {
  .store-case,
  .store-case--reverse {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }

  .store-case--reverse .store-case__left,
  .store-case--reverse .store-case__right {
    grid-column: auto;
  }

  .store-case__images {
    grid-template-columns: 1fr 1fr;
  }

  .store-case__img {
    height: 210px;
  }

  .store-case__right,
  .store-case--reverse .store-case__right {
    align-items: flex-start;
    padding-top: 0;
  }
}
</style>

