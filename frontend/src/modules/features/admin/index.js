/**
 * 管理后台功能模块
 */
import * as adminAPI from './api'
import * as adminComposables from './composables'

// 导出 API 和 Composables
export { adminAPI, adminComposables }

// 默认导出
export default {
  install(app) {
    // 注册全局组件或指令

    // 注册全局属性
    app.config.globalProperties.$adminAPI = adminAPI

    console.log('管理后台功能模块已安装')
  }
}
