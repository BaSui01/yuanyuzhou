<template>
  <div class="admin-layout">
    <div class="admin-sidebar" :class="{ 'collapsed': sidebarCollapsed }">
      <div class="sidebar-header">
        <img src="@/assets/logo.png" alt="Logo" class="sidebar-logo" />
        <h2 v-if="!sidebarCollapsed">管理后台</h2>
        <Button
          icon="pi pi-bars"
          class="p-button-rounded p-button-text sidebar-toggle"
          @click="toggleSidebar"
        />
      </div>

      <div class="sidebar-content">
        <div class="sidebar-menu">
          <router-link to="/admin/dashboard" class="menu-item" v-slot="{ isActive }">
            <div :class="['menu-link', { 'active': isActive }]">
              <i class="pi pi-home"></i>
              <span v-if="!sidebarCollapsed">仪表盘</span>
            </div>
          </router-link>

          <router-link to="/admin/users" class="menu-item" v-slot="{ isActive }">
            <div :class="['menu-link', { 'active': isActive }]">
              <i class="pi pi-users"></i>
              <span v-if="!sidebarCollapsed">用户管理</span>
            </div>
          </router-link>

          <router-link to="/admin/analytics" class="menu-item" v-slot="{ isActive }">
            <div :class="['menu-link', { 'active': isActive }]">
              <i class="pi pi-chart-bar"></i>
              <span v-if="!sidebarCollapsed">数据分析</span>
            </div>
          </router-link>

          <router-link to="/admin/settings" class="menu-item" v-slot="{ isActive }">
            <div :class="['menu-link', { 'active': isActive }]">
              <i class="pi pi-cog"></i>
              <span v-if="!sidebarCollapsed">系统设置</span>
            </div>
          </router-link>
        </div>
      </div>

      <div class="sidebar-footer">
        <div class="user-info" v-if="!sidebarCollapsed">
          <Avatar :image="adminUser.avatar || '/img/admin.png'" shape="circle" />
          <div class="user-details">
            <span class="user-name">{{ adminUser.name }}</span>
            <span class="user-role">{{ adminUser.role }}</span>
          </div>
        </div>
        <Button
          icon="pi pi-sign-out"
          class="p-button-rounded p-button-text logout-button"
          @click="logout"
          v-tooltip.right="sidebarCollapsed ? '退出登录' : ''"
        />
      </div>
    </div>

    <div class="admin-content" :class="{ 'expanded': sidebarCollapsed }">
      <div class="content-header">
        <div class="header-left">
          <h1>{{ currentPageTitle }}</h1>
        </div>
        <div class="header-right">
          <Button icon="pi pi-bell" class="p-button-rounded p-button-text notification-button" badge="5" />
          <Menu ref="userMenu" :model="userMenuItems" :popup="true" />
          <Button
            icon="pi pi-user"
            class="p-button-rounded p-button-text user-menu-button"
            @click="toggleUserMenu"
          />
        </div>
      </div>

      <div class="content-body">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAdminAuth } from './composables/useAdminAuth'

