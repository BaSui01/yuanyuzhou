/**
 * Vue Router 配置
 */

import { createRouter, createWebHistory } from 'vue-router'
import { routes } from '@/modules/navigation/routes'
import { setupRouterGuards } from '@/modules/navigation/guards'
import { ROUTER_CONFIG } from '../core/config'

/**
 * 创建路由实例
 */
const router = createRouter({
  history: createWebHistory(ROUTER_CONFIG.base),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 如果有保存的位置（浏览器后退/前进）
    if (savedPosition) {
      return savedPosition
    }

    // 如果路由有锚点
    if (to.hash) {
      return {
        el: to.hash,
        behavior: ROUTER_CONFIG.scrollBehavior
      }
    }

    // 默认滚动到顶部
    return { top: 0, behavior: ROUTER_CONFIG.scrollBehavior }
  }
})

/**
 * 设置路由守卫
 */
setupRouterGuards(router)

/**
 * 路由工具方法
 */
export const routerUtils = {
  /**
   * 获取当前路由
   */
  getCurrentRoute: () => router.currentRoute.value,

  /**
   * 编程式导航
   * @param {string|Object} to - 目标路由
   * @param {Object} options - 选项
   */
  navigate: (to, options = {}) => {
    if (options.replace) {
      return router.replace(to)
    }
    return router.push(to)
  },

  /**
   * 后退
   * @param {number} steps - 后退步数
   */
  back: (steps = 1) => {
    router.go(-steps)
  },

  /**
   * 前进
   * @param {number} steps - 前进步数
   */
  forward: (steps = 1) => {
    router.go(steps)
  },

  /**
   * 检查路由是否存在
   * @param {string} name - 路由名称
   */
  hasRoute: (name) => {
    return router.hasRoute(name)
  },

  /**
   * 获取路由匹配记录
   * @param {string} name - 路由名称
   */
  getRoutes: () => {
    return router.getRoutes()
  },

  /**
   * 动态添加路由
   * @param {Object} route - 路由配置
   */
  addRoute: (route) => {
    router.addRoute(route)
  },

  /**
   * 动态移除路由
   * @param {string} name - 路由名称
   */
  removeRoute: (name) => {
    router.removeRoute(name)
  },

  /**
   * 解析路由
   * @param {string|Object} to - 路由
   */
  resolve: (to) => {
    return router.resolve(to)
  }
}

export { router }
export default router
