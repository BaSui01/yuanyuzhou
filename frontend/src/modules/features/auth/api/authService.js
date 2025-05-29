import secureAxios from '@/modules/http/secureAxios'

/**
 * 认证服务 API
 * 基于 Django REST Framework 的认证后端
 */
export const authAPI = {
  /**
   * 用户登录
   * @param {Object} credentials - 登录凭据
   * @param {string} credentials.email - 邮箱
   * @param {string} credentials.password - 密码
   * @param {string} credentials.captcha - 验证码
   * @param {boolean} credentials.remember_me - 记住我
   */
  login: (credentials) => {
    return secureAxios.post('/api/auth/login/', {
      username: credentials.email, // 后端使用 username 字段
      password: credentials.password,
      captcha: credentials.captcha,
      remember_me: credentials.remember_me || false
    })
  },

  /**
   * 用户注册
   * @param {Object} userData - 注册数据
   * @param {string} userData.username - 用户名
   * @param {string} userData.email - 邮箱
   * @param {string} userData.password - 密码
   * @param {string} userData.confirmPassword - 确认密码
   * @param {string} userData.captcha - 验证码
   */
  register: (userData) => {
    return secureAxios.post('/api/auth/register/', {
      username: userData.username,
      email: userData.email,
      password: userData.password,
      password_confirmation: userData.confirmPassword,
      captcha: userData.captcha
    })
  },

  /**
   * 用户登出
   * @param {boolean} logoutAll - 是否登出所有设备
   */
  logout: (logoutAll = false) => {
    return secureAxios.post('/api/auth/logout/', {
      logout_all: logoutAll
    })
  },

  /**
   * 获取当前用户信息
   */
  me: () => {
    return secureAxios.get('/api/auth/status/')
  },

  /**
   * 忘记密码
   * @param {Object} data - 忘记密码数据
   * @param {string} data.email - 邮箱
   * @param {string} data.captcha - 验证码
   */
  forgotPassword: (data) => {
    return secureAxios.post('/api/auth/password-reset-request/', {
      email: data.email,
      captcha: data.captcha
    })
  },

  /**
   * 重置密码
   * @param {Object} data - 重置密码数据
   * @param {string} data.token - 重置令牌
   * @param {string} data.password - 新密码
   * @param {string} data.confirmPassword - 确认密码
   */
  resetPassword: (data) => {
    return secureAxios.post('/api/auth/password-reset-confirm/', {
      token: data.token,
      new_password: data.password,
      new_password_confirmation: data.confirmPassword
    })
  },

  /**
   * 验证邮箱
   * @param {string} token - 验证令牌
   */
  verifyEmail: (token) => {
    return secureAxios.post('/api/auth/verify-email/', {
      token: token
    })
  },

  /**
   * 重发验证邮件
   * @param {string} email - 邮箱地址
   */
  resendVerification: (email) => {
    return secureAxios.post('/api/auth/resend-verification/', {
      email: email
    })
  },

  /**
   * 获取验证码
   */
  getCaptcha: () => {
    // 返回验证码图片URL，添加时间戳防止缓存
    return `/api/auth/captcha/?t=${new Date().getTime()}`
  },

  /**
   * 刷新验证码
   */
  refreshCaptcha: () => {
    return authAPI.getCaptcha()
  },

  /**
   * 修改邮箱
   * @param {Object} data - 修改邮箱数据
   * @param {string} data.currentPassword - 当前密码
   * @param {string} data.newEmail - 新邮箱
   */
  changeEmail: (data) => {
    return secureAxios.post('/api/auth/change-email/', {
      current_password: data.currentPassword,
      new_email: data.newEmail
    })
  },

  /**
   * 停用账户
   * @param {string} password - 确认密码
   */
  deactivateAccount: (password) => {
    return secureAxios.post('/api/auth/deactivate-account/', {
      password: password
    })
  },

  /**
   * 创建 API 密钥
   * @param {Object} data - API 密钥数据
   * @param {string} data.name - 密钥名称
   * @param {string} data.description - 密钥描述
   * @param {Array} data.permissions - 权限列表
   */
  createAPIKey: (data) => {
    return secureAxios.post('/api/auth/api-keys/', data)
  },

  /**
   * 获取 API 密钥列表
   */
  getAPIKeys: () => {
    return secureAxios.get('/api/auth/api-keys/')
  },

  /**
   * 删除 API 密钥
   * @param {number} keyId - 密钥 ID
   */
  deleteAPIKey: (keyId) => {
    return secureAxios.delete(`/api/auth/api-keys/${keyId}/`)
  },

  /**
   * 更新用户资料
   * @param {Object} userData - 用户数据
   */
  updateProfile: (userData) => {
    return secureAxios.put('/api/auth/profile/', userData)
  },

  /**
   * 修改密码
   * @param {Object} data - 密码数据
   * @param {string} data.currentPassword - 当前密码
   * @param {string} data.newPassword - 新密码
   * @param {string} data.confirmPassword - 确认新密码
   */
  changePassword: (data) => {
    return secureAxios.post('/api/auth/change-password/', {
      current_password: data.currentPassword,
      new_password: data.newPassword,
      new_password_confirmation: data.confirmPassword
    })
  }
}
