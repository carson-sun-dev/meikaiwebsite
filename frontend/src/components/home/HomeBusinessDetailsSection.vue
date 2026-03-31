<template>
  <section class="home-business">
    <div class="home-business__inner">
      <h2 class="home-business__label">业务细节</h2>
      <div class="home-business__body">
        <p class="home-business__para">
          我们专注于<span class="home-business__accent">精品店铺</span>装修，至今已成功交付超过
          <span class="home-business__metric">120+</span>
          个项目
        </p>
        <p class="home-business__para">
          同时致力于为企业提供<span class="home-business__accent">办公装修</span>解决方案，已完成
          <span class="home-business__metric">30+</span>
          处高标准商务办公项目。
        </p>
        <p class="home-business__para">
          美恺从<span class="home-business__accent">家装</span>起家，我们始终将客户置于首位，为
          <span class="home-business__metric">200+</span>
          个家庭定制了梦想之家。
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
  padding-inline: max(1.5rem, calc((100vw - 67.5rem) / 2));
  box-sizing: border-box;
}

@media (min-width: 768px) {
  .home-business {
    padding-top: 4rem;
    padding-bottom: 4.5rem;
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
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: #000;
}

.home-business__body {
  display: flex;
  flex-direction: column;
  gap: 2.75rem;
  width: 100%;
}

@media (min-width: 768px) {
  .home-business__body {
    gap: 3.25rem;
  }
}

.home-business__para {
  margin: 0;
  font-family: 'EB Garamond', 'Noto Sans SC', serif;
  font-size: clamp(1.25rem, 3.2vw, 3rem);
  font-weight: 400;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: #000;
}

.home-business__accent {
  font-style: normal;
  color: #2977ed;
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
