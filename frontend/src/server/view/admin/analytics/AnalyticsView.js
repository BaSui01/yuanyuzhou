import { ref, onMounted } from 'vue'
import '@/assets/css/admin.css'

export default {
  setup() {
    // 状态
    const dateRange = ref(null)
    const selectedDataType = ref('all')
    const selectedPeriod = ref('日')
    const selectedBehavior = ref('all')
    const loadingChart = ref(true)
    const loadingTable = ref(true)

    // 数据类型选项
    const dataTypes = [
      { label: '全部数据', value: 'all' },
      { label: '用户数据', value: 'users' },
      { label: 'AI互动数据', value: 'ai' },
      { label: '元宇宙数据', value: 'metaverse' },
      { label: '收入数据', value: 'revenue' }
    ]

    // 行为类型选项
    const behaviorTypes = [
      { label: '全部行为', value: 'all' },
      { label: '登录行为', value: 'login' },
      { label: 'AI对话', value: 'ai_chat' },
      { label: '元宇宙访问', value: 'metaverse_visit' },
      { label: '社交互动', value: 'social' },
      { label: '购买行为', value: 'purchase' }
    ]

    // 概览统计数据
    const overviewStats = ref([
      {
        title: '总用户数',
        value: '1,245',
        trend: '较上月增长 12%',
        trendIcon: 'pi pi-arrow-up',
        trendColor: '#10b981',
        icon: 'pi pi-users',
        color: '#06b6d4',
        iconBg: 'rgba(6, 182, 212, 0.1)'
      },
      {
        title: 'AI互动次数',
        value: '8,567',
        trend: '较上月增长 8%',
        trendIcon: 'pi pi-arrow-up',
        trendColor: '#10b981',
        icon: 'pi pi-comments',
        color: '#8b5cf6',
        iconBg: 'rgba(139, 92, 246, 0.1)'
      },
      {
        title: '元宇宙访问量',
        value: '3,782',
        trend: '较上月增长 5%',
        trendIcon: 'pi pi-arrow-up',
        trendColor: '#10b981',
        icon: 'pi pi-globe',
        color: '#ec4899',
        iconBg: 'rgba(236, 72, 153, 0.1)'
      },
      {
        title: '总收入',
        value: '¥12,350',
        trend: '较上月下降 3%',
        trendIcon: 'pi pi-arrow-down',
        trendColor: '#ef4444',
        icon: 'pi pi-wallet',
        color: '#f59e0b',
        iconBg: 'rgba(245, 158, 11, 0.1)'
      }
    ])

    // 详细数据
    const detailedData = ref([
      {
        date: '2023-05-28',
        newUsers: 45,
        activeUsers: 320,
        aiInteractions: 567,
        metaverseVisits: 189,
        revenue: '1,250.00',
        retention: 85
      },
      {
        date: '2023-05-27',
        newUsers: 42,
        activeUsers: 310,
        aiInteractions: 542,
        metaverseVisits: 175,
        revenue: '1,180.00',
        retention: 82
      },
      {
        date: '2023-05-26',
        newUsers: 38,
        activeUsers: 295,
        aiInteractions: 510,
        metaverseVisits: 168,
        revenue: '1,050.00',
        retention: 80
      },
      {
        date: '2023-05-25',
        newUsers: 41,
        activeUsers: 305,
        aiInteractions: 530,
        metaverseVisits: 172,
        revenue: '1,120.00',
        retention: 81
      },
      {
        date: '2023-05-24',
        newUsers: 36,
        activeUsers: 285,
        aiInteractions: 495,
        metaverseVisits: 160,
        revenue: '980.00',
        retention: 78
      },
      {
        date: '2023-05-23',
        newUsers: 39,
        activeUsers: 298,
        aiInteractions: 515,
        metaverseVisits: 165,
        revenue: '1,020.00',
        retention: 79
      },
      {
        date: '2023-05-22',
        newUsers: 44,
        activeUsers: 315,
        aiInteractions: 550,
        metaverseVisits: 180,
        revenue: '1,200.00',
        retention: 83
      }
    ])

    // 方法
    const refreshData = () => {
      loadingChart.value = true
      loadingTable.value = true

      // 模拟API请求
      setTimeout(() => {
        // 更新图表数据
        loadingChart.value = false

        // 更新表格数据
        loadingTable.value = false
      }, 1000)
    }

    const refreshChart = () => {
      loadingChart.value = true

      // 模拟API请求
      setTimeout(() => {
        loadingChart.value = false
      }, 800)
    }

    const applyFilters = () => {
      loadingChart.value = true
      loadingTable.value = true

      // 模拟API请求
      setTimeout(() => {
        // 根据筛选条件更新数据
        loadingChart.value = false
        loadingTable.value = false
      }, 1000)
    }

    const exportReport = () => {
      // 模拟导出功能
      alert('报表导出功能尚未实现')
    }

    // 生命周期钩子
    onMounted(() => {
      // 设置默认日期范围为过去30天
      const today = new Date()
      const thirtyDaysAgo = new Date()
      thirtyDaysAgo.setDate(today.getDate() - 30)
      dateRange.value = [thirtyDaysAgo, today]

      // 模拟加载图表数据
      setTimeout(() => {
        loadingChart.value = false
      }, 1500)

      // 模拟加载表格数据
      setTimeout(() => {
        loadingTable.value = false
      }, 1000)
    })

    return {
      dateRange,
      selectedDataType,
      selectedPeriod,
      selectedBehavior,
      loadingChart,
      loadingTable,
      dataTypes,
      behaviorTypes,
      overviewStats,
      detailedData,
      refreshData,
      refreshChart,
      applyFilters,
      exportReport
    }
  }
}
