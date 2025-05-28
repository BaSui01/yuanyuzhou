<template>
  <div id="app" class="min-h-screen relative">
    <!-- 3D背景容器 -->
    <div id="three-background" class="fixed inset-0 z-0"></div>

    <!-- 主应用内容 -->
    <div class="relative z-10">
      <!-- 路由视图 -->
      <router-view />
    </div>

    <!-- AI桌宠助手 -->
    <PetAssistant v-if="showPetAssistant" />

    <!-- 全局加载器 -->
    <div
      v-if="globalLoading"
      class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-[9999]"
    >
      <div class="glass rounded-xl p-8 text-center">
        <div class="loader w-12 h-12 mx-auto mb-4"></div>
        <p class="text-white text-lg">{{ loadingText }}</p>
      </div>
    </div>

    <!-- 全局通知系统 -->
    <div class="notification-container fixed top-4 right-4 z-[9998] space-y-3">
      <transition-group
        name="notification"
        enter-active-class="transition-all duration-300 ease-out"
        enter-from-class="opacity-0 transform translate-x-full"
        enter-to-class="opacity-100 transform translate-x-0"
        leave-active-class="transition-all duration-200 ease-in"
        leave-from-class="opacity-100 transform translate-x-0"
        leave-to-class="opacity-0 transform translate-x-full"
      >
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="notification max-w-sm"
          :class="notification.type"
        >
          <div class="flex items-start space-x-3">
            <i
              :class="getNotificationIcon(notification.type)"
              class="text-lg mt-1"
            ></i>
            <div class="flex-1">
              <p class="font-medium">{{ notification.title }}</p>
              <p v-if="notification.message" class="text-sm opacity-90 mt-1">
                {{ notification.message }}
              </p>
            </div>
            <button
              @click="removeNotification(notification.id)"
              class="text-white/60 hover:text-white transition-colors"
            >
              <i class="pi pi-times text-sm"></i>
            </button>
          </div>
        </div>
      </transition-group>
    </div>

    <!-- 网络状态指示器 -->
    <div
      v-if="!isOnline"
      class="fixed bottom-4 left-4 bg-red-500/20 border border-red-500/30 rounded-lg px-4 py-2 text-red-400 z-50"
    >
      <i class="pi pi-wifi text-sm mr-2"></i>
      网络连接已断开
    </div>

    <!-- 调试信息 (仅开发环境) -->
    <div
      v-if="isDevelopment && showDebugInfo"
      class="fixed bottom-4 left-4 bg-black/80 text-white text-xs p-4 rounded-lg font-mono z-40"
    >
      <div class="space-y-1">
        <div>环境: {{ env }}</div>
        <div>路由: {{ currentRoute }}</div>
        <div>用户: {{ isAuthenticated ? userName : '未登录' }}</div>
        <div>3D背景: {{ threeBackgroundLoaded ? '已加载' : '未加载' }}</div>
        <div>内存使用: {{ memoryUsage }}MB</div>
      </div>
      <button
        @click="showDebugInfo = false"
        class="absolute top-2 right-2 text-white/60 hover:text-white"
      >
        ×
      </button>
    </div>

    <!-- 快捷键提示 -->
    <div
      v-if="showShortcuts"
      class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-[9999]"
      @click="showShortcuts = false"
    >
      <div class="glass rounded-xl p-8 max-w-md w-full mx-4" @click.stop>
        <h3 class="text-xl font-bold text-white mb-6 text-center">快捷键</h3>
        <div class="space-y-3">
          <div v-for="shortcut in shortcuts" :key="shortcut.key" class="flex justify-between items-center">
            <span class="text-gray-300">{{ shortcut.description }}</span>
            <kbd class="bg-white/10 px-2 py-1 rounded text-sm text-white font-mono">
              {{ shortcut.key }}
            </kbd>
          </div>
        </div>
        <button
          @click="showShortcuts = false"
          class="btn-primary w-full mt-6"
        >
          确定
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThreeBackground } from '@/composables/useThreeBackground'
import PetAssistant from '@/components/ai/PetAssistant.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const { initThreeBackground, destroyThreeBackground, updateParticleTheme } = useThreeBackground()

