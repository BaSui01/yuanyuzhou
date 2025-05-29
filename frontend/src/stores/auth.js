import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/modules/http'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref(null)
  const token = ref(localStorage.getItem('auth_token'))
  const isInitialized = ref(false)
  const loading = ref(false)

  // 计算属性
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const userName = computed(() => user.value?.name || '未知用户')
  const userAvatar = computed(() => user.value?.avatar || '/default-avatar.png')
  const userLevel = computed(() => user.value?.level || 1)
  const userExp = computed(() => user.value?.experience || 0)
  const isAdmin = computed(() => user.value?.role === 'admin' || user.value?.is_admin === true)
  const userRole = computed(() => user.value?.role || 'user')
  const userPermissions = computed(() => user.value?.permissions || [])

  // 设置认证信息
  const setAuth = (userData, authToken) => {
    user.value = userData
    token.value = authToken
    localStorage.setItem('auth_token', authToken)
    localStorage.setItem('user_data', JSON.stringify(userData))
  }

  // 清除认证信息
  const clearAuth = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user_data')
  }

  // 登录
  const login = async (credentials) => {
    loading.value = true
    try {
      const response = await api.auth.login(credentials)
      const { user: userData, token: authToken } = response.data

      setAuth(userData, authToken)

      return { success: true, data: response.data }
    } catch (error) {
      console.error('登录失败:', error)
      return {
        success: false,
        message: error.response?.data?.message || '登录失败，请重试'
      }
    } finally {
      loading.value = false
    }
  }

  // 注册
  const register = async (userData) => {
    loading.value = true
    try {
      const response = await api.auth.register(userData)
      const { user: newUser, token: authToken } = response.data

      setAuth(newUser, authToken)

      return { success: true, data: response.data }
    } catch (error) {
      console.error('注册失败:', error)
      return {
        success: false,
        message: error.response?.data?.message || '注册失败，请重试'
      }
    } finally {
      loading.value = false
    }
  }

  // 退出登录
  const logout = async () => {
    loading.value = true
    try {
      if (token.value) {
        await api.auth.logout()
      }
    } catch (error) {
      console.error('退出登录请求失败:', error)
    } finally {
      clearAuth()
      loading.value = false
    }
  }

  // 检查认证状态
  const checkAuth = async () => {
    if (isInitialized.value) return

    const savedToken = localStorage.getItem('auth_token')
    const savedUser = localStorage.getItem('user_data')

    if (savedToken && savedUser) {
      try {
        token.value = savedToken
        user.value = JSON.parse(savedUser)

        // 验证token是否仍然有效
        const response = await api.auth.me()
        user.value = response.data.user

        // 更新本地存储的用户信息
        localStorage.setItem('user_data', JSON.stringify(user.value))
      } catch (error) {
        console.error('Token验证失败:', error)
        clearAuth()
      }
    }

    isInitialized.value = true
  }

  // 更新用户信息
  const updateUser = async (userData) => {
    loading.value = true
    try {
      const response = await api.auth.updateProfile(userData)
      user.value = response.data.user

      // 更新本地存储
      localStorage.setItem('user_data', JSON.stringify(user.value))

      return { success: true, data: response.data }
    } catch (error) {
      console.error('更新用户信息失败:', error)
      return {
        success: false,
        message: error.response?.data?.message || '更新失败，请重试'
      }
    } finally {
      loading.value = false
    }
  }

  // 修改密码
  const changePassword = async (passwordData) => {
    loading.value = true
    try {
      const response = await api.auth.changePassword(passwordData)
      return { success: true, data: response.data }
    } catch (error) {
      console.error('修改密码失败:', error)
      return {
        success: false,
        message: error.response?.data?.message || '修改密码失败，请重试'
      }
    } finally {
      loading.value = false
    }
  }

  // 忘记密码
  const forgotPassword = async (email) => {
    loading.value = true
    try {
      const response = await api.auth.forgotPassword({ email })
      return { success: true, data: response.data }
    } catch (error) {
      console.error('发送重置密码邮件失败:', error)
      return {
        success: false,
        message: error.response?.data?.message || '发送失败，请重试'
      }
    } finally {
      loading.value = false
    }
  }

  // 重置密码
  const resetPassword = async (resetData) => {
    loading.value = true
    try {
      const response = await api.auth.resetPassword(resetData)
      return { success: true, data: response.data }
    } catch (error) {
      console.error('重置密码失败:', error)
      return {
        success: false,
        message: error.response?.data?.message || '重置密码失败，请重试'
      }
    } finally {
      loading.value = false
    }
  }

  // 检查权限
  const hasPermission = (permission) => {
    if (isAdmin.value) return true
    return userPermissions.value.includes(permission)
  }

  // 检查角色
  const hasRole = (role) => {
    if (isAdmin.value && role === 'admin') return true
    return userRole.value === role
  }

  // 获取社交登录URL
  const getSocialLoginUrl = async (provider) => {
    loading.value = true
    try {
      const response = await api.auth.getSocialLoginUrl(provider)
      return { success: true, data: response.data }
    } catch (error) {
      console.error('获取社交登录URL失败:', error)
      return {
        success: false,
        message: error.response?.data?.message || '获取失败，请重试'
      }
    } finally {
      loading.value = false
    }
  }

  return {
    // 状态
    user,
    token,
    isInitialized,
    loading,

    // 计算属性
    isAuthenticated,
    userName,
    userAvatar,
    userLevel,
    userExp,
    isAdmin,
    userRole,
    userPermissions,

    // 方法
    login,
    register,
    logout,
    checkAuth,
    updateUser,
    changePassword,
    forgotPassword,
    resetPassword,
    setAuth,
    clearAuth,
    hasPermission,
    hasRole,
    getSocialLoginUrl
  }
})
