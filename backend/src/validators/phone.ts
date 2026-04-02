/** 与前端 phoneValidation.ts 一致 */
export function validatePhone(v: string): boolean {
  const s = v.replace(/\s+/g, '')
  return /^[+]?(\d){5,15}$/.test(s) || /^0\d{5,14}$/.test(s)
}
