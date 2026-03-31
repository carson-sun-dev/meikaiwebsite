<template>
  <svg
    class="paper-plane-icon"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    aria-hidden="true"
  >
    <!-- 路径在 24×24 内重心偏左下，先平移到视口中心再旋转，便于在圆按钮内光学居中 -->
    <g class="paper-plane-icon__g" transform="translate(12 12) rotate(-45) translate(-12 -12)">
      <path
        fill="currentColor"
        transform="translate(1.25 -1.25)"
        d="M2.01 21.49 23 12 2.01 2.51v7.98l15.01 1.51L2.01 13.5v7.99Z"
      />
    </g>
  </svg>
</template>

<style scoped>
.paper-plane-icon {
  display: block;
  flex-shrink: 0;
  width: 100%;
  height: 100%;
}
</style>