// 响应式数据
const globalLoading = ref(false)
const loadingText = ref('加载中...')
const notifications = ref([])
const isOnline = ref(navigator.onLine)
const showDebugInfo = ref(false)
const showShortcuts = ref(false)
const threeBackgroundLoaded = ref(false)
const memoryUsage = ref(0)

// 计算属性
const isAuthenticated = computed(() => authStore.isAuthenticated)
const userName = computed(() => authStore.userName)
const currentRoute = computed(() => route.fullPath)
const isDevelopment = computed(() => import.meta.env.DEV)
const env = computed(() => import.meta.env.MODE)

const showPetAssistant = computed(() => {
  // 在特定页面显示AI桌宠
  const showPages = ['/dashboard', '/ai-chat', '/metaverse']
  return isAuthenticated.value && (
    showPages.includes(route.path) ||
    route.path.startsWith('/dashboard')
  )
})

// 快捷键配置
const shortcuts = ref([
  { key: 'Ctrl + K', description: '快速搜索' },
  { key: 'Ctrl + /', description: '显示快捷键' },
  { key: 'Esc', description: '关闭弹窗' },
  { key: 'Ctrl + D', description: '显示调试信息' },
  { key: 'Alt + T', description: '切换主题' },
  { key: 'Ctrl + Enter', description: '发送消息' }
])

// 通知管理
let notificationId = 0

const addNotification = (notification) => {
  const id = ++notificationId
  const newNotification = {
    id,
    type: 'info',
    title: '通知',
    message: '',
    duration: 5000,
    ...notification
  }

  notifications.value.push(newNotification)

  // 自动移除通知
  if (newNotification.duration > 0) {
    setTimeout(() => {
      removeNotification(id)
    }, newNotification.duration)
  }

  return id
}

const removeNotification = (id) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index > -1) {
    notifications.value.splice(index, 1)
  }
}

const getNotificationIcon = (type) => {
  const icons = {
    success: 'pi pi-check-circle',
    error: 'pi pi-times-circle',
    warning: 'pi pi-exclamation-triangle',
    info: 'pi pi-info-circle'
  }
  return icons[type] || 'pi pi-info-circle'
}

// 全局加载状态管理
const showGlobalLoading = (text = '加载中...') => {
  loadingText.value = text
  globalLoading.value = true
}

const hideGlobalLoading = () => {
  globalLoading.value = false
}

// 网络状态监听
const handleOnline = () => {
  isOnline.value = true
  addNotification({
    type: 'success',
    title: '网络已连接',
    message: '网络连接已恢复'
  })
}

const handleOffline = () => {
  isOnline.value = false
  addNotification({
    type: 'error',
    title: '网络已断开',
    message: '请检查网络连接',
    duration: 0 // 不自动消失
  })
}

// 快捷键处理
const handleKeyDown = (event) => {
  // Ctrl + K - 快速搜索
  if (event.ctrlKey && event.key === 'k') {
    event.preventDefault()
    // 实现搜索功能
    addNotification({
      type: 'info',
      title: '搜索功能',
      message: '搜索功能即将推出'
    })
  }

  // Ctrl + / - 显示快捷键
  if (event.ctrlKey && event.key === '/') {
    event.preventDefault()
    showShortcuts.value = true
  }

  // Esc - 关闭弹窗
  if (event.key === 'Escape') {
    showShortcuts.value = false
    showDebugInfo.value = false
  }

  // Ctrl + D - 调试信息
  if (event.ctrlKey && event.key === 'd' && isDevelopment.value) {
    event.preventDefault()
    showDebugInfo.value = !showDebugInfo.value
  }

  // Alt + T - 切换主题
  if (event.altKey && event.key === 't') {
    event.preventDefault()
    toggleTheme()
  }
}

