import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '@/stores/auth'
import { authAPI } from '../api/authService.js'

/**
 * 认证功能 Composable
 * 提供登录、注册、密码重置等认证功能
 */
export function useAuth() {
  const router = useRouter()
  const toast = useToast()
  const authStore = useAuthStore()

  // 状态
  const loading = ref(false)
  const error = ref(null)

  // 计算属性
  const isAuthenticated = computed(() => authStore.isAuthenticated)
  const user = computed(() => authStore.user)

  /**
   * 用户登录
   * @param {Object} credentials - 登录凭据
   * @param {string} credentials.email - 邮箱
   * @param {string} credentials.password - 密码
   * @param {string} credentials.captcha - 验证码
   * @param {boolean} credentials.remember_me - 记住我
   */
  const login = async (credentials) => {
    loading.value = true
    error.value = null

    try {
      const response = await authAPI.login(credentials)

      // 保存认证信息到 store
      authStore.setAuth(response.data.user, response.data.token)

      // 显示成功消息
      toast.add({
        severity: 'success',
        summary: '登录成功',
        detail: response.data.message || '欢迎回来！',
        life: 3000
      })

      // 重定向到之前的页面或首页
      const redirect = router.currentRoute.value.query.redirect || '/'
      router.push(redirect)

      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || '登录失败，请重试'

      toast.add({
        severity: 'error',
        summary: '登录失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  /**
   * 用户注册
   * @param {Object} userData - 注册数据
   * @param {string} userData.username - 用户名
   * @param {string} userData.email - 邮箱
   * @param {string} userData.password - 密码
   * @param {string} userData.confirmPassword - 确认密码
   * @param {string} userData.captcha - 验证码
   */
  const register = async (userData) => {
    loading.value = true
    error.value = null

    try {
      const response = await authAPI.register(userData)

      // 显示成功消息
      toast.add({
        severity: 'success',
        summary: '注册成功',
        detail: response.data.message || '注册成功，请查收验证邮件',
        life: 5000
      })

      // 重定向到登录页
      router.push('/auth/login')

      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || '注册失败，请重试'

      toast.add({
        severity: 'error',
        summary: '注册失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  /**
   * 用户登出
   * @param {boolean} logoutAll - 是否登出所有设备
   */
  const logout = async (logoutAll = false) => {
    loading.value = true

    try {
      await authAPI.logout(logoutAll)
    } catch (err) {
      console.error('登出请求失败:', err)
    } finally {
      // 清除本地认证信息
      authStore.clearAuth()

      toast.add({
        severity: 'info',
        summary: '已登出',
        detail: '您已成功登出',
        life: 3000
      })

      // 重定向到登录页
      router.push('/auth/login')
      loading.value = false
    }
  }

  /**
   * 忘记密码
   * @param {Object} data - 忘记密码数据
   * @param {string} data.email - 邮箱
   * @param {string} data.captcha - 验证码
   */
  const forgotPassword = async (data) => {
    loading.value = true
    error.value = null

    try {
      const response = await authAPI.forgotPassword(data)

      toast.add({
        severity: 'success',
        summary: '邮件已发送',
        detail: response.data.message || '请检查您的邮箱，按照邮件中的说明重置密码',
        life: 5000
      })

      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || '发送失败，请重试'

      toast.add({
        severity: 'error',
        summary: '发送失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  /**
   * 重置密码
   * @param {Object} data - 重置密码数据
   * @param {string} data.token - 重置令牌
   * @param {string} data.password - 新密码
   * @param {string} data.confirmPassword - 确认密码
   */
  const resetPassword = async (data) => {
    loading.value = true
    error.value = null

    try {
      const response = await authAPI.resetPassword(data)

      toast.add({
        severity: 'success',
        summary: '密码已重置',
        detail: response.data.message || '您的密码已成功重置，请使用新密码登录',
        life: 5000
      })

      // 重定向到登录页
      router.push('/auth/login')

      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || '重置失败，请重试'

      toast.add({
        severity: 'error',
        summary: '重置失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  /**
   * 验证邮箱
   * @param {string} token - 验证令牌
   */
  const verifyEmail = async (token) => {
    loading.value = true
    error.value = null

    try {
      const response = await authAPI.verifyEmail(token)

      toast.add({
        severity: 'success',
        summary: '邮箱验证成功',
        detail: response.data.message || '您的邮箱已成功验证',
        life: 3000
      })

      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || '验证失败'

      toast.add({
        severity: 'error',
        summary: '验证失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  /**
   * 重发验证邮件
   * @param {string} email - 邮箱地址
   */
  const resendVerification = async (email) => {
    loading.value = true
    error.value = null

    try {
      const response = await authAPI.resendVerification(email)

      toast.add({
        severity: 'success',
        summary: '验证邮件已发送',
        detail: response.data.message || '验证邮件已重新发送',
        life: 3000
      })

      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.message || '发送失败'

      toast.add({
        severity: 'error',
        summary: '发送失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  /**
   * 检查认证状态
   */
  const checkAuthStatus = async () => {
    if (!authStore.token) return false

    try {
      const response = await authAPI.me()
      authStore.user = response.data.user
      return true
    } catch (err) {
      authStore.clearAuth()
      return false
    }
  }

  return {
    // 状态
    loading,
    error,
    isAuthenticated,
    user,

    // 方法
    login,
    register,
    logout,
    forgotPassword,
    resetPassword,
    verifyEmail,
    resendVerification,
    checkAuthStatus
  }
}
