import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAIStore } from '@/stores/ai'
import Avatar from 'primevue/avatar'
import Button from 'primevue/button'
import Sidebar from 'primevue/sidebar'

const router = useRouter()
const authStore = useAuthStore()
const aiStore = useAIStore()

// 响应式数据
const showNotifications = ref(false)
const stats = ref({
  aiInteractions: 125,
  onlineTime: 3600 * 24 * 7, // 7天
})

// 计算属性
const userName = computed(() => authStore.userName)
const userAvatar = computed(() => authStore.userAvatar)
const userLevel = computed(() => authStore.userLevel)
const userExp = computed(() => authStore.userExp)
const nextLevelExp = computed(() => userLevel.value * 1000)

const petName = computed(() => aiStore.petName)
const petStatus = computed(() => '在线')
const petAvatar = computed(() => '/ai-pet-avatar.png')
const petEnergy = computed(() => aiStore.petSettings.energy)
const petMood = computed(() => aiStore.petSettings.mood)
const petMoodLevel = computed(() => {
  const moodLevels = { happy: 90, excited: 95, calm: 75, sad: 30, sleepy: 50 }
  return moodLevels[petMood.value] || 75
})
const petIntimacy = computed(() => aiStore.petSettings.intimacy)

const notificationCount = computed(() =>
  notifications.value.filter(n => !n.read).length
)

// 快捷访问卡片
const quickAccessCards = ref([
  {
    title: 'AI聊天',
    description: '与智能AI助手进行对话',
    icon: 'pi pi-comments',
    iconBg: 'bg-gradient-to-r from-blue-400 to-cyan-400',
    route: '/ai-chat',
    status: '活跃'
  },
  {
    title: '元宇宙',
    description: '探索虚拟世界空间',
    icon: 'pi pi-globe',
    iconBg: 'bg-gradient-to-r from-purple-400 to-pink-400',
    route: '/metaverse',
    status: '可用'
  },
  {
    title: '个人资料',
    description: '管理您的个人信息',
    icon: 'pi pi-user',
    iconBg: 'bg-gradient-to-r from-green-400 to-teal-400',
    route: '/profile',
    status: '完整'
  },
  {
    title: '设置',
    description: '系统设置和偏好',
    icon: 'pi pi-cog',
    iconBg: 'bg-gradient-to-r from-orange-400 to-amber-400',
    route: '/settings',
    status: '正常'
  }
])

// 最近活动
const recentActivities = ref([
  {
    title: '与AI助手聊天',
    description: '讨论了关于元宇宙的话题',
    time: '2分钟前',
    icon: 'pi pi-comments',
    iconBg: 'bg-blue-500/20 text-blue-400'
  },
  {
    title: '探索虚拟空间',
    description: '访问了新的3D场景',
    time: '1小时前',
    icon: 'pi pi-globe',
    iconBg: 'bg-purple-500/20 text-purple-400'
  },
  {
    title: '更新个人资料',
    description: '修改了头像和昵称',
    time: '3小时前',
    icon: 'pi pi-user',
    iconBg: 'bg-green-500/20 text-green-400'
  },
  {
    title: '系统登录',
    description: '成功登录到系统',
    time: '1天前',
    icon: 'pi pi-sign-in',
    iconBg: 'bg-orange-500/20 text-orange-400'
  }
])

// 通知数据
const notifications = ref([
  {
    id: 1,
    title: 'AI助手更新',
    message: '您的AI助手获得了新的对话能力',
    time: '10分钟前',
    read: false,
    icon: 'pi pi-robot',
    iconBg: 'bg-blue-500/20 text-blue-400'
  },
  {
    id: 2,
    title: '元宇宙活动',
    message: '新的虚拟活动即将开始',
    time: '1小时前',
    read: true,
    icon: 'pi pi-calendar',
    iconBg: 'bg-purple-500/20 text-purple-400'
  }
])

// 方法
const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const days = Math.floor(hours / 24)
  if (days > 0) return `${days}天`
  if (hours > 0) return `${hours}小时`
  return `${Math.floor(seconds / 60)}分钟`
}

const refreshAIStatus = async () => {
  // 刷新AI助手状态
  await aiStore.initializePet()
}

const dismissNotification = (id) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index !== -1) {
    notifications.value.splice(index, 1)
  }
}

const markAllAsRead = () => {
  notifications.value.forEach(n => n.read = true)
}

const clearAllNotifications = () => {
  notifications.value = []
}

// 生命周期
onMounted(async () => {
  // 初始化AI助手
  await aiStore.initializePet()
  await aiStore.loadSettings()
})
