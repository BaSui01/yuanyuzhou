/**
 * 应用设置模块
 */

// 导出应用初始化
export { default as initApp } from './init'

// 导出配置设置
export { default as setupConfig } from './config'

// 导出插件设置
export { default as setupPlugins } from './plugins'

// 导出服务设置
export { default as setupServices } from './services'

// 导出开发工具设置
export { default as setupDevtools } from './devtools'

// 默认导出
export default {
  init: () => import('./init'),
  config: () => import('./config'),
  plugins: () => import('./plugins'),
  services: () => import('./services'),
  devtools: () => import('./devtools')
}
