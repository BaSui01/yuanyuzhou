import { authConstants } from '../constants/authConstants.js'

/**
 * 认证相关工具函数
 */

/**
 * 格式化错误消息
 * @param {Object} error - 错误对象
 * @returns {string} 格式化后的错误消息
 */
const formatErrorMessage = (error) => {
  if (typeof error === 'string') {
    return error
  }

  if (error?.response?.data?.message) {
    return error.response.data.message
  }

  if (error?.response?.data?.error) {
    return error.response.data.error
  }

  if (error?.message) {
    return error.message
  }

  return '操作失败，请重试'
}

/**
 * 检查密码强度
 * @param {string} password - 密码
 * @returns {Object} 密码强度信息
 */
const checkPasswordStrength = (password) => {
  if (!password) {
    return {
      level: 0,
      text: '请输入密码',
      color: 'gray',
      score: 0
    }
  }

  let score = 0
  const checks = {
    length: password.length >= 8,
    lowercase: /[a-z]/.test(password),
    uppercase: /[A-Z]/.test(password),
    numbers: /\d/.test(password),
    special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
  }

  // 计算得分
  Object.values(checks).forEach(check => {
    if (check) score++
  })

  // 额外长度奖励
  if (password.length >= 12) score++

  let level, text, color
  if (score <= 2) {
    level = authConstants.PASSWORD_STRENGTH.WEAK
    text = '弱'
    color = 'red'
  } else if (score <= 4) {
    level = authConstants.PASSWORD_STRENGTH.MEDIUM
    text = '中'
    color = 'orange'
  } else {
    level = authConstants.PASSWORD_STRENGTH.STRONG
    text = '强'
    color = 'green'
  }

  return { level, text, color, score, checks }
}

/**
 * 验证邮箱格式
 * @param {string} email - 邮箱地址
 * @returns {boolean} 是否有效
 */
const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * 验证用户名格式
 * @param {string} username - 用户名
 * @returns {boolean} 是否有效
 */
const isValidUsername = (username) => {
  const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/
  return usernameRegex.test(username)
}

/**
 * 验证密码格式
 * @param {string} password - 密码
 * @returns {boolean} 是否有效
 */
const isValidPassword = (password) => {
  return password && password.length >= authConstants.DEFAULT_CONFIG.MIN_PASSWORD_LENGTH
}

/**
 * 生成随机字符串
 * @param {number} length - 字符串长度
 * @returns {string} 随机字符串
 */
const generateRandomString = (length = 32) => {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let result = ''
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return result
}

/**
 * 获取存储的认证信息
 * @returns {Object} 认证信息
 */
const getStoredAuth = () => {
  try {
    const token = localStorage.getItem(authConstants.STORAGE_KEYS.AUTH_TOKEN)
    const userData = localStorage.getItem(authConstants.STORAGE_KEYS.USER_DATA)

    return {
      token,
      user: userData ? JSON.parse(userData) : null
    }
  } catch (error) {
    console.error('获取存储的认证信息失败:', error)
    return { token: null, user: null }
  }
}

/**
 * 清除存储的认证信息
 */
const clearStoredAuth = () => {
  try {
    localStorage.removeItem(authConstants.STORAGE_KEYS.AUTH_TOKEN)
    localStorage.removeItem(authConstants.STORAGE_KEYS.USER_DATA)
    localStorage.removeItem(authConstants.STORAGE_KEYS.REMEMBER_ME)
    localStorage.removeItem(authConstants.STORAGE_KEYS.LAST_LOGIN)
  } catch (error) {
    console.error('清除存储的认证信息失败:', error)
  }
}

/**
 * 保存认证信息
 * @param {string} token - 认证令牌
 * @param {Object} user - 用户信息
 * @param {boolean} rememberMe - 是否记住我
 */
const saveAuth = (token, user, rememberMe = false) => {
  try {
    localStorage.setItem(authConstants.STORAGE_KEYS.AUTH_TOKEN, token)
    localStorage.setItem(authConstants.STORAGE_KEYS.USER_DATA, JSON.stringify(user))
    localStorage.setItem(authConstants.STORAGE_KEYS.LAST_LOGIN, new Date().toISOString())

    if (rememberMe) {
      localStorage.setItem(authConstants.STORAGE_KEYS.REMEMBER_ME, 'true')
    }
  } catch (error) {
    console.error('保存认证信息失败:', error)
  }
}

/**
 * 检查 token 是否过期
 * @param {string} token - JWT token
 * @returns {boolean} 是否过期
 */
const isTokenExpired = (token) => {
  if (!token) return true

  try {
    // 解析 JWT token
    const payload = JSON.parse(atob(token.split('.')[1]))
    const currentTime = Date.now() / 1000

    return payload.exp < currentTime
  } catch (error) {
    console.error('解析 token 失败:', error)
    return true
  }
}

/**
 * 获取用户角色权限
 * @param {Object} user - 用户对象
 * @returns {Array} 权限列表
 */
const getUserPermissions = (user) => {
  if (!user) return []

  // 管理员拥有所有权限
  if (user.role === authConstants.USER_ROLES.ADMIN || user.is_admin) {
    return ['*']
  }

  return user.permissions || []
}

/**
 * 检查用户是否有指定权限
 * @param {Object} user - 用户对象
 * @param {string} permission - 权限名称
 * @returns {boolean} 是否有权限
 */
const hasPermission = (user, permission) => {
  const permissions = getUserPermissions(user)

  // 管理员或拥有所有权限
  if (permissions.includes('*')) {
    return true
  }

  return permissions.includes(permission)
}

/**
 * 格式化用户显示名称
 * @param {Object} user - 用户对象
 * @returns {string} 显示名称
 */
const formatUserDisplayName = (user) => {
  if (!user) return '未知用户'

  return user.display_name || user.name || user.username || user.email || '未知用户'
}

/**
 * 获取用户头像 URL
 * @param {Object} user - 用户对象
 * @returns {string} 头像 URL
 */
const getUserAvatarUrl = (user) => {
  if (!user) return '/default-avatar.png'

  return user.avatar || user.avatar_url || '/default-avatar.png'
}

/**
 * 验证重置令牌格式
 * @param {string} token - 重置令牌
 * @returns {boolean} 是否有效
 */
const isValidResetToken = (token) => {
  // 重置令牌通常是一个长字符串
  return token && typeof token === 'string' && token.length >= 32
}

/**
 * 获取社交登录 URL
 * @param {string} provider - 提供商名称
 * @param {string} redirectUrl - 重定向 URL
 * @returns {string} 登录 URL
 */
const getSocialLoginUrl = (provider, redirectUrl = window.location.origin) => {
  const baseUrl = import.meta.env.VITE_API_BASE_URL || '/api'
  return `${baseUrl}/auth/social/${provider}?redirect_url=${encodeURIComponent(redirectUrl)}`
}

export const authUtils = {
  formatErrorMessage,
  checkPasswordStrength,
  isValidEmail,
  isValidUsername,
  isValidPassword,
  generateRandomString,
  getStoredAuth,
  clearStoredAuth,
  saveAuth,
  isTokenExpired,
  getUserPermissions,
  hasPermission,
  formatUserDisplayName,
  getUserAvatarUrl,
  isValidResetToken,
  getSocialLoginUrl
}