// 主题切换
const toggleTheme = () => {
  const themes = ['cyber', 'nature', 'sunset', 'ocean']
  const currentTheme = localStorage.getItem('theme') || 'cyber'
  const currentIndex = themes.indexOf(currentTheme)
  const nextTheme = themes[(currentIndex + 1) % themes.length]

  localStorage.setItem('theme', nextTheme)
  updateParticleTheme(nextTheme)

  addNotification({
    type: 'success',
    title: '主题已切换',
    message: `已切换到${nextTheme}主题`
  })
}

// 内存使用监控
const updateMemoryUsage = () => {
  if (performance.memory) {
    memoryUsage.value = Math.round(performance.memory.usedJSHeapSize / 1024 / 1024)
  }
}

// 初始化3D背景
const initBackground = async () => {
  try {
    showGlobalLoading('正在加载3D背景...')
    await nextTick()

    await initThreeBackground('three-background')
    threeBackgroundLoaded.value = true

    // 根据当前主题设置粒子颜色
    const savedTheme = localStorage.getItem('theme') || 'cyber'
    updateParticleTheme(savedTheme)

    console.log('3D背景初始化成功')
  } catch (error) {
    console.error('3D背景初始化失败:', error)
    addNotification({
      type: 'warning',
      title: '3D背景加载失败',
      message: '将使用基础背景'
    })
  } finally {
    hideGlobalLoading()
  }
}

// 生命周期
onMounted(async () => {
  // 检查认证状态
  showGlobalLoading('正在验证身份...')
  await authStore.checkAuth()

  // 初始化3D背景
  await initBackground()

  // 添加事件监听器
  window.addEventListener('online', handleOnline)
  window.addEventListener('offline', handleOffline)
  window.addEventListener('keydown', handleKeyDown)

  // 内存监控定时器
  const memoryInterval = setInterval(updateMemoryUsage, 5000)

  // 欢迎通知
  if (isAuthenticated.value) {
    addNotification({
      type: 'success',
      title: `欢迎回来，${userName.value}！`,
      message: '准备好开始您的元宇宙之旅了吗？'
    })
  }

  onUnmounted(() => {
    // 清理事件监听器
    window.removeEventListener('online', handleOnline)
    window.removeEventListener('offline', handleOffline)
    window.removeEventListener('keydown', handleKeyDown)
    clearInterval(memoryInterval)

    // 销毁3D背景
    destroyThreeBackground()
  })
})

// 路由变化监听
watch(() => route.path, (newPath) => {
  // 路由变化时的处理逻辑
  console.log('路由变化:', newPath)
}, { immediate: true })

// 认证状态变化监听
watch(() => authStore.isAuthenticated, (authenticated) => {
  if (authenticated) {
    addNotification({
      type: 'success',
      title: '登录成功',
      message: `欢迎，${authStore.userName}！`
    })
  } else {
    addNotification({
      type: 'info',
      title: '已退出登录',
      message: '感谢使用，期待下次见面！'
    })
  }
})

// 暴露全局方法
window.app = {
  addNotification,
  showGlobalLoading,
  hideGlobalLoading,
  toggleTheme
}
</script>

<style lang="scss">
// 导入主样式文件
@use'@/assets/styles/main.scss';

// 应用特定样式
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

// 全局玻璃效果类
.glass {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.glass-dark {
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

// 通知动画
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

// 自定义滚动条
* {
  scrollbar-width: thin;
  scrollbar-color: rgba(6, 182, 212, 0.5) transparent;
}

*::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

*::-webkit-scrollbar-track {
  background: transparent;
}

*::-webkit-scrollbar-thumb {
  background: rgba(6, 182, 212, 0.5);
  border-radius: 3px;
}

*::-webkit-scrollbar-thumb:hover {
  background: rgba(6, 182, 212, 0.7);
}

// 响应式设计
@media (max-width: 768px) {
  .notification-container {
    @apply left-4 right-4;
  }

  .notification {
    @apply max-w-none;
  }
}

// 高对比度模式支持
@media (prefers-contrast: high) {
  .glass,
  .glass-dark {
    border-width: 2px;
  }

  .notification {
    border-width: 2px;
  }
}

// 减少动画模式支持
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

// 打印样式
@media print {
  #three-background,
  .pet-assistant,
  .notification-container {
    display: none !important;
  }
}
</style>
