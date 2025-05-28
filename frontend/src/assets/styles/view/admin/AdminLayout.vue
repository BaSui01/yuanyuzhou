<template>
  <div class="admin-layout">
    <div class="flex h-screen">
      <!-- 侧边栏 -->
      <div class="admin-sidebar bg-gray-900 w-64 flex-shrink-0 h-full overflow-y-auto" :class="{ 'hidden': !sidebarVisible }">
        <!-- Logo和标题 -->
        <div class="p-4 border-b border-gray-800">
          <div class="flex items-center">
            <img src="/logo.svg" alt="Logo" class="h-8 w-8 mr-3" />
            <h1 class="text-xl font-bold text-white">管理后台</h1>
          </div>
        </div>

        <!-- 菜单 -->
        <div class="p-2">
          <div class="menu-section mb-4">
            <span class="text-xs text-gray-500 px-4 py-2 block">主菜单</span>
            <ul class="menu-items">
              <li v-for="route in mainMenuItems" :key="route.name">
                <router-link
                  :to="{ name: route.name }"
                  class="menu-item flex items-center px-4 py-2 rounded-lg text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
                  :class="{ 'active bg-gray-800 text-cyan-400': isRouteActive(route.name) }"
                >
                  <i :class="route.meta.icon + ' mr-3 text-lg'"></i>
                  <span>{{ route.meta.title }}</span>
                </router-link>
              </li>
            </ul>
          </div>

          <div class="menu-section mb-4">
            <span class="text-xs text-gray-500 px-4 py-2 block">系统</span>
            <ul class="menu-items">
              <li>
                <router-link
                  :to="{ name: 'AdminSettings' }"
                  class="menu-item flex items-center px-4 py-2 rounded-lg text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
                  :class="{ 'active bg-gray-800 text-cyan-400': isRouteActive('AdminSettings') }"
                >
                  <i class="pi pi-cog mr-3 text-lg"></i>
                  <span>系统设置</span>
                </router-link>
              </li>
              <li>
                <a
                  href="#"
                  class="menu-item flex items-center px-4 py-2 rounded-lg text-gray-300 hover:bg-gray-800 hover:text-white transition-colors"
                  @click.prevent="logout"
                >
                  <i class="pi pi-sign-out mr-3 text-lg"></i>
                  <span>退出登录</span>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 主内容区 -->
      <div class="admin-content flex-1 flex flex-col h-full overflow-hidden">
        <!-- 顶部导航栏 -->
        <header class="admin-header bg-gray-800 border-b border-gray-700 py-2 px-4">
          <div class="flex justify-between items-center">
            <div class="flex items-center">
              <Button
                icon="pi pi-bars"
                class="p-button-text p-button-rounded text-white mr-2 md:hidden"
                @click="toggleSidebar"
              />
              <div class="breadcrumbs text-gray-400 hidden md:flex items-center">
                <router-link to="/admin" class="hover:text-white">管理后台</router-link>
                <i v-if="currentRoute.meta.parent" class="pi pi-angle-right mx-2 text-gray-600"></i>
                <template v-if="currentRoute.meta.parent">
                  <router-link :to="{ name: currentRoute.meta.parent }" class="hover:text-white">
                    {{ getParentRouteTitle() }}
                  </router-link>
                </template>
                <i class="pi pi-angle-right mx-2 text-gray-600"></i>
                <span class="text-white">{{ currentRoute.meta.title }}</span>
              </div>
            </div>

            <div class="flex items-center">
              <Button
                icon="pi pi-bell"
                class="p-button-text p-button-rounded text-white mr-2"
                :badge="notificationCount.toString()"
                @click="showNotifications = true"
              />
              <Button
                icon="pi pi-user"
                class="p-button-text p-button-rounded text-white"
                @click="showUserMenu = true"
              />
              <Menu
                ref="userMenu"
                :model="userMenuItems"
                :popup="true"
                class="admin-user-menu"
              />
            </div>
          </div>
        </header>

        <!-- 页面内容 -->
        <main class="admin-main flex-1 overflow-auto bg-gray-900 p-4">
          <router-view></router-view>
        </main>
      </div>
    </div>

    <!-- 通知侧边栏 -->
    <Sidebar v-model:visible="showNotifications" position="right" class="p-sidebar-md">
      <template #header>
        <div class="flex justify-between items-center p-3">
          <h2 class="text-xl font-bold">系统通知</h2>
          <Button icon="pi pi-times" class="p-button-text p-button-rounded" @click="showNotifications = false" />
        </div>
      </template>

      <div class="notifications p-4 space-y-4">
        <div v-if="notifications.length === 0" class="text-center py-8">
          <i class="pi pi-bell-slash text-4xl text-gray-600 mb-4"></i>
          <p class="text-gray-400">暂无通知</p>
        </div>

        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="notification bg-gray-800 p-4 rounded-lg"
          :class="{'border-l-4': !notification.read}"
          :style="notification.read ? '' : 'border-color: #06b6d4'"
        >
          <div class="flex items-start gap-3">
            <div class="notification-icon w-8 h-8 rounded-full flex items-center justify-center" :class="notification.iconBg">
              <i :class="notification.icon + ' text-sm'"></i>
            </div>

            <div class="flex-1">
              <h4 class="font-medium text-white">{{ notification.title }}</h4>
              <p class="text-sm text-gray-400 mt-1">{{ notification.message }}</p>
              <div class="text-xs text-gray-500 mt-2">{{ notification.time }}</div>
            </div>

            <Button
              icon="pi pi-times"
              class="p-button-text p-button-rounded p-button-sm"
              @click="dismissNotification(notification.id)"
            />
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-between p-3 border-t border-gray-800">
          <Button label="全部已读" class="p-button-text" @click="markAllAsRead" />
          <Button label="清空通知" class="p-button-text p-button-danger" @click="clearAllNotifications" />
        </div>
      </template>
    </Sidebar>
  </div>
</template>

<script>
import AdminLayoutViews from '@/server/view/admin/AdminLayoutViews'
</script>

<style>
@use '../../styles/view/admin/dashboard.scss'
</style>
