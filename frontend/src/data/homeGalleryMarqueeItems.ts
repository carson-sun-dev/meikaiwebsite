/**
 * 图片来自 `src/source/homepage/3/`，文件名（不含扩展名）即轮播下方说明。
 * 当前按文件体积大致对应分辨率：最大的 4 张作「大」、最小的 4 张作「小」、中间 4 张作「中」；每组顺序 大→小→中。
 */
import img_zhongshi_keiting from '@/source/homepage/3/中式典雅客厅.jpg'
import img_zhongshi_canguan from '@/source/homepage/3/中式餐馆.jpg'
import img_xiuxian_huiyishi from '@/source/homepage/3/休闲会议室.jpg'
import img_fushi_dianpu from '@/source/homepage/3/复式店铺.jpg'
import img_jiaju_zoulang from '@/source/homepage/3/家居走廊.jpg'
import img_dianpu_datang from '@/source/homepage/3/店铺大堂.jpg'
import img_fenwei_menlang from '@/source/homepage/3/氛围门廊.jpg'
import img_qingxin_fenwei from '@/source/homepage/3/清新氛围.jpg'
import img_jianyue_qiantai from '@/source/homepage/3/简约前台.jpg'
import img_menmian_fangmentou from '@/source/homepage/3/门面房门头.jpg'
import img_canyin_baojian from '@/source/homepage/3/餐饮包间.jpg'
import img_gaoya_chahuashi from '@/source/homepage/3/高雅茶话室.jpg'

/** 单张在组内档位：大 / 中 / 小，形成错落层次 */
export type GalleryItemSize = 'large' | 'medium' | 'small'

/**
 * 可选视觉变体（仅「大」图常用）：
 * - `frame`：竖向矩形大图区（约 3:4，高大于宽）
 * - `tall`：竖长大图区（竖构图）
 */
export type GalleryItemVariant = 'default' | 'frame' | 'tall'

export interface HomeGallerySlideItem {
  id: string
  /** 图片地址：打包导入的模块或 `https://...` 字符串 */
  image: string
  /** 图片下方说明文字 */
  caption: string
  size: GalleryItemSize
  variant?: GalleryItemVariant
}

/**
 * 首页案例横向跑马灯数据。
 *
 * 无缝循环原理（配合 `home-page.css` 动画）：
 * 1. `HomeGalleryMarqueeStrip` 把本数组渲染两份首尾相接（整段序列复制一次）。
 * 2. 轨道总宽度为两倍内容；动画 `translate3d(0) → translate3d(-50%,0,0)` 恰好移动「一整份」宽度。
 * 3. 第二份与第一份开头一致，滚到接缝处时视觉上连续，避免跳回起点。
 * 4. `translate3d` + `backface-visibility` 尽量用合成层，减轻卡顿。
 * 速度：改 `.home-gallery__marquee-shell` 的 `--home-gallery-marquee-duration`。
 *
 * 自定义：换图则在顶部 import 静态资源并把 `image` 设为该模块，或 `image: 'https://...'`；改 `caption`；每连续 3 条为一组，顺序大→小→中，追加新组就加 3 条；`id` 全局唯一；仅大图需要 `variant: 'frame'`（竖向大图）或 `'tall'`（更窄的竖长）。条数非 3 的倍数时最后一组可不足 3 张。
 */
export const homeGalleryMarqueeItems: HomeGallerySlideItem[] = [
  /* 组 1：大(最大档) → 小 → 中 */
  { id: 'g1-1', image: img_qingxin_fenwei, caption: '清新氛围', size: 'large', variant: 'frame' },
  { id: 'g1-2', image: img_canyin_baojian, caption: '餐饮包间', size: 'small' },
  { id: 'g1-3', image: img_zhongshi_keiting, caption: '中式典雅客厅', size: 'medium' },
  /* 组 2 */
  { id: 'g2-1', image: img_zhongshi_canguan, caption: '中式餐馆', size: 'large', variant: 'frame' },
  { id: 'g2-2', image: img_fushi_dianpu, caption: '复式店铺', size: 'small' },
  { id: 'g2-3', image: img_jiaju_zoulang, caption: '家居走廊', size: 'medium' },
  /* 组 3 */
  { id: 'g3-1', image: img_menmian_fangmentou, caption: '门面房门头', size: 'large', variant: 'frame' },
  { id: 'g3-2', image: img_dianpu_datang, caption: '店铺大堂', size: 'small' },
  { id: 'g3-3', image: img_fenwei_menlang, caption: '氛围门廊', size: 'medium' },
  /* 组 4 */
  { id: 'g4-1', image: img_xiuxian_huiyishi, caption: '休闲会议室', size: 'large', variant: 'frame' },
  { id: 'g4-2', image: img_jianyue_qiantai, caption: '简约前台', size: 'small' },
  { id: 'g4-3', image: img_gaoya_chahuashi, caption: '高雅茶话室', size: 'medium' },
]
