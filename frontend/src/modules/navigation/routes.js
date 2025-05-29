/**
 * 路由配置
 */

import { ROUTE_NAMES } from '../core/constants'

/**
 * 基础路由
 */
export const baseRoutes = [
  {
    path: '/',
    name: ROUTE_NAMES.HOME,
    component: () => import('@/views/Home.vue'),
    meta: {
      title: '首页',
      requiresAuth: false
    }
  },
  {
    path: '/dashboard',
    name: ROUTE_NAMES.DASHBOARD,
    component: () => import('@/views/Dashboard.vue'),
    meta: {
      title: '仪表板',
      requiresAuth: true
    }
  }
]

/**
 * 认证路由
 */
export const authRoutes = [
  {
    path: '/auth',
    component: () => import('@/views/auth/AuthLayout.vue'),
    meta: {
      requiresAuth: false
    },
    children: [
      {
        path: 'login',
        name: ROUTE_NAMES.LOGIN,
        component: () => import('@/views/auth/Login.vue'),
        meta: {
          title: '登录'
        }
      },
      {
        path: 'register',
        name: ROUTE_NAMES.REGISTER,
        component: () => import('@/views/auth/Register.vue'),
        meta: {
          title: '注册'
        }
      },
      {
        path: 'forgot-password',
        name: 'ForgotPassword',
        component: () => import('@/views/auth/ForgotPassword.vue'),
        meta: {
          title: '忘记密码'
        }
      },
      {
        path: 'reset-password',
        name: 'ResetPassword',
        component: () => import('@/views/auth/ResetPassword.vue'),
        meta: {
          title: '重置密码'
        }
      }
    ]
  }
]

/**
 * AI 功能路由
 */
export const aiRoutes = [
  {
    path: '/ai',
    component: () => import('@/views/ai/AILayout.vue'),
    meta: {
      requiresAuth: true,
      title: 'AI功能'
    },
    children: [
      {
        path: 'chat',
        name: ROUTE_NAMES.AI_CHAT,
        component: () => import('@/views/ai/AIChat.vue'),
        meta: {
          title: 'AI对话'
        }
      },
      {
        path: 'companion',
        name: ROUTE_NAMES.AI_COMPANION,
        component: () => import('@/views/ai/AICompanion.vue'),
        meta: {
          title: 'AI伴侣'
        }
      },
      {
        path: 'image-analysis',
        name: 'ImageAnalysis',
        component: () => import('@/views/ai/ImageAnalysis.vue'),
        meta: {
          title: '图像分析'
        }
      },
      {
        path: 'image-captioning',
        name: 'ImageCaptioning',
        component: () => import('@/views/ai/ImageCaptioning.vue'),
        meta: {
          title: '图像描述'
        }
      },
      {
        path: 'voice-lab',
        name: 'VoiceLab',
        component: () => import('@/views/ai/VoiceLab.vue'),
        meta: {
          title: '语音实验室'
        }
      }
    ]
  }
]

/**
 * 元宇宙路由
 */
export const metaverseRoutes = [
  {
    path: '/metaverse',
    name: ROUTE_NAMES.METAVERSE,
    component: () => import('@/views/metaverse/Metaverse.vue'),
    meta: {
      title: '元宇宙',
      requiresAuth: true
    }
  },
  {
    path: '/metaverse-view',
    name: 'MetaverseView',
    component: () => import('@/views/metaverse/MetaverseView.vue'),
    meta: {
      title: '元宇宙空间',
      requiresAuth: true
    }
  }
]

/**
 * 用户相关路由
 */
export const userRoutes = [
  {
    path: '/user',
    component: () => import('@/views/user/UserLayout.vue'),
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: 'profile',
        name: ROUTE_NAMES.PROFILE,
        component: () => import('@/views/user/Profile.vue'),
        meta: {
          title: '个人资料'
        }
      },
      {
        path: 'friends',
        name: ROUTE_NAMES.FRIENDS,
        component: () => import('@/views/user/Friends.vue'),
        meta: {
          title: '好友'
        }
      },
      {
        path: 'settings',
        name: ROUTE_NAMES.SETTINGS,
        component: () => import('@/views/user/Settings.vue'),
        meta: {
          title: '设置'
        }
      }
    ]
  }
]

/**
 * 管理员路由
 */
