/**
 * 全局常量定义
 */

// 应用状态常量
export const APP_STATES = {
  LOADING: 'loading',
  READY: 'ready',
  ERROR: 'error'
}

// 用户状态常量
export const USER_STATES = {
  GUEST: 'guest',
  AUTHENTICATED: 'authenticated',
  PENDING: 'pending',
  BANNED: 'banned'
}

// API 状态码
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  UNPROCESSABLE_ENTITY: 422,
  INTERNAL_SERVER_ERROR: 500
}

// 存储键名
export const STORAGE_KEYS = {
  TOKEN: 'auth_token',
  REFRESH_TOKEN: 'refresh_token',
  USER: 'user_info',
  PREFERENCES: 'user_preferences',
  THEME: 'app_theme',
  LANGUAGE: 'app_language'
}

// 事件名称
export const EVENTS = {
  AUTH_LOGIN: 'auth:login',
  AUTH_LOGOUT: 'auth:logout',
  AUTH_REFRESH: 'auth:refresh',
  USER_UPDATED: 'user:updated',
  NOTIFICATION_NEW: 'notification:new',
  CHAT_MESSAGE: 'chat:message',
  ERROR_OCCURRED: 'error:occurred'
}

// 路由名称常量
export const ROUTE_NAMES = {
  HOME: 'Home',
  DASHBOARD: 'Dashboard',
  LOGIN: 'Login',
  REGISTER: 'Register',
  PROFILE: 'Profile',
  SETTINGS: 'Settings',
  AI_CHAT: 'AIChat',
  AI_COMPANION: 'AICompanion',
  METAVERSE: 'Metaverse',
  FRIENDS: 'Friends'
}

// AI 模型类型
export const AI_MODELS = {
  CHAT: 'chat',
  COMPANION: 'companion',
  IMAGE_ANALYSIS: 'image_analysis',
  VOICE_LAB: 'voice_lab'
}

// 元宇宙空间类型
export const METAVERSE_SPACES = {
  PUBLIC: 'public',
  PRIVATE: 'private',
  SHARED: 'shared',
  PREMIUM: 'premium'
}

// 消息类型
export const MESSAGE_TYPES = {
  TEXT: 'text',
  IMAGE: 'image',
  VOICE: 'voice',
  VIDEO: 'video',
  FILE: 'file',
  SYSTEM: 'system'
}

// 通知类型
export const NOTIFICATION_TYPES = {
  INFO: 'info',
  SUCCESS: 'success',
  WARNING: 'warning',
  ERROR: 'error'
}
