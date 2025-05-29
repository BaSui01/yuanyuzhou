<template>
  <div class="dashboard-view p-4 md:p-6">
    <div class="max-w-7xl mx-auto">
      <!-- 欢迎区域 -->
      <div class="welcome-section mb-8">
        <div class="glass rounded-xl p-6 md:p-8 flex flex-col md:flex-row items-center md:items-start gap-6">
          <div class="user-avatar">
            <Avatar :image="userAvatar" size="xlarge" class="w-24 h-24 ring-2 ring-white/20" />
          </div>

          <div class="user-info flex-1">
            <h1 class="text-2xl md:text-3xl font-bold text-white">欢迎回来，{{ userName }}</h1>
            <p class="text-gray-400 mt-2">今天是个探索元宇宙的好日子！</p>

            <div class="user-stats flex flex-wrap gap-4 mt-4">
              <div class="stat glass-dark px-4 py-2 rounded-lg">
                <div class="text-sm text-gray-400">等级</div>
                <div class="text-xl font-bold text-cyan-400">{{ userLevel }}</div>
              </div>

              <div class="stat glass-dark px-4 py-2 rounded-lg">
                <div class="text-sm text-gray-400">经验值</div>
                <div class="text-xl font-bold text-purple-400">{{ userExp }} / {{ nextLevelExp }}</div>
              </div>

              <div class="stat glass-dark px-4 py-2 rounded-lg">
                <div class="text-sm text-gray-400">AI互动</div>
                <div class="text-xl font-bold text-pink-400">{{ stats.aiInteractions || 0 }}</div>
              </div>

              <div class="stat glass-dark px-4 py-2 rounded-lg">
                <div class="text-sm text-gray-400">在线时长</div>
                <div class="text-xl font-bold text-amber-400">{{ formatTime(stats.onlineTime || 0) }}</div>
              </div>
            </div>
          </div>

          <div class="quick-actions flex flex-wrap gap-2">
            <Button icon="pi pi-user" class="p-button-rounded p-button-text" tooltip="个人资料"
              @click="$router.push('/profile')" />
            <Button icon="pi pi-cog" class="p-button-rounded p-button-text" tooltip="设置"
              @click="$router.push('/settings')" />
            <Button icon="pi pi-bell" class="p-button-rounded p-button-text" :badge="notificationCount.toString()"
              tooltip="通知" @click="showNotifications = true" />
          </div>
        </div>
      </div>

      <!-- 快捷访问卡片 -->
      <div class="quick-access-cards grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div v-for="card in quickAccessCards" :key="card.title"
          class="card glass hover:glass-hover cursor-pointer rounded-xl p-6 transition-all duration-300"
          @click="$router.push(card.route)">
          <div class="card-icon w-12 h-12 rounded-full flex items-center justify-center mb-4" :class="card.iconBg">
            <i :class="card.icon + ' text-xl'"></i>
          </div>

          <h3 class="text-lg font-bold text-white mb-2">{{ card.title }}</h3>
          <p class="text-gray-400 text-sm">{{ card.description }}</p>

          <div class="mt-4 flex justify-between items-center">
            <span class="text-xs text-gray-500">{{ card.status }}</span>
            <i class="pi pi-arrow-right text-cyan-400"></i>
          </div>
        </div>
      </div>

      <!-- 活动和统计 -->
      <div class="stats-and-activity grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- 最近活动 -->
        <div class="recent-activity lg:col-span-2 glass rounded-xl p-6">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-bold text-white">最近活动</h2>
            <Button label="查看全部" class="p-button-text p-button-sm" />
          </div>

          <div class="activities space-y-4">
            <div v-for="(activity, index) in recentActivities" :key="index" class="activity flex gap-4">
              <div class="activity-icon w-10 h-10 rounded-full flex items-center justify-center"
                :class="activity.iconBg">
                <i :class="activity.icon + ' text-sm'"></i>
              </div>

              <div class="flex-1">
                <div class="flex justify-between">
                  <h4 class="font-medium text-white">{{ activity.title }}</h4>
                  <span class="text-xs text-gray-500">{{ activity.time }}</span>
                </div>
                <p class="text-sm text-gray-400">{{ activity.description }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- AI助手状态 -->
        <div class="ai-assistant-status glass rounded-xl p-6">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-bold text-white">AI助手状态</h2>
            <Button icon="pi pi-refresh" class="p-button-text p-button-rounded p-button-sm" @click="refreshAIStatus" />
          </div>

          <div class="ai-status mb-6">
            <div class="flex items-center mb-4">
              <Avatar :image="petAvatar" class="mr-3" />
              <div>
                <h3 class="font-medium text-white">{{ petName }}</h3>
                <p class="text-xs text-cyan-400">{{ petStatus }}</p>
              </div>
            </div>

            <div class="stats space-y-4">
              <div class="stat">
                <div class="flex justify-between items-center mb-1">
                  <span class="text-sm text-gray-400">能量</span>
                  <span class="text-xs text-gray-500">{{ petEnergy }}%</span>
                </div>
                <div class="h-2 bg-gray-700 rounded-full overflow-hidden">
                  <div class="h-full bg-gradient-to-r from-green-400 to-cyan-400 rounded-full"
                    :style="{ width: `${petEnergy}%` }"></div>
                </div>
              </div>

              <div class="stat">
                <div class="flex justify-between items-center mb-1">
                  <span class="text-sm text-gray-400">心情</span>
                  <span class="text-xs text-gray-500">{{ petMood }}</span>
                </div>
                <div class="h-2 bg-gray-700 rounded-full overflow-hidden">
                  <div class="h-full bg-gradient-to-r from-yellow-400 to-amber-400 rounded-full"
                    :style="{ width: `${petMoodLevel}%` }"></div>
                </div>
              </div>

              <div class="stat">
                <div class="flex justify-between items-center mb-1">
                  <span class="text-sm text-gray-400">亲密度</span>
                  <span class="text-xs text-gray-500">{{ petIntimacy }}%</span>
                </div>
                <div class="h-2 bg-gray-700 rounded-full overflow-hidden">
                  <div class="h-full bg-gradient-to-r from-pink-400 to-purple-400 rounded-full"
                    :style="{ width: `${petIntimacy}%` }"></div>
                </div>
              </div>
            </div>
          </div>

          <div class="quick-actions">
            <Button label="与AI聊天" icon="pi pi-comments" class="w-full mb-2" @click="$router.push('/ai-chat')" />
            <Button label="AI伴侣空间" icon="pi pi-heart" class="p-button-outlined w-full"
              @click="$router.push('/ai-companion')" />
          </div>
        </div>
      </div>
    </div>

    <!-- 通知侧边栏 -->
    <Sidebar v-model:visible="showNotifications" position="right" class="p-sidebar-md">
      <template #header>
        <div class="flex justify-between items-center p-3">
          <h2 class="text-xl font-bold">通知中心</h2>
          <Button icon="pi pi-times" class="p-button-text p-button-rounded" @click="showNotifications = false" />
        </div>
      </template>

      <div class="notifications p-4 space-y-4">
        <div v-if="notifications.length === 0" class="text-center py-8">
          <i class="pi pi-bell-slash text-4xl text-gray-600 mb-4"></i>
          <p class="text-gray-400">暂无通知</p>
        </div>

        <div v-for="notification in notifications" :key="notification.id" class="notification glass-dark p-4 rounded-lg"
          :class="{ 'unread': !notification.read }">
          <div class="flex items-start gap-3">
            <div class="notification-icon w-8 h-8 rounded-full flex items-center justify-center"
              :class="notification.iconBg">
              <i :class="notification.icon + ' text-sm'"></i>
            </div>

            <div class="flex-1">
              <h4 class="font-medium text-white">{{ notification.title }}</h4>
              <p class="text-sm text-gray-400 mt-1">{{ notification.message }}</p>
              <div class="text-xs text-gray-500 mt-2">{{ notification.time }}</div>
            </div>

            <Button icon="pi pi-times" class="p-button-text p-button-rounded p-button-sm"
              @click="dismissNotification(notification.id)" />
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

<script setup>
import Dashboard from '@/modules/features/Dashboard';
</script>

<style lang="scss" scoped>
@use '@styles/view/dashboard.scss';
</style>
