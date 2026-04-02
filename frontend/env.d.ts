/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** 生产环境若前后端不同域，填 API 根地址（无末尾 /），空则用相对路径 /api */
  readonly VITE_API_BASE?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
