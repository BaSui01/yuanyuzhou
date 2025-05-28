import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const userId = route.params.id

// 状态
const user = ref(null)
const loading = ref(true)
const deleteUserDialog = ref(false)
const sendNotificationDialog = ref(false)
const notification = ref({
  title: '',
  message: '',
  type: 'info'
})

// 用户活动记录
const userActivities = ref([
  {
    title: '登录系统',
    description: '用户从新设备登录了元宇宙社交空间',
    time: '2小时前',
    icon: 'pi pi-sign-in',
    iconColor: '#06b6d4',
    iconBg: 'rgba(6, 182, 212, 0.1)'
  },
  {
    title: 'AI对话',
    description: '与AI助手进行了15分钟的对话',
    time: '昨天',
    icon: 'pi pi-comments',
    iconColor: '#8b5cf6',
    iconBg: 'rgba(139, 92, 246, 0.1)'
  },
  {
    title: '个人资料更新',
    description: '用户更新了个人资料信息',
    time: '3天前',
    icon: 'pi pi-user-edit',
    iconColor: '#ec4899',
    iconBg: 'rgba(236, 72, 153, 0.1)'
  },
  {
    title: '购买会员',
    description: '用户购买了3个月的VIP会员',
    time: '1周前',
    icon: 'pi pi-wallet',
    iconColor: '#f59e0b',
    iconBg: 'rgba(245, 158, 11, 0.1)'
  }
])

// 用户统计数据
const userStats = ref({
  aiInteractions: 47,
  aiInteractionsLast30Days: 23,
  metaverseVisits: 18,
  metaverseVisitsLast30Days: 12,
  onlineHours: 35.5,
  onlineHoursLast30Days: 15.2,
  totalSpent: '299.00',
  spentLast30Days: '99.00'
})

// 通知类型选项
const notificationTypes = [
  { label: '信息', value: 'info' },
  { label: '成功', value: 'success' },
  { label: '警告', value: 'warning' },
  { label: '错误', value: 'error' }
]

// 方法
const loadUserData = async () => {
  loading.value = true

  try {
    // 模拟API请求
    setTimeout(() => {
      // 模拟用户数据
      if (userId === '1') {
        user.value = {
          id: 1,
          name: '张小明',
          email: 'zhang@example.com',
          avatar: '/avatars/user1.jpg',
          role: 'admin',
          status: 'active',
          lastLogin: '2023-05-28 14:30',
          createdAt: '2023-01-15',
          phone: '13812345678',
          birthday: '1990-01-15',
          gender: '男',
          location: '北京市',
          accountType: '高级账户',
          membershipLevel: 'VIP',
          membershipExpiry: '2023-12-31',
          balance: '1280.50',
          emailVerified: true,
          phoneVerified: true,
          twoFactorEnabled: true,
          lastPasswordChange: '2023-04-10'
        }
      } else if (userId === '2') {
        user.value = {
          id: 2,
          name: '李小华',
          email: 'li@example.com',
          avatar: '/avatars/user2.jpg',
          role: 'user',
          status: 'active',
          lastLogin: '2023-05-27 09:15',
          createdAt: '2023-02-20',
          phone: '13987654321',
          birthday: '1995-05-20',
          gender: '女',
          location: '上海市',
          accountType: '标准账户',
          membershipLevel: '普通会员',
          membershipExpiry: null,
          balance: '50.00',
          emailVerified: true,
          phoneVerified: false,
          twoFactorEnabled: false,
          lastPasswordChange: '2023-03-05'
        }
      } else {
        user.value = null
      }

      loading.value = false
    }, 1000)
  } catch (error) {
    console.error('加载用户数据失败:', error)
    loading.value = false
  }
}

const getRoleSeverity = (role) => {
  switch (role) {
    case 'admin':
      return 'danger'
    case 'vip':
      return 'warning'
    case 'creator':
      return 'info'
    default:
      return 'success'
  }
}

const getStatusSeverity = (status) => {
  switch (status) {
    case 'active':
      return 'success'
    case 'pending':
      return 'warning'
    case 'disabled':
      return 'info'
    case 'banned':
      return 'danger'
    default:
      return null
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}

const formatTimeAgo = (dateString) => {
  if (!dateString) return ''
  // 简单实现，实际项目中可使用专门的时间库
  return '最近'
}

const formatHours = (hours) => {
  if (!hours) return '0小时'
  return `${hours}小时`
}

const editUser = () => {
  // 跳转到编辑页面或打开编辑对话框
  router.push({ name: 'AdminUsers', query: { edit: userId } })
}

const confirmDeleteUser = () => {
  deleteUserDialog.value = true
}

const deleteUser = () => {
  // 模拟删除用户
  deleteUserDialog.value = false
  router.push({ name: 'AdminUsers' })
}

const resetPassword = () => {
  // 模拟重置密码
  alert(`已向用户 ${user.value.email} 发送密码重置邮件`)
}

const toggleUserStatus = () => {
  // 模拟切换用户状态
  if (user.value) {
    user.value.status = user.value.status === 'active' ? 'disabled' : 'active'
  }
}

const viewLoginHistory = () => {
  // 模拟查看登录历史
  alert('查看登录历史功能尚未实现')
}

const openSendNotification = () => {
  notification.value = {
    title: '',
    message: '',
    type: 'info'
  }
  sendNotificationDialog.value = true
}

const sendNotification = () => {
  // 模拟发送通知
  alert(`已向用户 ${user.value.name} 发送通知: ${notification.value.title}`)
  sendNotificationDialog.value = false
}

// 生命周期钩子
onMounted(() => {
  loadUserData()
})
