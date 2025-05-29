/**
 * 测试模块统一导出
 */

// 导出 Mock 服务
export { default as mockService } from './mocks'

// 导出测试工具
export * from './utils'

// 导出测试数据
export * from './fixtures'

// 导出浏览器 Mock
export { worker } from './mocks/browser'

// 导出服务器 Mock
export { server } from './mocks/server'

// 默认导出
export default {
  mocks: () => import('./mocks'),
  utils: () => import('./utils'),
  fixtures: () => import('./fixtures')
}
