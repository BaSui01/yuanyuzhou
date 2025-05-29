/**
 * 导航模块统一导出
 */

// 导出路由
export { default as router } from './router'

// 导出路由配置
export { routes } from './routes'

// 导出路由守卫
export * from './guards'

// 导出导航工具
export * from './utils'

// 默认导出
export default {
  router: () => import('./router'),
  routes: () => import('./routes').then(m => m.routes),
  guards: () => import('./guards')
}
