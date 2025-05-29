import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useAdminStore = defineStore('admin', () => {
  // 状态
  const adminInfo = ref(null)
  const isLoading = ref(false)
  const error = ref(null)

  // 获取管理员信息
  const getAdminInfo = async () => {
    isLoading.value = true
    error.value = null

    try {
      const response = await axios.get('/api/admin/profile')
      adminInfo.value = response.data
      return adminInfo.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取管理员信息失败'
      console.error('获取管理员信息失败:', err)
      return null
    } finally {
      isLoading.value = false
    }
  }

  // 更新管理员信息
  const updateAdminInfo = async (data) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await axios.put('/api/admin/profile', data)
      adminInfo.value = response.data
      return true
    } catch (err) {
      error.value = err.response?.data?.message || '更新管理员信息失败'
      console.error('更新管理员信息失败:', err)
      return false
    } finally {
      isLoading.value = false
    }
  }

  // 管理员登录
  const login = async (credentials) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await axios.post('/api/admin/login', credentials)
      adminInfo.value = response.data.user

      // 保存令牌
      localStorage.setItem('admin_token', response.data.token)

      // 设置默认请求头
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`

      return true
    } catch (err) {
      error.value = err.response?.data?.message || '登录失败'
      console.error('管理员登录失败:', err)
      return false
    } finally {
      isLoading.value = false
    }
  }

  // 管理员退出登录
  const logout = async () => {
    isLoading.value = true
    error.value = null

    try {
      await axios.post('/api/admin/logout')

      // 清除状态
      adminInfo.value = null

      // 清除令牌
      localStorage.removeItem('admin_token')

      // 清除请求头
      delete axios.defaults.headers.common['Authorization']

      return true
    } catch (err) {
      error.value = err.response?.data?.message || '退出登录失败'
      console.error('管理员退出登录失败:', err)
      return false
    } finally {
      isLoading.value = false
    }
  }

  // 检查是否已登录
  const checkAuth = () => {
    const token = localStorage.getItem('admin_token')

    if (token) {
      // 设置默认请求头
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      return true
    }

    return false
  }

  // 初始化
  const initialize = async () => {
    if (checkAuth()) {
      return await getAdminInfo()
    }
    return null
  }

  return {
    adminInfo,
    isLoading,
    error,
    getAdminInfo,
    updateAdminInfo,
    login,
    logout,
    checkAuth,
    initialize
  }
})
