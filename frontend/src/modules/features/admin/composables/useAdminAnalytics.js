/**
 * 管理后台数据分析 composable
 */
import { ref, reactive, watch } from 'vue'
import { useToast } from 'primevue/usetoast'
import { analytics } from '../api/analytics'
import Chart from 'chart.js/auto'

export function useAdminAnalytics() {
  const toast = useToast()

  // 状态
  const metrics = ref({
    activeUsers: 0,
    activeUsersTrend: 0,
    conversations: 0,
    conversationsTrend: 0,
    spaceVisits: 0,
    spaceVisitsTrend: 0,
    avgUsageTime: 0,
    avgUsageTimeTrend: 0
  })

  const topConversationTopics = ref([])
  const topSpaceScenes = ref([])
  const loading = ref(false)
  const error = ref(null)

  // 图表
  const charts = reactive({
    userActivity: null,
    deviceUsage: null,
    aiUsage: null,
    retention: null
  })

  // 周期选项
  const periodOptions = [
    { name: '今天', value: 'today' },
    { name: '昨天', value: 'yesterday' },
    { name: '本周', value: 'this_week' },
    { name: '本月', value: 'this_month' },
    { name: '本季度', value: 'this_quarter' },
    { name: '本年', value: 'this_year' }
  ]
  const selectedPeriod = ref(periodOptions[3])

  // 日期范围
  const dateRange = ref(null)

  // 选择的指标
  const metricOptions = [
    { name: '活跃用户', value: 'active_users' },
    { name: 'AI对话量', value: 'ai_conversations' },
    { name: '空间访问量', value: 'space_visits' },
    { name: '平均使用时长', value: 'avg_usage_time' }
  ]
  const selectedMetrics = ref([metricOptions[0], metricOptions[1]])

  // 图表设置
  const chartSettings = reactive({
    type: { name: '线图', value: 'line' },
    showLegend: true,
    stacked: false,
    dataPoints: 15
  })

  /**
   * 获取分析数据
   * @param {Object} params - 查询参数
   * @returns {Promise<Object>} - 返回分析数据
   */
  const getAnalyticsData = async (params = {}) => {
    loading.value = true
    error.value = null

    try {
      // 构建查询参数
      const queryParams = {
        period: selectedPeriod.value.value,
        ...params
      }

      if (dateRange.value && dateRange.value[0] && dateRange.value[1]) {
        queryParams.start_date = dateRange.value[0].toISOString().split('T')[0]
        queryParams.end_date = dateRange.value[1].toISOString().split('T')[0]
      }

      if (selectedMetrics.value.length > 0) {
        queryParams.metrics = selectedMetrics.value.map(m => m.value).join(',')
      }

      const response = await analytics.getAnalyticsData(queryParams)

      // 更新统计数据
      metrics.value = response.metrics

      // 更新热门主题
      topConversationTopics.value = response.topConversationTopics

      // 更新热门场景
      topSpaceScenes.value = response.topSpaceScenes

      return response
    } catch (err) {
      error.value = err.response?.data?.message || '获取分析数据失败'

      toast.add({
        severity: 'error',
        summary: '获取分析数据失败',
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
   * @param {Object} chartElements - 图表元素对象
   */
  const initCharts = (chartData, chartElements) => {
    // 销毁旧图表
    Object.keys(charts).forEach(key => {
      if (charts[key]) {
        charts[key].destroy()
        charts[key] = null
      }
    })

    // 用户活跃度趋势图
    if (chartElements.userActivity) {
      charts.userActivity = new Chart(chartElements.userActivity, {
        type: 'line',
        data: {
          labels: chartData.userActivity.labels,
          datasets: [
            {
              label: '日活跃用户',
              data: chartData.userActivity.daily,
              borderColor: '#4CAF50',
              backgroundColor: 'rgba(76, 175, 80, 0.1)',
              tension: 0.4,
              fill: true
            },
            {
              label: '周活跃用户',
              data: chartData.userActivity.weekly,
              borderColor: '#2196F3',
              backgroundColor: 'rgba(33, 150, 243, 0.1)',
              tension: 0.4,
              fill: true
            },
            {
              label: '月活跃用户',
              data: chartData.userActivity.monthly,
              borderColor: '#9C27B0',
              backgroundColor: 'rgba(156, 39, 176, 0.1)',
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
              display: chartSettings.showLegend
            },
            title: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              stacked: chartSettings.stacked
            },
            x: {
              stacked: chartSettings.stacked
            }
          }
        }
      })
    }

    // 设备使用分布图
    if (chartElements.deviceUsage) {
      charts.deviceUsage = new Chart(chartElements.deviceUsage, {
        type: 'doughnut',
        data: {
          labels: chartData.deviceUsage.labels,
          datasets: [
            {
              data: chartData.deviceUsage.data,
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
              position: 'right',
              display: chartSettings.showLegend
            }
          }
        }
      })
    }

    // AI助手使用情况图
    if (chartElements.aiUsage) {
      charts.aiUsage = new Chart(chartElements.aiUsage, {
        type: chartSettings.type.value === 'line' ? 'line' : 'bar',
        data: {
          labels: chartData.aiUsage.labels,
          datasets: [
            {
              label: '对话数量',
              data: chartData.aiUsage.conversations,
              backgroundColor: 'rgba(33, 150, 243, 0.7)',
              borderColor: 'rgba(33, 150, 243, 1)',
              tension: 0.4
            },
            {
              label: '平均时长(分钟)',
              data: chartData.aiUsage.duration,
              backgroundColor: 'rgba(156, 39, 176, 0.7)',
              borderColor: 'rgba(156, 39, 176, 1)',
              tension: 0.4
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
              display: chartSettings.showLegend
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              stacked: chartSettings.stacked
            },
            x: {
              stacked: chartSettings.stacked
            }
          }
        }
      })
    }

    // 用户留存率图
    if (chartElements.retention) {
      charts.retention = new Chart(chartElements.retention, {
        type: 'line',
        data: {
          labels: chartData.retention.labels,
          datasets: [
            {
              label: '次日留存',
              data: chartData.retention.nextDay,
              borderColor: '#4CAF50',
              backgroundColor: 'rgba(76, 175, 80, 0.1)',
              tension: 0.4,
              fill: true
            },
            {
              label: '7日留存',
              data: chartData.retention.day7,
              borderColor: '#2196F3',
              backgroundColor: 'rgba(33, 150, 243, 0.1)',
              tension: 0.4,
              fill: true
            },
            {
              label: '30日留存',
              data: chartData.retention.day30,
              borderColor: '#9C27B0',
              backgroundColor: 'rgba(156, 39, 176, 0.1)',
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
              display: chartSettings.showLegend
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
              ticks: {
                callback: function(value) {
                  return value + '%'
                }
              }
            }
          }
        }
      })
    }
  }

  /**
   * 刷新数据
   * @param {Object} chartElements - 图表元素对象
   */
  const refreshData = async (chartElements) => {
    const response = await getAnalyticsData()
    if (response && response.charts) {
      initCharts(response.charts, chartElements)
    }
  }

  /**
   * 应用图表设置
   * @param {Object} chartElements - 图表元素对象
   */
  const applyChartSettings = async (chartElements) => {
    const response = await getAnalyticsData()
    if (response && response.charts) {
      initCharts(response.charts, chartElements)

      toast.add({
        severity: 'success',
        summary: '设置已应用',
        detail: '图表设置已更新',
        life: 3000
      })
    }
  }

  /**
   * 导出分析报告
   * @param {string} format - 导出格式
   * @returns {Promise<Blob>} - 返回报告文件
   */
  const exportReport = async (format = 'pdf') => {
    loading.value = true
    error.value = null

    try {
      const response = await analytics.exportReport({
        period: selectedPeriod.value.value,
        format,
        metrics: selectedMetrics.value.map(m => m.value).join(',')
      })

      // 创建下载链接
      const url = window.URL.createObjectURL(response)
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `analytics-report-${new Date().toISOString().split('T')[0]}.${format}`)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)

      toast.add({
        severity: 'success',
        summary: '导出成功',
        detail: '分析报告已导出',
        life: 3000
      })

      return response
    } catch (err) {
      error.value = err.response?.data?.message || '导出分析报告失败'

      toast.add({
        severity: 'error',
        summary: '导出失败',
        detail: error.value,
        life: 5000
      })

      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 下载图表为图片
   * @param {string} chartId - 图表ID
   * @returns {string|null} - 返回图片数据URL
   */
  const downloadChart = (chartId) => {
    const chart = charts[chartId]
    if (chart) {
      const link = document.createElement('a')
      link.download = `${chartId}-chart.png`
      link.href = chart.toBase64Image()
      link.click()
      return link.href
    }
    return null
  }

  /**
   * 获取所有主题分析
   * @returns {Promise<Array>} - 返回主题分析数据
   */
  const getAllTopics = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await analytics.getAllTopics()
      return response.topics
    } catch (err) {
      error.value = err.response?.data?.message || '获取主题分析数据失败'

      toast.add({
        severity: 'error',
        summary: '获取主题数据失败',
        detail: error.value,
        life: 5000
      })

      return []
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取所有场景分析
   * @returns {Promise<Array>} - 返回场景分析数据
   */
  const getAllScenes = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await analytics.getAllScenes()
      return response.scenes
    } catch (err) {
      error.value = err.response?.data?.message || '获取场景分析数据失败'

      toast.add({
        severity: 'error',
        summary: '获取场景数据失败',
        detail: error.value,
        life: 5000
      })

      return []
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取自定义分析数据
   * @param {Object} data - 查询数据
   * @returns {Promise<Object>} - 返回自定义分析数据
   */
  const getCustomAnalytics = async (data) => {
    loading.value = true
    error.value = null

    try {
      const response = await analytics.getCustomAnalytics(data)
      return response
    } catch (err) {
      error.value = err.response?.data?.message || '获取自定义分析数据失败'

      toast.add({
        severity: 'error',
        summary: '获取自定义数据失败',
        detail: error.value,
        life: 5000
      })

      return null
    } finally {
      loading.value = false
    }
  }

  /**
   * 格式化数字
   * @param {number} num - 数字
   * @returns {string} - 格式化后的字符串
   */
  const formatNumber = (num) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M'
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K'
    }
    return num.toString()
  }

  // 监听周期变化
  watch(selectedPeriod, (newValue, oldValue) => {
    if (newValue !== oldValue) {
      getAnalyticsData()
    }
  })

  return {
    metrics,
    topConversationTopics,
    topSpaceScenes,
    loading,
    error,
    charts,
    periodOptions,
    selectedPeriod,
    dateRange,
    metricOptions,
    selectedMetrics,
    chartSettings,
    getAnalyticsData,
    initCharts,
    refreshData,
    applyChartSettings,
    exportReport,
    downloadChart,
    getAllTopics,
    getAllScenes,
    getCustomAnalytics,
    formatNumber
  }
}
