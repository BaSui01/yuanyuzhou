/**
 * 认证相关常量
 */

// 本地存储键名
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  USER_DATA: 'user_data',
  REMEMBER_ME: 'remember_me',
  LAST_LOGIN: 'last_login'
}

// 认证状态
export const AUTH_STATUS = {
  AUTHENTICATED: 'authenticated',
  UNAUTHENTICATED: 'unauthenticated',
  PENDING: 'pending',
  EXPIRED: 'expired'
}

// 用户角色
export const USER_ROLES = {
  ADMIN: 'admin',
  USER: 'user',
  MODERATOR: 'moderator',
  VIP: 'vip'
}

// 登录方式
export const LOGIN_TYPES = {
  EMAIL: 'email',
  USERNAME: 'username',
  PHONE: 'phone',
  SOCIAL: 'social'
}

// 社交登录提供商
export const SOCIAL_PROVIDERS = {
  GOOGLE: 'google',
  GITHUB: 'github',
  WECHAT: 'wechat',
  QQ: 'qq',
  WEIBO: 'weibo'
}

// 验证状态
export const VERIFICATION_STATUS = {
  PENDING: 'pending',
  VERIFIED: 'verified',
  EXPIRED: 'expired',
  FAILED: 'failed'
}

// 密码强度等级
export const PASSWORD_STRENGTH = {
  WEAK: 1,
  MEDIUM: 2,
  STRONG: 3
}

// 错误代码
export const AUTH_ERROR_CODES = {
  INVALID_CREDENTIALS: 'INVALID_CREDENTIALS',
  ACCOUNT_DISABLED: 'ACCOUNT_DISABLED',
  EMAIL_NOT_VERIFIED: 'EMAIL_NOT_VERIFIED',
  TOKEN_EXPIRED: 'TOKEN_EXPIRED',
  CAPTCHA_INVALID: 'CAPTCHA_INVALID',
  RATE_LIMITED: 'RATE_LIMITED',
  USER_EXISTS: 'USER_EXISTS',
  EMAIL_EXISTS: 'EMAIL_EXISTS'
}

// 默认配置
export const DEFAULT_CONFIG = {
  // Token 过期时间（毫秒）
  TOKEN_EXPIRY: 24 * 60 * 60 * 1000, // 24小时

  // 记住我过期时间（毫秒）
  REMEMBER_ME_EXPIRY: 30 * 24 * 60 * 60 * 1000, // 30天

  // 验证码刷新间隔（毫秒）
  CAPTCHA_REFRESH_INTERVAL: 60 * 1000, // 1分钟

  // 自动登录检查间隔（毫秒）
  AUTO_LOGIN_CHECK_INTERVAL: 10 * 60 * 1000, // 10分钟

  // 密码最小长度
  MIN_PASSWORD_LENGTH: 8,

  // 密码最大长度
  MAX_PASSWORD_LENGTH: 128,

  // 用户名最小长度
  MIN_USERNAME_LENGTH: 3,

  // 用户名最大长度
  MAX_USERNAME_LENGTH: 20
}

export const authConstants = {
  STORAGE_KEYS,
  AUTH_STATUS,
  USER_ROLES,
  LOGIN_TYPES,
  SOCIAL_PROVIDERS,
  VERIFICATION_STATUS,
  PASSWORD_STRENGTH,
  AUTH_ERROR_CODES,
  DEFAULT_CONFIG
}
