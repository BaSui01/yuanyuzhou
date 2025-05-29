/**
 * 管理后台 API 模块入口
 */
import { auth } from './auth'
import { dashboard } from './dashboard'
import { users } from './users'
import { analytics } from './analytics'
import { settings } from './settings'

// 导出所有 API 模块
export { auth, dashboard, users, analytics, settings }

// 默认导出
export default {
  auth,
  dashboard,
  users,
  analytics,
  settings
}
