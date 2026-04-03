import { z } from 'zod'

/** 与前端 ContactQuoteForm 店铺类型 option value 保持一致 */
export const storeTypeKeys = [
  'food',
  'retail',
  'entertainment',
  'fitness',
  'milk-tea',
  'other',
] as const

/** 特殊设备多选 value */
export const specialDeviceKeys = [
  'high-power',
  'water-elec',
  'ac',
  'cctv',
  'fire-safety',
  'other',
] as const

/** 家装地板/墙面多选 value */
export const resFloorWallKeys = [
  'wood-floor',
  'composite-floor',
  'tile',
  'panel',
  'art-paint',
  'wallpaper',
  'other',
] as const

export const storeTypeSchema = z
  .union([z.literal(''), z.enum(storeTypeKeys)])
  .default('')

export const specialDevicesSchema = z.array(z.enum(specialDeviceKeys)).max(32).default([])

export const resFloorWallSchema = z.array(z.enum(resFloorWallKeys)).max(32).default([])
