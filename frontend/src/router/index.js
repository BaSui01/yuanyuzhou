import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/views/HomeView.vue'),
      meta: {
        title: '元宇宙社交空间',
        transition: 'fade'
      }
    },
    {
      path: '/auth',
      name: 'Auth',
      component: () => import('@/views/auth/AuthLayout.vue'),
      meta: {
        title: '用户认证',
        transition: 'slide-up',
        hidePet: true
      },
      children: [
        {
          path: 'login',
          name: 'Login',
          component: () => import('@/views/auth/LoginView.vue'),
          meta: {
            title: '登录',
            guest: true
          }
        },
        {
          path: 'register',
          name: 'Register',
          component: () => import('@/views/auth/RegisterView.vue'),
          meta: {
            title: '注册',
            guest: true
          }
        },
        {
          path: 'forgot-password',
          name: 'ForgotPassword',
          component: () => import('@/views/auth/ForgotPasswordView.vue'),
          meta: {
            title: '忘记密码',
            guest: true
          }
        },
        {
          path: 'reset-password',
          name: 'ResetPassword',
          component: () => import('@/views/auth/ResetPasswordView.vue'),
          meta: {
            title: '重置密码',
            guest: true
          }
        }
      ]
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: {
        title: '用户中心',
        requiresAuth: true,
        transition: 'slide-left'
      }
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('@/views/user/ProfileView.vue'),
      meta: {
        title: '个人资料',
        requiresAuth: true,
        transition: 'slide-left'
      }
    },
    {
      path: '/ai-chat',
      name: 'AIChat',
      component: () => import('@/views/ai/AIChatView.vue'),
      meta: {
        title: 'AI智能对话',
        requiresAuth: true,
        transition: 'slide-left'
      }
    },
    {
      path: '/ai-companion',
      name: 'AICompanion',
      component: () => import('@/views/ai/AICompanionView.vue'),
      meta: {
        title: 'AI伴侣',
        requiresAuth: true,
        transition: 'slide-left'
      }
    },
    {
      path: '/social',
      name: 'Social',
      component: () => import('@/views/social/SocialView.vue'),
      meta: {
        title: '社交空间',
        requiresAuth: true,
        transition: 'slide-left'
      }
    },
    {
      path: '/metaverse',
      name: 'Metaverse',
      component: () => import('@/views/metaverse/MetaverseView.vue'),
      meta: {
        title: '元宇宙空间',
        requiresAuth: true,
        transition: 'slide-left'
      }
    },
    {
      path: '/settings',
      name: 'Settings',
      component: () => import('@/views/user/SettingsView.vue'),
      meta: {
        title: '设置',
        requiresAuth: true,
        transition: 'slide-left'
      }
    },
    {
      path: '/voice-lab',
      name: 'VoiceLab',
      component: () => import('@/views/ai/VoiceLabView.vue'),
      meta: {
        title: '语音实验室',
        requiresAuth: true,
        transition: 'slide-left'
      }
    },
    // 后台管理系统路由
    {
      path: '/admin',
      name: 'Admin',
      component: () => import('@/views/admin/AdminLayout.vue'),
      meta: {
        title: '后台管理',
        requiresAuth: true,
        requiresAdmin: true,
        hidePet: true,
        transition: 'fade'
      },
      children: [
        {
          path: '',
          name: 'AdminDashboard',
          component: () => import('@/views/admin/DashboardView.vue'),
          meta: {
            title: '管理仪表盘',
            icon: 'pi pi-home'
          }
        },
        {
          path: 'users',
          name: 'AdminUsers',
          component: () => import('@/views/admin/users/UsersView.vue'),
          meta: {
            title: '用户管理',
            icon: 'pi pi-users'
          }
        },
        {
          path: 'users/:id',
          name: 'AdminUserDetail',
          component: () => import('@/views/admin/users/UserDetailView.vue'),
          meta: {
            title: '用户详情',
            parent: 'AdminUsers'
          }
        },
        {
          path: 'ai',
          name: 'AdminAI',
          component: () => import('@/views/admin/ai/AIManagementView.vue'),
          meta: {
            title: 'AI管理',
            icon: 'pi pi-comments'
          }
        },
        {
          path: 'metaverse',
          name: 'AdminMetaverse',
          component: () => import('@/views/admin/metaverse/MetaverseManagementView.vue'),
          meta: {
            title: '元宇宙管理',
            icon: 'pi pi-globe'
          }
        },
        {
          path: 'analytics',
          name: 'AdminAnalytics',
          component: () => import('@/views/admin/analytics/AnalyticsView.vue'),
          meta: {
            title: '数据分析',
            icon: 'pi pi-chart-bar'
          }
        },
        {
          path: 'settings',
          name: 'AdminSettings',
          component: () => import('@/views/admin/settings/SettingsView.vue'),
          meta: {
            title: '系统设置',
            icon: 'pi pi-cog'
          }
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/NotFoundView.vue'),
      meta: {
        title: '页面未找到',
        transition: 'fade'
      }
    }
  ]
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // 更新页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 元宇宙社交空间`
  }

  // 检查认证状态
  if (!authStore.isInitialized) {
    await authStore.checkAuth()
  }

  // 需要认证的路由
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }

  // 需要管理员权限的路由
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next({ name: 'Dashboard' })
    return
  }

  // 游客专用路由（已登录用户不能访问）
  if (to.meta.guest && authStore.isAuthenticated) {
    next({ name: 'Dashboard' })
    return
  }

  next()
})

export default router