export const adminRoutes = [
  {
    path: '/admin',
    component: () => import('@/modules/features/admin/AdminLayout.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: '管理后台'
    },
    children: [
      {
        path: '',
        redirect: '/admin/dashboard'
      },
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/modules/features/admin/DashboardView.vue'),
        meta: {
          title: '管理仪表板'
        }
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('@/modules/features/admin/UsersView.vue'),
        meta: {
          title: '用户管理'
        }
      },
      {
        path: 'users/:id',
        name: 'AdminUserDetail',
        component: () => import('@/modules/features/admin/UserDetailView.vue'),
        meta: {
          title: '用户详情'
        }
      },
      {
        path: 'analytics',
        name: 'AdminAnalytics',
        component: () => import('@/modules/features/admin/AnalyticsView.vue'),
        meta: {
          title: '数据分析'
        }
      },
      {
        path: 'settings',
        name: 'AdminSettings',
        component: () => import('@/modules/features/admin/SettingsView.vue'),
        meta: {
          title: '系统设置'
        }
      }
    ]
  }
]

/**
 * 静态页面路由
 */
export const staticRoutes = [
  {
    path: '/about',
    name: 'About',
    component: () => import('@/components/pages/About.vue'),
    meta: {
      title: '关于我们',
      requiresAuth: false
    }
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('@/components/pages/Contact.vue'),
    meta: {
      title: '联系我们',
      requiresAuth: false
    }
  },
  {
    path: '/privacy',
    name: 'Privacy',
    component: () => import('@/components/pages/Privacy.vue'),
    meta: {
      title: '隐私政策',
      requiresAuth: false
    }
  },
  {
    path: '/team',
    name: 'Team',
    component: () => import('@/components/pages/Team.vue'),
    meta: {
      title: '团队介绍',
      requiresAuth: false
    }
  }
]

/**
 * 错误页面路由
 */
export const errorRoutes = [
  {
    path: '/404',
    name: 'NotFound',
    component: () => import('@/views/errors/404.vue'),
    meta: {
      title: '页面未找到'
    }
  },
  {
    path: '/403',
    name: 'Forbidden',
    component: () => import('@/views/errors/403.vue'),
    meta: {
      title: '访问被拒绝'
    }
  },
  {
    path: '/500',
    name: 'ServerError',
    component: () => import('@/views/errors/500.vue'),
    meta: {
      title: '服务器错误'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  }
]

/**
 * 合并所有路由
 */
export const routes = [
  ...baseRoutes,
  ...authRoutes,
  ...aiRoutes,
  ...metaverseRoutes,
  ...userRoutes,
  ...adminRoutes,
  ...staticRoutes,
  ...errorRoutes
]

/**
 * 路由分组导出
 */
export const routeGroups = {
  base: baseRoutes,
  auth: authRoutes,
  ai: aiRoutes,
  metaverse: metaverseRoutes,
  user: userRoutes,
  admin: adminRoutes,
  static: staticRoutes,
  error: errorRoutes
}

/**
 * 获取所有路由名称
 */
export const getAllRouteNames = () => {
  const names = []
  const extractNames = (routes) => {
    routes.forEach(route => {
      if (route.name) {
        names.push(route.name)
      }
      if (route.children) {
        extractNames(route.children)
      }
    })
  }
  extractNames(routes)
  return names
}

/**
 * 根据权限过滤路由
 */
export const filterRoutesByPermission = (routes, userPermissions = []) => {
  return routes.filter(route => {
    // 如果路由需要管理员权限
    if (route.meta?.requiresAdmin && !userPermissions.includes('admin')) {
      return false
    }
    // 如果路由需要认证但用户未登录
    if (route.meta?.requiresAuth && !userPermissions.includes('authenticated')) {
      return false
    }
    return true
  })
}

/**
 * 获取面包屑导航
 */
export const getBreadcrumbs = (route) => {
  const breadcrumbs = []
  const pathArray = route.path.split('/').filter(Boolean)
  let currentPath = ''

  pathArray.forEach((segment, index) => {
    currentPath += `/${segment}`
    const matchedRoute = routes.find(r => r.path === currentPath)
    if (matchedRoute && matchedRoute.meta?.title) {
      breadcrumbs.push({
        name: matchedRoute.meta.title,
        path: currentPath,
        isLast: index === pathArray.length - 1
      })
    }
  })

  return breadcrumbs
}

export default routes