export default {
  name: 'AdminLayout',
  setup() {
    const router = useRouter()
    const toast = useToast()
    const { adminInfo, logout: authLogout, getAdminInfo } = useAdminAuth()

    // 侧边栏折叠状态
    const sidebarCollapsed = ref(false)

    // 用户菜单
    const userMenu = ref(null)
    const userMenuItems = ref([
      {
        label: '个人资料',
        icon: 'pi pi-user',
        command: () => router.push('/admin/profile')
      },
      {
        label: '系统设置',
        icon: 'pi pi-cog',
        command: () => router.push('/admin/settings')
      },
      {
        separator: true
      },
      {
        label: '退出登录',
        icon: 'pi pi-sign-out',
        command: () => logout()
      }
    ])

    // 管理员用户信息
    const adminUser = computed(() => {
      return adminInfo.value || {
        name: '管理员',
        role: '超级管理员',
        avatar: '/img/admin.png'
      }
    })

    // 当前页面标题
    const currentPageTitle = computed(() => {
      const route = router.currentRoute.value
      switch (route.path) {
        case '/admin/dashboard':
          return '仪表盘'
        case '/admin/users':
          return '用户管理'
        case '/admin/analytics':
          return '数据分析'
        case '/admin/settings':
          return '系统设置'
        default:
          if (route.path.startsWith('/admin/users/')) {
            return '用户详情'
          }
          return '管理后台'
      }
    })

    // 切换侧边栏
    const toggleSidebar = () => {
      sidebarCollapsed.value = !sidebarCollapsed.value
      localStorage.setItem('admin-sidebar-collapsed', sidebarCollapsed.value)
    }

    // 切换用户菜单
    const toggleUserMenu = (event) => {
      userMenu.value.toggle(event)
    }

    // 退出登录
    const logout = async () => {
      try {
        await authLogout()
        router.push('/auth/login')
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: '退出失败',
          detail: '退出登录时发生错误',
          life: 3000
        })
      }
    }

    // 初始化
    onMounted(() => {
      // 从本地存储恢复侧边栏状态
      const savedState = localStorage.getItem('admin-sidebar-collapsed')
      if (savedState !== null) {
        sidebarCollapsed.value = savedState === 'true'
      }

      // 获取管理员信息
      getAdminInfo()
    })

    return {
      sidebarCollapsed,
      toggleSidebar,
      adminUser,
      userMenu,
      userMenuItems,
      toggleUserMenu,
      currentPageTitle,
      logout
    }
  }
}
</script>

<style lang="scss" scoped>
.admin-layout {
  display: flex;
  height: 100vh;
  width: 100%;
  overflow: hidden;
}

.admin-sidebar {
  width: 250px;
  background-color: #1e1e2d;
  color: #ffffff;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;

  &.collapsed {
    width: 70px;
  }

  .sidebar-header {
    height: 70px;
    padding: 0 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);

    .sidebar-logo {
      width: 36px;
      height: 36px;
    }

    h2 {
      margin: 0;
      font-size: 1.2rem;
      font-weight: 600;
      flex: 1;
      margin-left: 12px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }

  .sidebar-content {
    flex: 1;
    overflow-y: auto;
    padding: 16px 0;

    .sidebar-menu {
      display: flex;
      flex-direction: column;
      gap: 4px;

      .menu-item {
        text-decoration: none;
        color: #ffffff;

        .menu-link {
          display: flex;
          align-items: center;
          padding: 12px 16px;
          border-radius: 6px;
          margin: 0 8px;
          transition: background-color 0.2s ease;

          &:hover {
            background-color: rgba(255, 255, 255, 0.1);
          }

          &.active {
            background-color: var(--primary-color);
            color: #ffffff;
          }

          i {
            font-size: 1.2rem;
            margin-right: 12px;
          }

          span {
            font-size: 0.9rem;
            white-space: nowrap;
          }
        }
      }
    }
  }

  .sidebar-footer {
    height: 70px;
    padding: 0 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-top: 1px solid rgba(255, 255, 255, 0.1);

    .user-info {
      display: flex;
      align-items: center;
      gap: 10px;
      flex: 1;
      min-width: 0;

      .user-details {
        display: flex;
        flex-direction: column;
        min-width: 0;

        .user-name {
          font-size: 0.9rem;
          font-weight: 600;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .user-role {
          font-size: 0.75rem;
          opacity: 0.7;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
      }
    }
  }
}

.admin-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #f8f9fa;
  transition: margin-left 0.3s ease;
  overflow: hidden;

  &.expanded {
    margin-left: -180px;
  }

  .content-header {
    height: 70px;
    padding: 0 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: #ffffff;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    z-index: 10;

    .header-left {
      h1 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: 600;
      }
    }

    .header-right {
      display: flex;
      align-items: center;
      gap: 12px;

      .notification-button {
        position: relative;
      }
    }
  }

  .content-body {
    flex: 1;
    padding: 24px;
    overflow-y: auto;
  }
}
</style>
