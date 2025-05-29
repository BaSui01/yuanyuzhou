/**
 * 路由守卫
 */

import { useAuthStore } from '@/stores/auth'
import { ROUTE_NAMES, STORAGE_KEYS } from '../core/constants'
import { storage } from '../core/utils'

/**
 * 认证守卫
 * @param {Object} to - 目标路由
 * @param {Object} from - 来源路由
 * @param {Function} next - 下一步函数
 */
export function authGuard(to, from, next) {
  const authStore = useAuthStore()
  const token = storage.get(STORAGE_KEYS.TOKEN)

  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    if (!token || !authStore.isAuthenticated) {
      // 保存当前尝试访问的路由，登录后重定向
      storage.set('redirectAfterLogin', to.fullPath)
      next({ name: ROUTE_NAMES.LOGIN })
      return
    }
  }

  // 如果已登录用户访问登录页，重定向到仪表板
  if (to.name === ROUTE_NAMES.LOGIN && token && authStore.isAuthenticated) {
    next({ name: ROUTE_NAMES.DASHBOARD })
    return
  }

  next()
}

/**
 * 管理员权限守卫
 * @param {Object} to - 目标路由
 * @param {Object} from - 来源路由
 * @param {Function} next - 下一步函数
 */
export function adminGuard(to, from, next) {
  const authStore = useAuthStore()

  if (to.meta.requiresAdmin) {
    if (!authStore.isAdmin) {
      next({ name: 'Forbidden' })
      return
    }
  }

  next()
}

/**
 * 权限守卫
 * @param {Object} to - 目标路由
 * @param {Object} from - 来源路由
 * @param {Function} next - 下一步函数
 */
export function permissionGuard(to, from, next) {
  const authStore = useAuthStore()

  if (to.meta.permissions && to.meta.permissions.length > 0) {
    const hasPermission = to.meta.permissions.some(permission =>
      authStore.hasPermission(permission)
    )

    if (!hasPermission) {
      next({ name: 'Forbidden' })
      return
    }
  }

  next()
}

/**
 * 页面标题守卫
 * @param {Object} to - 目标路由
 */
export function titleGuard(to) {
  // 设置页面标题
  if (to.meta && to.meta.title) {
    document.title = `${to.meta.title} - 元宇宙社交平台`
  } else {
    document.title = '元宇宙社交平台'
  }
}

/**
 * 进度条守卫
 */
export function progressGuard() {
  // 这里可以集成 NProgress 或其他进度条库
  // NProgress.start()
}

/**
 * 页面加载完成守卫
 */
export function loadingCompleteGuard() {
  // 页面加载完成后的处理
  // NProgress.done()
}

/**
 * 设置路由守卫
 * @param {Object} router - 路由实例
 */
export function setupRouterGuards(router) {
  // 全局前置守卫
  router.beforeEach(async (to, from, next) => {
    // 开始进度条
    progressGuard()

    // 认证守卫
    authGuard(to, from, (nextRoute) => {
      if (nextRoute) {
        next(nextRoute)
        return
      }

      // 管理员权限守卫
      adminGuard(to, from, (nextRoute) => {
        if (nextRoute) {
          next(nextRoute)
          return
        }

        // 权限守卫
        permissionGuard(to, from, next)
      })
    })
  })

  // 全局解析守卫
  router.beforeResolve((to, from, next) => {
    // 在导航被确认之前，同时在所有组件内守卫和异步路由组件被解析之后调用
    next()
  })

  // 全局后置钩子
  router.afterEach((to, from) => {
    // 设置页面标题
    titleGuard(to)

    // 完成进度条
    loadingCompleteGuard()

    // 记录路由变化（用于分析）
    if (window.gtag) {
      window.gtag('config', 'GA_TRACKING_ID', {
        page_path: to.path
      })
    }
  })

  // 路由错误处理
  router.onError((error) => {
    console.error('路由错误:', error)

    // 这里可以添加错误上报逻辑
    // errorReporter.report(error)
  })
}

/**
 * 路由守卫工具
 */
export const guardUtils = {
  /**
   * 检查用户是否有权限访问路由
   * @param {Object} route - 路由对象
   * @param {Object} user - 用户对象
   * @returns {boolean} 是否有权限
   */
  canAccess(route, user) {
    if (route.meta.requiresAuth && !user) {
      return false
    }

    if (route.meta.requiresAdmin && !user?.isAdmin) {
      return false
    }

    if (route.meta.permissions && route.meta.permissions.length > 0) {
      return route.meta.permissions.some(permission =>
        user?.permissions?.includes(permission)
      )
    }

    return true
  },

  /**
   * 获取重定向路由
   * @param {Object} user - 用户对象
   * @returns {string} 重定向路由名称
   */
  getRedirectRoute(user) {
    if (!user) {
      return ROUTE_NAMES.LOGIN
    }

    if (user.isAdmin) {
      return 'AdminDashboard'
    }

    return ROUTE_NAMES.DASHBOARD
  }
}
