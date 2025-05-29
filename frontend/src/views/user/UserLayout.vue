<template>
  <div class="user-layout">
    <div class="user-sidebar">
      <div class="sidebar-header">
        <div class="user-avatar">
          <Avatar :image="user.avatar || '/img/default.png'" size="large" shape="circle" />
          <span class="status-badge" :class="isOnline ? 'online' : 'offline'"></span>
        </div>
        <div class="user-info">
          <h3>{{ user.username }}</h3>
          <p>{{ user.email }}</p>
        </div>
      </div>

      <div class="sidebar-menu">
        <ul>
          <li>
            <router-link to="/user/profile" active-class="active">
              <i class="pi pi-user"></i>
              <span>个人资料</span>
            </router-link>
          </li>
          <li>
            <router-link to="/user/settings" active-class="active">
              <i class="pi pi-cog"></i>
              <span>账号设置</span>
            </router-link>
          </li>
          <li>
            <router-link to="/user/friends" active-class="active">
              <i class="pi pi-users"></i>
              <span>好友管理</span>
            </router-link>
          </li>
          <li>
            <router-link to="/messages" active-class="active">
              <i class="pi pi-comments"></i>
              <span>消息中心</span>
              <Badge v-if="unreadMessages > 0" :value="unreadMessages" severity="danger" />
            </router-link>
          </li>
        </ul>
      </div>

      <div class="sidebar-footer">
        <Button icon="pi pi-arrow-left" label="返回主页" class="p-button-text" @click="goToHome" />
      </div>
    </div>

    <div class="user-content">
      <router-view />
    </div>
  </div>
</template>

<script>
import UserLayoutViews from '@/server/view/user/UserLayoutViews'
</script>

<style lang="scss">
@use '@styles/view/user/layout.scss';
</style>
