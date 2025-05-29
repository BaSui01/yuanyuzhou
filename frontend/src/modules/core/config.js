/**
 * 核心配置
 */

// 应用配置
export const APP_CONFIG = {
  name: '元宇宙社交平台',
  version: '1.0.0',
  description: 'AI驱动的元宇宙社交体验平台',
  env: import.meta.env.MODE,
  isDev: import.meta.env.DEV,
  isProd: import.meta.env.PROD
}

// API 配置
export const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 30000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
}

// 路由配置
export const ROUTER_CONFIG = {
  mode: 'history',
  base: import.meta.env.BASE_URL,
  scrollBehavior: 'smooth'
}

// 存储配置
export const STORAGE_CONFIG = {
  prefix: 'metaverse_',
  type: 'localStorage' // localStorage | sessionStorage
}

// 加密配置
export const CRYPTO_CONFIG = {
  defaultLevel: 2,
  enabled: true
}

// 默认导出所有配置
export default {
  app: APP_CONFIG,
  api: API_CONFIG,
  router: ROUTER_CONFIG,
  storage: STORAGE_CONFIG,
  crypto: CRYPTO_CONFIG
}
