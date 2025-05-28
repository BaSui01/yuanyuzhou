import { ref, onMounted } from 'vue'
import '@/assets/css/admin.css'

export default {
  setup() {
    // 状态
    const selectedPeriod = ref('月')
    const loadingChart = ref(true)

    // 统计卡片数据
    const statCards = ref([
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
        title: '系统收入',
        value: '¥12,350',
        trend: '较上月下降 3%',
        trendIcon: 'pi pi-arrow-down',
        trendColor: '#ef4444',
        icon: 'pi pi-wallet',
        color: '#f59e0b',
        iconBg: 'rgba(245, 158, 11, 0.1)'
      }
    ])

    // 最近活动
    const recentActivities = ref([
      {
        title: '新用户注册',
        description: '新用户完成注册并设置了个人资料',
        time: '10分钟前',
        icon: 'pi pi-user-plus',
        iconColor: '#06b6d4',
        iconBg: 'rgba(6, 182, 212, 0.1)',
        user: {
          name: '张小明',
          avatar: '/avatars/user1.jpg'
        }
      },
      {
        title: '系统更新',
        description: '系统已更新到最新版本 v1.2.5',
        time: '2小时前',
        icon: 'pi pi-sync',
        iconColor: '#8b5cf6',
        iconBg: 'rgba(139, 92, 246, 0.1)'
      },
      {
        title: '元宇宙空间创建',
        description: '用户创建了新的元宇宙空间',
        time: '昨天',
        icon: 'pi pi-globe',
        iconColor: '#ec4899',
        iconBg: 'rgba(236, 72, 153, 0.1)',
        user: {
          name: '李小华',
          avatar: '/avatars/user2.jpg'
        }
      },
      {
        title: 'AI模型更新',
        description: 'AI助手模型已更新到最新版本',
        time: '2天前',
        icon: 'pi pi-cog',
        iconColor: '#f59e0b',
        iconBg: 'rgba(245, 158, 11, 0.1)'
      }
    ])

    // 系统状态
    const systemStatus = ref([
      {
        name: 'CPU 使用率',
        value: 45,
        statusText: '正常',
        statusColor: '#10b981',
        color: '#06b6d4'
      },
      {
        name: '内存使用率',
        value: 72,
        statusText: '注意',
        statusColor: '#f59e0b',
        color: '#8b5cf6'
      },
      {
        name: '存储空间',
        value: 30,
        statusText: '正常',
        statusColor: '#10b981',
        color: '#ec4899'
      },
      {
        name: '网络带宽',
        value: 65,
        statusText: '正常',
        statusColor: '#10b981',
        color: '#f59e0b'
      }
    ])

    // 方法
    const refreshData = () => {
      loadingChart.value = true

      // 模拟API请求
      setTimeout(() => {
        loadingChart.value = false
      }, 1000)
    }

    const refreshSystemStatus = () => {
      // 模拟更新系统状态
      systemStatus.value = systemStatus.value.map(status => {
        return {
          ...status,
          value: Math.floor(Math.random() * 100)
        }
      })

      // 更新状态文本和颜色
      systemStatus.value.forEach(status => {
        if (status.value > 80) {
          status.statusText = '警告'
          status.statusColor = '#ef4444'
        } else if (status.value > 60) {
          status.statusText = '注意'
          status.statusColor = '#f59e0b'
        } else {
          status.statusText = '正常'
          status.statusColor = '#10b981'
        }
      })
    }

    // 生命周期钩子
    onMounted(() => {
      // 模拟加载图表数据
      setTimeout(() => {
        loadingChart.value = false
      }, 1500)
    })

    return {
      selectedPeriod,
      loadingChart,
      statCards,
      recentActivities,
      systemStatus,
      refreshData,
      refreshSystemStatus
    }
  }
}
