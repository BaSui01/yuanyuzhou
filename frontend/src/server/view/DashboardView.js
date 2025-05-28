import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useAIStore } from '@/stores/ai'

const authStore = useAuthStore()
const aiStore = useAIStore()

// 用户信息
const userName = computed(() => authStore.userName)
const userAvatar = computed(() => authStore.userAvatar)
const userLevel = computed(() => authStore.userLevel)
const userExp = computed(() => authStore.userExp)
const nextLevelExp = computed(() => userLevel.value * 100)

// AI宠物信息
const petName = computed(() => aiStore.petName)
const petAvatar = computed(() => `/avatars/pet-${aiStore.petSettings.appearance.color.replace('#', '')}.png`)
const petStatus = computed(() => {
  const mood = aiStore.petSettings.mood
  if (mood === 'happy') return '心情愉悦'
  if (mood === 'excited') return '兴奋不已'
  if (mood === 'calm') return '平静放松'
  if (mood === 'sleepy') return '有点困倦'
  if (mood === 'sad') return '情绪低落'
  return '状态正常'
})
const petEnergy = ref(85)
const petMood = computed(() => {
  const mood = aiStore.petSettings.mood
  if (mood === 'happy') return '愉悦'
  if (mood === 'excited') return '兴奋'
  if (mood === 'calm') return '平静'
  if (mood === 'sleepy') return '困倦'
  if (mood === 'sad') return '低落'
  return '正常'
})
const petMoodLevel = computed(() => {
  const mood = aiStore.petSettings.mood
  if (mood === 'happy') return 90
  if (mood === 'excited') return 95
  if (mood === 'calm') return 70
  if (mood === 'sleepy') return 40
  if (mood === 'sad') return 30
  return 60
})
const petIntimacy = ref(65)

// 用户统计
const stats = ref({
  aiInteractions: 47,
  onlineTime: 3600 * 5 + 1800, // 5小时30分钟
  lastLogin: '2025-05-28 14:30'
})

// 通知
const showNotifications = ref(false)
const notifications = ref([
  {
    id: 1,
    title: '系统更新',
    message: '元宇宙社交空间已更新到最新版本，新增多项功能',
    time: '10分钟前',
    read: false,
    icon: 'pi pi-info-circle',
    iconBg: 'bg-blue-500/20 text-blue-400'
  },
  {
    id: 2,
    title: 'AI助手提醒',
    message: '您的AI助手小星想和您聊天了',
    time: '30分钟前',
    read: true,
    icon: 'pi pi-comment',
    iconBg: 'bg-cyan-500/20 text-cyan-400'
  },
  {
    id: 3,
    title: '成就解锁',
    message: '恭喜您解锁了"探索先锋"成就',
    time: '2小时前',
    read: true,
    icon: 'pi pi-star',
    iconBg: 'bg-yellow-500/20 text-yellow-400'
  }
])
const notificationCount = computed(() => notifications.value.filter(n => !n.read).length)

// 快捷访问卡片
const quickAccessCards = ref([
  {
    title: 'AI智能对话',
    description: '与您的AI助手进行智能对话',
    icon: 'pi pi-comments',
    iconBg: 'bg-cyan-500/20 text-cyan-400',
    route: '/ai-chat',
    status: '今日已对话: 3次'
  },
  {
    title: '元宇宙空间',
    description: '探索您的个人元宇宙空间',
    icon: 'pi pi-globe',
    iconBg: 'bg-purple-500/20 text-purple-400',
    route: '/metaverse',
    status: '上次访问: 2小时前'
  },
  {
    title: '社交广场',
    description: '与其他用户互动交流',
    icon: 'pi pi-users',
    iconBg: 'bg-pink-500/20 text-pink-400',
    route: '/social',
    status: '5位好友在线'
  },
  {
    title: '语音实验室',
    description: 'AI语音合成与识别',
    icon: 'pi pi-volume-up',
    iconBg: 'bg-amber-500/20 text-amber-400',
    route: '/voice-lab',
    status: '新功能已上线'
  }
])

// 最近活动
const recentActivities = ref([
  {
    title: '登录系统',
    description: '您从新设备登录了元宇宙社交空间',
    time: '刚刚',
    icon: 'pi pi-sign-in',
    iconBg: 'bg-green-500/20 text-green-400'
  },
  {
    title: 'AI对话',
    description: '与AI助手进行了15分钟的对话',
    time: '2小时前',
    icon: 'pi pi-comments',
    iconBg: 'bg-cyan-500/20 text-cyan-400'
  },
  {
    title: '成就解锁',
    description: '解锁了"探索先锋"成就',
    time: '昨天',
    icon: 'pi pi-star',
    iconBg: 'bg-yellow-500/20 text-yellow-400'
  },
  {
    title: '系统更新',
    description: '元宇宙社交空间更新到了最新版本',
    time: '2天前',
    icon: 'pi pi-refresh',
    iconBg: 'bg-blue-500/20 text-blue-400'
  }
])

// 方法
const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)

  return `${hours}小时${minutes}分钟`
}

const refreshAIStatus = async () => {
  try {
    // 模拟API调用
    petEnergy.value = Math.floor(Math.random() * 30) + 70 // 70-100之间
    petIntimacy.value = Math.floor(Math.random() * 20) + 60 // 60-80之间

    // 实际项目中应该调用API
    // await aiStore.refreshPetStatus()
  } catch (error) {
    console.error('刷新AI状态失败:', error)
  }
}

const dismissNotification = (id) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index !== -1) {
    notifications.value.splice(index, 1)
  }
}

const markAllAsRead = () => {
  notifications.value.forEach(notification => {
    notification.read = true
  })
}

const clearAllNotifications = () => {
  notifications.value = []
}

// 生命周期钩子
onMounted(async () => {
  // 初始化数据
  refreshAIStatus()

  // 实际项目中应该从API获取数据
  // await Promise.all([
  //   authStore.getUserStats(),
  //   aiStore.getPetStatus()
  // ])
})
