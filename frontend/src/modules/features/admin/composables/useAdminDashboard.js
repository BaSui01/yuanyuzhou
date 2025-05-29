/**
 * 管理后台仪表盘 composable
 */
import { ref, reactive } from 'vue'
import { useToast } from 'primevue/usetoast'
import { dashboard } from '../api/dashboard'
import Chart from 'chart.js/auto'

export function useAdminDashboard() {
  const toast = useToast()

  // 状态
  const stats = ref({
    totalUsers: 0,
    userGrowth: 0,
    totalConversations: 0,
    conversationGrowth: 0,
    activeSpaces: 0,
    spaceGrowth: 0,
    avgUsageTime: 0,
    usageTimeGrowth: 0
  })

  const recentUsers = ref([])
  const systemNotifications = ref([])
  const loading = ref(false)
  const error = ref(null)

  // 图表
  const charts = reactive({
    userGrowth: null,
    activeUsers: null
  })

  // 图表周期选择
  const chartPeriods = [
    { name: '7天', value: '7d' },
    { name: '30天', value: '30d' },
    { name: '90天', value: '90d' },
    { name: '1年', value: '1y' }
  ]
  const selectedPeriod = ref(chartPeriods[1])

  /**
   * 获取仪表盘统计数据
   * @returns {Promise<Object>} - 返回统计数据
   */
  const getStats = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await dashboard.getStats()
      stats.value = response
      return stats.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取统计数据失败'

      toast.add({
        severity: 'error',
        summary: '获取统计数据失败',
        detail: error.value,
        life: 5000
      })

      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取用户增长趋势数据
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} - 返回趋势数据
   */
  const getUserGrowthTrend = async (params = {}) => {
    loading.value = true
    error.value = null

    try {
      const response = await dashboard.getUserGrowthTrend({
        period: selectedPeriod.value.value,
        ...params
      })
      return response
    } catch (err) {
      error.value = err.response?.data?.message || '获取用户增长趋势数据失败'

      toast.add({
        severity: 'error',
        summary: '获取趋势数据失败',
        detail: error.value,
        life: 5000
      })

      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取活跃用户分布数据
   * @returns {Promise<Object>} - 返回分布数据
   */
  const getActiveUsersDistribution = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await dashboard.getActiveUsersDistribution()
      return response
    } catch (err) {
      error.value = err.response?.data?.message || '获取活跃用户分布数据失败'

      toast.add({
        severity: 'error',
        summary: '获取分布数据失败',
        detail: error.value,
        life: 5000
      })

      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取最近注册用户
   * @param {Object} params - 查询参数
   * @returns {Promise<Array>} - 返回用户列表
   */
  const getRecentUsers = async (params = {}) => {
    loading.value = true
    error.value = null

    try {
      const response = await dashboard.getRecentUsers(params)
      recentUsers.value = response.users
      return recentUsers.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取最近注册用户失败'

      toast.add({
        severity: 'error',
        summary: '获取用户数据失败',
        detail: error.value,
        life: 5000
      })

      return []
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取系统通知
   * @param {Object} params - 查询参数
   * @returns {Promise<Array>} - 返回通知列表
   */
  const getSystemNotifications = async (params = {}) => {
    loading.value = true
    error.value = null

    try {
      const response = await dashboard.getSystemNotifications(params)
      systemNotifications.value = response.notifications
      return systemNotifications.value
    } catch (err) {
      error.value = err.response?.data?.message || '获取系统通知失败'

      toast.add({
        severity: 'error',
        summary: '获取通知数据失败',
        detail: error.value,
        life: 5000
      })

      return []
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取所有仪表盘数据
   * @returns {Promise<Object>} - 返回仪表盘数据
   */
  const getAllDashboardData = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await dashboard.getAllDashboardData()

      // 更新统计数据
      stats.value = response.stats

      // 更新最近用户
      recentUsers.value = response.recentUsers

      // 更新系统通知
      systemNotifications.value = response.systemNotifications

      return response
    } catch (err) {
      error.value = err.response?.data?.message || '获取仪表盘数据失败'

      toast.add({
        severity: 'error',
        summary: '获取仪表盘数据失败',
        detail: error.value,
        life: 5000
      })

      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 初始化图表
   * @param {Object} chartData - 图表数据
   * @param {HTMLElement} userGrowthChartEl - 用户增长图表元素
   * @param {HTMLElement} activeUsersChartEl - 活跃用户图表元素
   */
  const initCharts = (chartData, userGrowthChartEl, activeUsersChartEl) => {
    // 销毁旧图表
    if (charts.userGrowth) {
      charts.userGrowth.destroy()
    }

    if (charts.activeUsers) {
      charts.activeUsers.destroy()
    }

    // 用户增长趋势图
    if (userGrowthChartEl) {
      charts.userGrowth = new Chart(userGrowthChartEl, {
        type: 'line',
        data: {
          labels: chartData.userGrowth.labels,
          datasets: [
            {
              label: '新用户',
              data: chartData.userGrowth.data,
              borderColor: '#4CAF50',
              backgroundColor: 'rgba(76, 175, 80, 0.1)',
              tension: 0.4,
              fill: true
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
            title: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      })
    }

    // 活跃用户分布图
    if (activeUsersChartEl) {
      charts.activeUsers = new Chart(activeUsersChartEl, {
        type: 'doughnut',
        data: {
          labels: chartData.activeUsers.labels,
          datasets: [
            {
              data: chartData.activeUsers.data,
              backgroundColor: [
                'rgba(255, 99, 132, 0.7)',
                'rgba(54, 162, 235, 0.7)',
                'rgba(255, 206, 86, 0.7)',
                'rgba(75, 192, 192, 0.7)'
              ]
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'right'
            }
          }
        }
      })
    }
  }

  /**
   * 创建系统通知
   * @param {Object} data - 通知数据
   * @returns {Promise<Object>} - 返回创建结果
   */
  const createNotification = async (data) => {
    loading.value = true
    error.value = null

    try {
      const response = await dashboard.createNotification(data)

      toast.add({
        severity: 'success',
        summary: '创建成功',
        detail: '系统通知已创建',
        life: 3000
      })

      // 刷新通知列表
      await getSystemNotifications()

      return { success: true, notification: response }
    } catch (err) {
      error.value = err.response?.data?.message || '创建系统通知失败'

      toast.add({
        severity: 'error',
        summary: '创建失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  /**
   * 查看系统通知详情
   * @param {string|number} notificationId - 通知ID
   * @returns {Promise<Object>} - 返回通知详情
   */
  const getNotificationDetail = async (notificationId) => {
    loading.value = true
    error.value = null

    try {
      const response = await dashboard.getNotificationDetail(notificationId)
      return response
    } catch (err) {
      error.value = err.response?.data?.message || '获取通知详情失败'

      toast.add({
        severity: 'error',
        summary: '获取详情失败',
        detail: error.value,
        life: 5000
      })

      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 编辑系统通知
   * @param {string|number} notificationId - 通知ID
   * @param {Object} data - 通知数据
   * @returns {Promise<Object>} - 返回编辑结果
   */
  const updateNotification = async (notificationId, data) => {
    loading.value = true
    error.value = null

    try {
      const response = await dashboard.updateNotification(notificationId, data)

      toast.add({
        severity: 'success',
        summary: '更新成功',
        detail: '系统通知已更新',
        life: 3000
      })

      // 刷新通知列表
      await getSystemNotifications()

      return { success: true, notification: response }
    } catch (err) {
      error.value = err.response?.data?.message || '更新系统通知失败'

      toast.add({
        severity: 'error',
        summary: '更新失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  /**
   * 删除系统通知
   * @param {string|number} notificationId - 通知ID
   * @returns {Promise<Object>} - 返回删除结果
   */
  const deleteNotification = async (notificationId) => {
    loading.value = true
    error.value = null

    try {
      await dashboard.deleteNotification(notificationId)

      toast.add({
        severity: 'success',
        summary: '删除成功',
        detail: '系统通知已删除',
        life: 3000
      })

      // 刷新通知列表
      await getSystemNotifications()

      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.message || '删除系统通知失败'

      toast.add({
        severity: 'error',
        summary: '删除失败',
        detail: error.value,
        life: 5000
      })

      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取状态标签样式
   * @param {string} status - 状态
   * @returns {string} - 返回样式名称
   */
  const getStatusSeverity = (status) => {
    switch (status) {
      case '活跃':
        return 'success'
      case '待验证':
        return 'warning'
      case '禁用':
        return 'danger'
      default:
        return 'info'
    }
  }

  /**
   * 获取通知标签样式
   * @param {string} type - 通知类型
   * @returns {string} - 返回样式名称
   */
  const getNotificationSeverity = (type) => {
    switch (type) {
      case '系统':
        return 'info'
      case '更新':
        return 'success'
      case '警告':
        return 'warning'
      case '错误':
        return 'danger'
      default:
        return 'info'
    }
  }

  return {
    stats,
    recentUsers,
    systemNotifications,
    loading,
    error,
    charts,
    chartPeriods,
    selectedPeriod,
    getStats,
    getUserGrowthTrend,
    getActiveUsersDistribution,
    getRecentUsers,
    getSystemNotifications,
    getAllDashboardData,
    initCharts,
    createNotification,
    getNotificationDetail,
    updateNotification,
    deleteNotification,
    getStatusSeverity,
    getNotificationSeverity
  }
}
