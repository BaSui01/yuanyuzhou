import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import '@/assets/css/admin.css'

export default {
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()
    const userMenu = ref(null)

    // 状态
    const sidebarVisible = ref(true)
    const showNotifications = ref(false)
    const showUserMenu = ref(false)
    const notifications = ref([
      {
        id: 1,
        title: '系统更新',
        message: '系统已更新到最新版本',
        time: '10分钟前',
        read: false,
        icon: 'pi pi-info-circle',
        iconBg: 'bg-blue-500/20 text-blue-400'
      },
      {
        id: 2,
        title: '新用户注册',
        message: '今日新增5位用户注册',
        time: '30分钟前',
        read: true,
        icon: 'pi pi-user-plus',
        iconBg: 'bg-green-500/20 text-green-400'
      }
    ])

    // 计算属性
    const notificationCount = computed(() => notifications.value.filter(n => !n.read).length)
    const currentRoute = computed(() => route)

    // 主菜单项
    const mainMenuItems = computed(() => {
      return router.options.routes
        .find(r => r.path === '/admin')
        .children
        .filter(route => route.meta && route.meta.icon)
    })

    // 用户菜单项
    const userMenuItems = [
      {
        label: authStore.userName,
        items: [
          {
            label: '返回前台',
            icon: 'pi pi-external-link',
            command: () => router.push('/dashboard')
          },
          {
            label: '个人资料',
            icon: 'pi pi-user',
            command: () => router.push('/profile')
          },
          {
            separator: true
          },
          {
            label: '退出登录',
            icon: 'pi pi-sign-out',
            command: () => logout()
          }
        ]
      }
    ]

    // 方法
    const toggleSidebar = () => {
      sidebarVisible.value = !sidebarVisible.value
    }

    const isRouteActive = (routeName) => {
      if (route.name === routeName) return true
      if (route.meta.parent === routeName) return true
      return false
    }

    const getParentRouteTitle = () => {
      if (!route.meta.parent) return ''
      const parentRoute = router.options.routes
        .find(r => r.path === '/admin')
        .children
        .find(r => r.name === route.meta.parent)

      return parentRoute?.meta?.title || ''
    }

    const logout = async () => {
      try {
        await authStore.logout()
        router.push('/auth/login')
      } catch (error) {
        console.error('退出登录失败:', error)
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
    onMounted(() => {
      // 检查用户是否有管理员权限
      if (!authStore.isAdmin) {
        router.push('/dashboard')
      }
    })

    return {
      sidebarVisible,
      showNotifications,
      showUserMenu,
      notifications,
      notificationCount,
      currentRoute,
      mainMenuItems,
      userMenuItems,
      userMenu,
      toggleSidebar,
      isRouteActive,
      getParentRouteTitle,
      logout,
      dismissNotification,
      markAllAsRead,
      clearAllNotifications
    }
  }
}
