/**
 * 模块系统主入口文件
 *
 * 重构后的模块结构：
 * ├── core/           # 核心模块（配置、常量、工具函数）
 * ├── http/           # HTTP 客户端（API 请求、加密等）
 * ├── navigation/     # 导航模块（路由、守卫）
 * ├── features/       # 功能模块（AI、用户、元宇宙等）
 * ├── testing/        # 测试模块（Mock、工具等）
 * └── setup/          # 应用设置（初始化、插件等）
 */

// 核心模块
export * as core from './core'
export { default as config } from './core/config'
export * as constants from './core/constants'
export * as utils from './core/utils'

// HTTP 模块
export * as http from './http'
export { default as api } from './http/api'
export { request } from './http/request'

// 导航模块
export * as navigation from './navigation'
export { default as router } from './navigation/router'
export { routes } from './navigation/routes'

// 功能模块
export * as features from './features'
export * as ai from './features/ai'
export * as user from './features/user'
export * as metaverse from './features/metaverse'

// 测试模块
export * as testing from './testing'

// 设置模块
export * as setup from './setup'

/**
 * 模块注册器
 */
class ModuleRegistry {
  constructor() {
    this.modules = new Map()
    this.initialized = false
  }

  /**
   * 注册模块
   * @param {string} name - 模块名称
   * @param {Object} module - 模块对象
   */
  register(name, module) {
    this.modules.set(name, module)
  }

  /**
   * 获取模块
   * @param {string} name - 模块名称
   * @returns {Object} 模块对象
   */
  get(name) {
    return this.modules.get(name)
  }

  /**
   * 检查模块是否存在
   * @param {string} name - 模块名称
   * @returns {boolean} 是否存在
   */
  has(name) {
    return this.modules.has(name)
  }

  /**
   * 获取所有模块
   * @returns {Array} 模块数组
   */
  getAll() {
    return Array.from(this.modules.entries())
  }

  /**
   * 初始化所有模块
   */
  async initialize() {
    if (this.initialized) return

    try {
      // 并行初始化所有模块
      const initPromises = Array.from(this.modules.values())
        .filter(module => typeof module.init === 'function')
        .map(module => module.init())

      await Promise.all(initPromises)
      this.initialized = true
      console.log('所有模块初始化完成')
    } catch (error) {
      console.error('模块初始化失败:', error)
      throw error
    }
  }
}

// 创建全局模块注册器
export const moduleRegistry = new ModuleRegistry()

// 注册所有模块
const registerModules = async () => {
  // 注册核心模块
  moduleRegistry.register('core', await import('./core'))

  // 注册 HTTP 模块
  moduleRegistry.register('http', await import('./http'))

  // 注册导航模块
  moduleRegistry.register('navigation', await import('./navigation'))

  // 注册功能模块
  moduleRegistry.register('features', await import('./features'))

  // 注册测试模块
  if (import.meta.env.DEV) {
    moduleRegistry.register('testing', await import('./testing'))
  }

  // 注册设置模块
  moduleRegistry.register('setup', await import('./setup'))
}

/**
 * 初始化模块系统
 */
export const initModules = async () => {
  try {
    await registerModules()
    await moduleRegistry.initialize()
    return moduleRegistry
  } catch (error) {
    console.error('模块系统初始化失败:', error)
    throw error
  }
}

// 默认导出
export default {
  // 模块
  core: () => import('./core'),
  http: () => import('./http'),
  navigation: () => import('./navigation'),
  features: () => import('./features'),
  testing: () => import('./testing'),
  setup: () => import('./setup'),

  // 注册器
  registry: moduleRegistry,

  // 初始化
  init: initModules
}
