/**
 * 管理后台用户管理 composable
 */
import { ref, reactive } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import { users } from '../api/users'

export function useAdminUsers() {
  const toast = useToast()
  const confirm = useConfirm()

  // 状态
  const usersList = ref([])
  const selectedUsers = ref([])
  const userDetail = ref(null)
  const loginHistory = ref([])
  const activityLog = ref([])
  const loading = ref(false)
  const submitting = ref(false)
  const error = ref(null)
  const totalUsers = ref(0)
  const pagination = reactive({
    page: 1,
    pageSize: 10,
    totalPages: 0
  })

  // 过滤器
  const filters = reactive({
    search: '',
    status: null,
    role: null,
    dateRange: [null, null],
    devices: {
      desktop: false,
      mobile: false,
      tablet: false
    },
    activity: null
  })

  /**
   * 获取用户列表
   * @param {Object} params - 查询参数
   * @returns {Promise<Array>} - 返回用户列表
   */
  const getUsers = async (params = {}) => {
    loading.value = true
    error.value = null

    try {
      // 构建查询参数
      const queryParams = {
        page: pagination.page,
        pageSize: pagination.pageSize,
        ...params
      }

      if (filters.search) {
        queryParams.search = filters.search
      }

      if (filters.status) {
        queryParams.status = filters.status.value
      }

      if (filters.role) {
        queryParams.role = filters.role.value
      }

      if (filters.dateRange[0] && filters.dateRange[1]) {
        queryParams.start_date = filters.dateRange[0].toISOString().split('T')[0]
        queryParams.end_date = filters.dateRange[1].toISOString().split('T')[0]
      }

      if (filters.activity) {
        queryParams.activity = filters.activity.value
      }

      const deviceFilters = []
      if (filters.devices.desktop) deviceFilters.push('desktop')
      if (filters.devices.mobile) deviceFilters.push('mobile')
      if (filters.devices.tablet) deviceFilters.push('tablet')

      if (deviceFilters.length > 0) {
        queryParams.devices = deviceFilters.join(',')
      }

      const response = await users.getUsers(queryParams)

      usersList.value = response.users
      totalUsers.value = response.total
      pagination.totalPages = response.totalPages

      return usersList.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取用户列表失败'

      toast.add({
        severity: 'error',
        summary: '获取用户列表失败',
        detail: error.value,
        life: 5000
      })

      return []
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取用户详情
   * @param {string|number} userId - 用户ID
   * @returns {Promise<Object|null>} - 返回用户详情
   */
  const getUserDetail = async (userId) => {
    loading.value = true
    error.value = null

    try {
      const response = await users.getUserDetail(userId)

      userDetail.value = response.user
      loginHistory.value = response.loginHistory || []
      activityLog.value = response.activityLog || []

      return userDetail.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取用户详情失败'

      toast.add({
        severity: 'error',
        summary: '获取用户详情失败',
        detail: error.value,
        life: 5000
      })

      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 创建用户
   * @param {Object} userData - 用户数据
   * @returns {Promise<Object>} - 返回创建结果
   */
  const createUser = async (userData) => {
    submitting.value = true
    error.value = null

    try {
      const response = await users.createUser(userData)

      toast.add({
        severity: 'success',
        summary: '创建成功',
        detail: '用户已成功创建',
        life: 3000
      })

      return { success: true, user: response }
    } catch (err) {
      error.value = err.response?.data?.message || '创建用户失败'

      toast.add({
        severity: 'error',
        summary: '创建失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      submitting.value = false
    }
  }

  /**
   * 更新用户信息
   * @param {string|number} userId - 用户ID
   * @param {Object} userData - 用户数据
   * @returns {Promise<Object>} - 返回更新结果
   */
  const updateUser = async (userId, userData) => {
    submitting.value = true
    error.value = null

    try {
      const response = await users.updateUser(userId, userData)

      toast.add({
        severity: 'success',
        summary: '更新成功',
        detail: '用户信息已更新',
        life: 3000
      })

      return { success: true, user: response }
    } catch (err) {
      error.value = err.response?.data?.message || '更新用户信息失败'

      toast.add({
        severity: 'error',
        summary: '更新失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      submitting.value = false
    }
  }

  /**
   * 删除用户
   * @param {string|number} userId - 用户ID
   * @returns {Promise<Object>} - 返回删除结果
   */
  const deleteUser = async (userId) => {
    submitting.value = true
    error.value = null

    try {
      await users.deleteUser(userId)

      toast.add({
        severity: 'success',
        summary: '删除成功',
        detail: '用户已成功删除',
        life: 3000
      })

      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || '删除用户失败'

      toast.add({
        severity: 'error',
        summary: '删除失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      submitting.value = false
    }
  }

  /**
   * 确认删除用户
   * @param {Object} user - 用户对象
   * @param {Function} callback - 删除成功后的回调函数
   */
  const confirmDeleteUser = (user, callback) => {
    confirm.require({
      message: `确定要删除用户 "${user.username}" 吗？此操作不可撤销。`,
      header: '确认删除',
      icon: 'pi pi-exclamation-triangle',
      acceptClass: 'p-button-danger',
      accept: async () => {
        const result = await deleteUser(user.id)
        if (result.success && callback) {
          callback()
        }
      }
    })
  }

  /**
   * 批量删除用户
   * @param {Array} userIds - 用户ID数组
   * @returns {Promise<Object>} - 返回删除结果
   */
  const batchDeleteUsers = async (userIds) => {
    submitting.value = true
    error.value = null

    try {
      await users.batchDeleteUsers(userIds)

      toast.add({
        severity: 'success',
        summary: '批量删除成功',
        detail: `已成功删除 ${userIds.length} 个用户`,
        life: 3000
      })

      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || '批量删除用户失败'

      toast.add({
        severity: 'error',
        summary: '批量删除失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      submitting.value = false
    }
  }

  /**
   * 确认批量删除用户
   * @param {Array} users - 用户对象数组
   * @param {Function} callback - 删除成功后的回调函数
   */
  const confirmBatchDeleteUsers = (users, callback) => {
    confirm.require({
      message: `确定要删除选中的 ${users.length} 个用户吗？此操作不可撤销。`,
      header: '确认批量删除',
      icon: 'pi pi-exclamation-triangle',
      acceptClass: 'p-button-danger',
      accept: async () => {
        const userIds = users.map(user => user.id)
        const result = await batchDeleteUsers(userIds)
        if (result.success && callback) {
          callback()
        }
      }
    })
  }

  /**
   * 更新用户状态
   * @param {string|number} userId - 用户ID
   * @param {string} status - 用户状态
   * @returns {Promise<Object>} - 返回更新结果
   */
  const updateUserStatus = async (userId, status) => {
    submitting.value = true
    error.value = null

    try {
      await users.updateUserStatus(userId, status)

      const statusText = status === 'active' ? '启用' : '禁用'

      toast.add({
        severity: 'success',
        summary: '状态更新成功',
        detail: `用户已${statusText}`,
        life: 3000
      })

      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || '更新用户状态失败'

      toast.add({
        severity: 'error',
        summary: '状态更新失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      submitting.value = false
    }
  }

  /**
   * 重置用户密码
   * @param {string|number} userId - 用户ID
   * @returns {Promise<Object>} - 返回重置结果
   */
  const resetUserPassword = async (userId) => {
    submitting.value = true
    error.value = null

    try {
      const response = await users.resetUserPassword(userId)

      toast.add({
        severity: 'success',
        summary: '密码重置成功',
        detail: '用户密码已重置',
        life: 3000
      })

      return { success: true, newPassword: response.newPassword }
    } catch (err) {
      error.value = err.response?.data?.message || '重置用户密码失败'

      toast.add({
        severity: 'error',
        summary: '密码重置失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      submitting.value = false
    }
  }

  /**
   * 确认重置用户密码
   * @param {Object} user - 用户对象
   * @param {Function} callback - 重置成功后的回调函数
   */
  const confirmResetUserPassword = (user, callback) => {
    confirm.require({
      message: `确定要重置用户 "${user.username}" 的密码吗？`,
      header: '确认重置密码',
      icon: 'pi pi-exclamation-triangle',
      accept: async () => {
        const result = await resetUserPassword(user.id)
        if (result.success && callback) {
          callback(result.newPassword)
        }
      }
    })
  }

  /**
   * 应用过滤器
   */
  const applyFilters = () => {
    pagination.page = 1
    getUsers()
  }

  /**
   * 重置过滤器
   */
  const resetFilters = () => {
    filters.search = ''
    filters.status = null
    filters.role = null
    filters.dateRange = [null, null]
    filters.devices = {
      desktop: false,
      mobile: false,
      tablet: false
    }
    filters.activity = null

    pagination.page = 1
    getUsers()
  }

  /**
   * 切换页码
   * @param {number} page - 页码
   */
  const changePage = (page) => {
    pagination.page = page
    getUsers()
  }

  /**
   * 切换每页数量
   * @param {number} pageSize - 每页数量
   */
  const changePageSize = (pageSize) => {
    pagination.pageSize = pageSize
    pagination.page = 1
    getUsers()
  }

  return {
    usersList,
    selectedUsers,
    userDetail,
    loginHistory,
    activityLog,
    loading,
    submitting,
    error,
    totalUsers,
    pagination,
    filters,
    getUsers,
    getUserDetail,
    createUser,
    updateUser,
    deleteUser,
    confirmDeleteUser,
    batchDeleteUsers,
    confirmBatchDeleteUsers,
    updateUserStatus,
    resetUserPassword,
    confirmResetUserPassword,
    applyFilters,
    resetFilters,
    changePage,
    changePageSize
  }
}
