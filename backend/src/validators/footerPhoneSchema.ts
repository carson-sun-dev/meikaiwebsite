import { z } from 'zod'

import { validatePhone } from './phone.js'

export const footerPhoneBodySchema = z.object({
  phone: z
    .string()
    .trim()
    .min(5, '请填写联系电话')
    .max(32)
    .refine(validatePhone, '无效的手机号或电话格式'),
})

export type FooterPhoneBody = z.infer<typeof footerPhoneBodySchema>
