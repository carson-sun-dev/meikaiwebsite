/** 与联系页报价表单一致：允许 +86 / 空格的 5~15 位数字或 0 开头的固话格式 */
export function validatePhone(v: string) {
  return /^[+]?(\d){5,15}$/.test(v.replace(/\s+/g, '')) || /^0\d{5,14}$/.test(v)
}
