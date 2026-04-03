<template>
  <section class="home-business">
    <div class="home-business__inner">
      <h2 class="home-business__label">业务细节</h2>
      <div class="home-business__body">
        <p class="home-business__para">
          我们专注于<router-link to="/store" class="home-business__accent">品牌店铺</router-link>装修，至今已成功交付
          <span class="home-business__metric">120+</span>
          。从网红餐饮、品牌零售到高端会所，
          我们将每一平米都转化为商业价值，助力店主实现从“开业”到“爆火”的跨越。
        </p>
        <p class="home-business__para">
          我们为企业提供<router-link to="/business" class="home-business__accent">商务·办公</router-link>解决方案，已完成
          <span class="home-business__metric">30+</span>
          高标准商务办公项目。为您的团队构筑激发灵感的创意引擎，让办公空间成为彰显企业实力与格局的窗口。
        </p>
        <p class="home-business__para">
          美恺从<router-link to="/residential" class="home-business__accent">精品家装</router-link>起家，已为
          <span class="home-business__metric">200+</span>
          个家庭定制了梦想之家。我们始终对家装保持着最深沉的敬畏。
          从零散的图纸到温暖的实景,我们坚持将客户需求置于首位。
        </p>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* Figma 画幅约 1080×560：内容区 1080px，区块高度约 560px，与 Gallery 共用同一水平留白 */
.home-business {
  border-top: 1px solid #f5f5f5;
  background: #fff;
  padding-top: 3.5rem;
  padding-bottom: 4rem;
  padding-inline: max(1rem, calc((100vw - 67.5rem) / 2));
  box-sizing: border-box;
}

@media (min-width: 768px) {
  .home-business {
    padding-top: 4rem;
    padding-bottom: 4.5rem;
    padding-inline: max(1.5rem, calc((100vw - 67.5rem) / 2));
  }
}

.home-business__inner {
  display: flex;
  max-width: 67.5rem;
  min-height: 35rem;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 2.25rem;
  margin-left: auto;
  margin-right: auto;
  box-sizing: border-box;
  /* 与 Figma 类似：内容靠左上，与区域边缘留出间距 */
  padding: 1.5rem 1.5rem 2rem;
}

@media (max-width: 767px) {
  .home-business__inner {
    min-height: unset;
  }
}

.home-business__label {
  margin: 0;
  font-family: 'EB Garamond', 'Noto Sans SC', serif;
  font-size: 1.2rem;
  font-weight: 400;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: #000;
}

.home-business__body {
  display: flex;
  flex-direction: column;
  gap: 3.2rem;
  width: 100%;
}

@media (min-width: 768px) {
  .home-business__body {
    gap: 3.8rem;
  }

}

.home-business__para {
  margin: 0;
  font-family: 'EB Garamond', 'Noto Sans SC', serif;
  font-size: clamp(1.08rem, 2.4vw, 2.35rem);
  font-weight: 400;
  line-height: 1.4;
  letter-spacing: 0.005em;
  color: #000;
  text-align: justify;
  text-justify: inter-ideograph;
}

.home-business__accent {
  display: inline;
  font-style: normal;
  color: #ff5449;
  text-decoration: none;
  white-space: nowrap;
  transition: opacity 0.15s ease;
}

.home-business__accent:hover {
  opacity: 0.85;
}

.home-business__metric {
  font-family: Inter, 'Noto Sans SC', system-ui, sans-serif;
  font-size: clamp(1.75rem, 4.5vw, 4rem);
  font-weight: 500;
  font-style: normal;
  line-height: 1.1;
  letter-spacing: -0.03em;
  color: #000;
}
</style>
