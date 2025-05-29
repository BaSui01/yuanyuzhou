/**
 * 管理后台认证 composable
 */
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { auth } from '../api/auth'

export function useAdminAuth() {
  const router = useRouter()
  const toast = useToast()

  // 状态
  const adminInfo = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const isAuthenticated = computed(() => !!adminInfo.value)

  /**
   * 管理员登录
   * @param {Object} credentials - 登录凭证
   * @returns {Promise<Object>} - 返回登录结果
   */
  const login = async (credentials) => {
    loading.value = true
    error.value = null

    try {
      const response = await auth.login(credentials)

      // 保存管理员信息
      adminInfo.value = response.user

      // 保存令牌
      localStorage.setItem('admin_token', response.token)

      toast.add({
        severity: 'success',
        summary: '登录成功',
        detail: '欢迎回到管理后台',
        life: 3000
      })

      // 跳转到仪表盘
      router.push('/admin/dashboard')

      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || '登录失败，请检查用户名和密码'

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
   * 管理员退出登录
   * @returns {Promise<boolean>} - 返回是否成功
   */
  const logout = async () => {
    loading.value = true

    try {
      await auth.logout()

      // 清除管理员信息
      adminInfo.value = null

      // 清除令牌
      localStorage.removeItem('admin_token')

      toast.add({
        severity: 'success',
        summary: '退出成功',
        detail: '您已成功退出管理后台',
        life: 3000
      })

      // 跳转到登录页
      router.push('/auth/login')

      return true
    } catch (err) {
      error.value = err.response?.data?.message || '退出登录失败'

      toast.add({
        severity: 'error',
        summary: '退出失败',
        detail: error.value,
        life: 5000
      })

      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取管理员信息
   * @returns {Promise<Object|null>} - 返回管理员信息
   */
  const getAdminInfo = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await auth.getProfile()
      adminInfo.value = response
      return adminInfo.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取管理员信息失败'
      console.error('获取管理员信息失败:', err)
      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 更新管理员信息
   * @param {Object} data - 个人资料数据
   * @returns {Promise<boolean>} - 返回是否成功
   */
  const updateAdminInfo = async (data) => {
    loading.value = true
    error.value = null

    try {
      const response = await auth.updateProfile(data)
      adminInfo.value = response

      toast.add({
        severity: 'success',
        summary: '更新成功',
        detail: '个人资料已更新',
        life: 3000
      })

      return true
    } catch (err) {
      error.value = err.response?.data?.message || '更新个人资料失败'

      toast.add({
        severity: 'error',
        summary: '更新失败',
        detail: error.value,
        life: 5000
      })

      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * 更改密码
   * @param {Object} data - 密码数据
   * @returns {Promise<boolean>} - 返回是否成功
   */
  const changePassword = async (data) => {
    loading.value = true
    error.value = null

    try {
      await auth.changePassword(data)

      toast.add({
        severity: 'success',
        summary: '密码已更改',
        detail: '您的密码已成功更改',
        life: 3000
      })

      return true
    } catch (err) {
      error.value = err.response?.data?.message || '更改密码失败'

      toast.add({
        severity: 'error',
        summary: '更改失败',
        detail: error.value,
        life: 5000
      })

      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * 检查认证状态
   * @returns {Promise<boolean>} - 返回是否已认证
   */
  const checkAuth = async () => {
    // 如果已有管理员信息，则认为已认证
    if (adminInfo.value) {
      return true
    }

    // 检查本地存储中是否有令牌
    const token = localStorage.getItem('admin_token')
    if (!token) {
      return false
    }

    // 验证令牌
    try {
      await auth.validateToken()

      // 获取管理员信息
      await getAdminInfo()

      return true
    } catch (err) {
      // 清除无效令牌
      localStorage.removeItem('admin_token')
      return false
    }
  }

  return {
    adminInfo,
    loading,
    error,
    isAuthenticated,
    login,
    logout,
    getAdminInfo,
    updateAdminInfo,
    changePassword,
    checkAuth
  }
}
