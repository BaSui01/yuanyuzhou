/**
 * 核心工具函数
 */

import { STORAGE_KEYS } from './constants'

/**
 * 深度克隆对象
 * @param {any} obj - 要克隆的对象
 * @returns {any} 克隆后的对象
 */
export function deepClone(obj) {
  if (obj === null || typeof obj !== 'object') return obj
  if (obj instanceof Date) return new Date(obj.getTime())
  if (obj instanceof Array) return obj.map(item => deepClone(item))

  const clonedObj = {}
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      clonedObj[key] = deepClone(obj[key])
    }
  }
  return clonedObj
}

/**
 * 防抖函数
 * @param {Function} func - 要防抖的函数
 * @param {number} wait - 等待时间（毫秒）
 * @returns {Function} 防抖后的函数
 */
export function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

/**
 * 节流函数
 * @param {Function} func - 要节流的函数
 * @param {number} limit - 限制时间（毫秒）
 * @returns {Function} 节流后的函数
 */
export function throttle(func, limit) {
  let inThrottle
  return function() {
    const args = arguments
    const context = this
    if (!inThrottle) {
      func.apply(context, args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}

/**
 * 格式化日期
 * @param {Date|string|number} date - 日期
 * @param {string} format - 格式字符串
 * @returns {string} 格式化后的日期字符串
 */
export function formatDate(date, format = 'YYYY-MM-DD HH:mm:ss') {
  const d = new Date(date)
  if (isNaN(d.getTime())) return ''

  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hours = String(d.getHours()).padStart(2, '0')
  const minutes = String(d.getMinutes()).padStart(2, '0')
  const seconds = String(d.getSeconds()).padStart(2, '0')

  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds)
}

/**
 * 生成唯一ID
 * @param {string} prefix - 前缀
 * @returns {string} 唯一ID
 */
export function generateId(prefix = 'id') {
  return `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
}

/**
 * 存储工具
 */
export const storage = {
  /**
   * 设置存储项
   * @param {string} key - 键名
   * @param {any} value - 值
   * @param {string} type - 存储类型
   */
  set(key, value, type = 'localStorage') {
    try {
      const serializedValue = JSON.stringify(value)
      window[type].setItem(`metaverse_${key}`, serializedValue)
    } catch (error) {
      console.error('Storage set error:', error)
    }
  },

  /**
   * 获取存储项
   * @param {string} key - 键名
   * @param {any} defaultValue - 默认值
   * @param {string} type - 存储类型
   * @returns {any} 存储的值
   */
  get(key, defaultValue = null, type = 'localStorage') {
    try {
      const item = window[type].getItem(`metaverse_${key}`)
      return item ? JSON.parse(item) : defaultValue
    } catch (error) {
      console.error('Storage get error:', error)
      return defaultValue
    }
  },

  /**
   * 移除存储项
   * @param {string} key - 键名
   * @param {string} type - 存储类型
   */
  remove(key, type = 'localStorage') {
    try {
      window[type].removeItem(`metaverse_${key}`)
    } catch (error) {
      console.error('Storage remove error:', error)
    }
  },

  /**
   * 清空存储
   * @param {string} type - 存储类型
   */
  clear(type = 'localStorage') {
    try {
      window[type].clear()
    } catch (error) {
      console.error('Storage clear error:', error)
    }
  }
}

/**
 * URL 工具
 */
export const url = {
  /**
   * 解析查询参数
   * @param {string} search - 查询字符串
   * @returns {Object} 参数对象
   */
  parseQuery(search = window.location.search) {
    const params = new URLSearchParams(search)
    const result = {}
    for (const [key, value] of params) {
      result[key] = value
    }
    return result
  },

  /**
   * 构建查询字符串
   * @param {Object} params - 参数对象
   * @returns {string} 查询字符串
   */
  buildQuery(params) {
    const searchParams = new URLSearchParams()
    Object.keys(params).forEach(key => {
      if (params[key] !== null && params[key] !== undefined) {
        searchParams.append(key, params[key])
      }
    })
    return searchParams.toString()
  }
}

/**
 * 验证工具
 */
export const validate = {
  /**
   * 验证邮箱
   * @param {string} email - 邮箱地址
   * @returns {boolean} 是否有效
   */
  email(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return re.test(email)
  },

  /**
   * 验证手机号
   * @param {string} phone - 手机号
   * @returns {boolean} 是否有效
   */
  phone(phone) {
    const re = /^1[3-9]\d{9}$/
    return re.test(phone)
  },

  /**
   * 验证密码强度
   * @param {string} password - 密码
   * @returns {Object} 验证结果
   */
  password(password) {
    const result = {
      valid: false,
      strength: 'weak',
      errors: []
    }

    if (password.length < 8) {
      result.errors.push('密码长度至少8位')
    }
    if (!/[a-z]/.test(password)) {
      result.errors.push('密码需包含小写字母')
    }
    if (!/[A-Z]/.test(password)) {
      result.errors.push('密码需包含大写字母')
    }
    if (!/\d/.test(password)) {
      result.errors.push('密码需包含数字')
    }
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      result.errors.push('密码需包含特殊字符')
    }

    if (result.errors.length === 0) {
      result.valid = true
      result.strength = 'strong'
    } else if (result.errors.length <= 2) {
      result.strength = 'medium'
    }

    return result
  }
}

/**
 * 文件工具
 */
export const file = {
  /**
   * 格式化文件大小
   * @param {number} bytes - 字节数
   * @returns {string} 格式化后的大小
   */
  formatSize(bytes) {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  },

  /**
   * 获取文件扩展名
   * @param {string} filename - 文件名
   * @returns {string} 扩展名
   */
  getExtension(filename) {
    return filename.slice((filename.lastIndexOf('.') - 1 >>> 0) + 2)
  },

  /**
   * 检查文件类型
   * @param {File} file - 文件对象
   * @param {Array} allowedTypes - 允许的类型
   * @returns {boolean} 是否允许
   */
  checkType(file, allowedTypes) {
    return allowedTypes.includes(file.type)
  }
}
