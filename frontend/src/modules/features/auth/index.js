/**
 * 认证功能模块
 * 提供登录、注册、密码重置等认证相关功能
 */

// API 服务
export { authAPI } from './api/authService.js'

// Composables
export { useAuth } from './composables/useAuth.js'
export { useCaptcha } from './composables/useCaptcha.js'
export { useAuthValidation } from './composables/useAuthValidation.js'

// 工具函数
export { authUtils } from './utils/authUtils.js'

// 常量
export { authConstants } from './constants/authConstants.js'
