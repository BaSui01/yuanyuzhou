import secureAxios from '../secureAxios';

/**
 * 认证相关API
 */
export const authAPI = {
  // 用户登录
  login: (credentials) => {
    return secureAxios.post('/auth/login', {
      email: credentials.email,
      password: credentials.password,
      remember: credentials.remember || false
    });
  },

  // 用户注册
  register: (userData) => {
    return secureAxios.post('/auth/register', {
      name: userData.name,
      email: userData.email,
      password: userData.password,
      password_confirmation: userData.passwordConfirmation,
      terms_accepted: userData.termsAccepted || false
    });
  },

  // 退出登录
  logout: () => {
    return secureAxios.post('/auth/logout');
  },

  // 获取当前用户信息
  me: () => {
    return secureAxios.get('/auth/me');
  },

  // 刷新token
  refresh: () => {
    return secureAxios.post('/auth/refresh');
  },

  // 忘记密码
  forgotPassword: (email) => {
    return secureAxios.post('/auth/forgot-password', { email });
  },

  // 重置密码
  resetPassword: (data) => {
    return secureAxios.post('/auth/reset-password', {
      email: data.email,
      token: data.token,
      password: data.password,
      password_confirmation: data.passwordConfirmation
    });
  },

  // 修改密码
  changePassword: (data) => {
    return secureAxios.post('/auth/change-password', {
      current_password: data.currentPassword,
      password: data.newPassword,
      password_confirmation: data.passwordConfirmation
    });
  },

  // 更新用户资料
  updateProfile: (userData) => {
    return secureAxios.put('/auth/profile', {
      name: userData.name,
      email: userData.email,
      avatar: userData.avatar,
      bio: userData.bio,
      preferences: userData.preferences
    });
  },

  // 上传头像
  uploadAvatar: (file) => {
    const formData = new FormData();
    formData.append('avatar', file);

    return secureAxios.post('/auth/avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // 验证邮箱
  verifyEmail: (token) => {
    return secureAxios.post('/auth/verify-email', { token });
  },

  // 重发验证邮件
  resendVerification: () => {
    return secureAxios.post('/auth/resend-verification');
  },

  // 获取用户偏好设置
  getPreferences: () => {
    return secureAxios.get('/auth/preferences');
  },

  // 更新用户偏好设置
  updatePreferences: (preferences) => {
    return secureAxios.put('/auth/preferences', preferences);
  },

  // 获取用户统计信息
  getUserStats: () => {
    return secureAxios.get('/auth/stats');
  },

  // 删除账户
  deleteAccount: (password) => {
    return secureAxios.delete('/auth/account', {
      data: { password }
    });
  },

  // 检查邮箱是否可用
  checkEmailAvailability: (email) => {
    return secureAxios.post('/auth/check-email', { email });
  },

  // 检查用户名是否可用
  checkUsernameAvailability: (username) => {
    return secureAxios.post('/auth/check-username', { username });
  },

  // 获取第三方登录地址
  getSocialLoginUrl: (provider) => {
    return secureAxios.get(`/auth/social/${provider}`);
  },

  // 第三方登录回调处理
  handleSocialCallback: (provider, code, state) => {
    return secureAxios.post(`/auth/social/${provider}/callback`, {
      code,
      state
    });
  },

  // 绑定第三方账号
  bindSocialAccount: (provider, code) => {
    return secureAxios.post(`/auth/social/${provider}/bind`, { code });
  },

  // 解绑第三方账号
  unbindSocialAccount: (provider) => {
    return secureAxios.delete(`/auth/social/${provider}/unbind`);
  },

  // 启用两步验证
  enableTwoFactorAuth: () => {
    return secureAxios.post('/auth/2fa/enable');
  },

  // 禁用两步验证
  disableTwoFactorAuth: (password) => {
    return secureAxios.post('/auth/2fa/disable', { password });
  },

  // 验证两步验证码
  verifyTwoFactorAuth: (code) => {
    return secureAxios.post('/auth/2fa/verify', { code });
  },

  // 获取恢复代码
  getRecoveryCodes: () => {
    return secureAxios.get('/auth/2fa/recovery-codes');
  },

  // 重新生成恢复代码
  regenerateRecoveryCodes: () => {
    return secureAxios.post('/auth/2fa/recovery-codes/regenerate');
  }
};
