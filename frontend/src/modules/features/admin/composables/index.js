/**
 * 管理后台 composables 入口
 */
import { useAdminAuth } from './useAdminAuth'
import { useAdminUsers } from './useAdminUsers'
import { useAdminDashboard } from './useAdminDashboard'
import { useAdminAnalytics } from './useAdminAnalytics'
import { useAdminSettings } from './useAdminSettings'

// 导出所有 composables
export {
  useAdminAuth,
  useAdminUsers,
  useAdminDashboard,
  useAdminAnalytics,
  useAdminSettings
}
