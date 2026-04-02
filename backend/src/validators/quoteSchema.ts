import { z } from 'zod'

import { validatePhone } from './phone.js'

const commonSchema = z.object({
  buildingType: z.string().min(1).max(64),
  schedule: z.string().min(1).max(64),
})

const contactSchema = z
  .object({
    gender: z.enum(['mr', 'ms']),
    lastName: z.string().trim().min(1).max(32),
    phone: z.string().trim().min(5).max(32),
    remark: z.string().max(4000).optional().default(''),
  })
  .strict()
  .superRefine((val, ctx) => {
    if (!validatePhone(val.phone)) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        path: ['phone'],
        message: '无效的手机号或电话格式',
      })
    }
  })

const stringArray = (maxLen: number, maxItems: number) =>
  z.array(z.string().min(1).max(maxLen)).max(maxItems).default([])

const storeSchema = z
  .object({
    storeType: z.string().max(64).default(''),
    shopArea: z.string().min(1, '请选择门店面积').max(64),
    backArea: z.string().max(64).default(''),
    doorSignNeeds: stringArray(48, 32),
    specialDevices: stringArray(48, 32),
    licenseAssist: z.string().max(64).default(''),
  })
  .strict()

const businessSchema = z
  .object({
    businessSeatArea: z.string().min(1, '请选择工程面积').max(64),
    businessOfficeCount: z.string().max(32).default(''),
    businessMeetingCount: z.string().max(32).default(''),
    businessFuncZones: stringArray(48, 32),
    businessSoundproof: z.string().max(32).default(''),
    businessWeakElectrics: stringArray(48, 32),
    businessAcType: z.string().max(64).default(''),
    businessFurnitureCustomized: z.string().max(32).default(''),
  })
  .strict()

const residentialSchema = z
  .object({
    resHomeArea: z.string().min(1, '请选择房屋面积').max(64),
    resBedroomCount: z.string().max(32).default(''),
    resBathroomCount: z.string().max(32).default(''),
    resLivingRoomCount: z.string().max(32).default(''),
    resDiningRoomCount: z.string().max(32).default(''),
    resKeyAreas: stringArray(48, 32),
    resIslandNeed: z.string().max(32).default(''),
    resFloorWall: stringArray(48, 32),
    resStorage: stringArray(48, 32),
    resSmartHome: stringArray(48, 32),
  })
  .strict()

export const quotePayloadSchema = z.discriminatedUnion('planKey', [
  z
    .object({
      planKey: z.literal('store'),
      common: commonSchema,
      store: storeSchema,
      contact: contactSchema,
    })
    .strict(),
  z
    .object({
      planKey: z.literal('business'),
      common: commonSchema,
      business: businessSchema,
      contact: contactSchema,
    })
    .strict(),
  z
    .object({
      planKey: z.literal('residential'),
      common: commonSchema,
      residential: residentialSchema,
      contact: contactSchema,
    })
    .strict(),
])

export type QuotePayload = z.infer<typeof quotePayloadSchema>
