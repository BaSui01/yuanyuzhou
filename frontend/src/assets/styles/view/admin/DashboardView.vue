<template>
  <div class="admin-dashboard">
    <h1 class="text-2xl font-bold text-white mb-6">管理仪表盘</h1>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
      <div
        v-for="(stat, index) in statCards"
        :key="index"
        class="stat-card bg-gray-800 rounded-xl p-6 border-l-4"
        :style="{ borderColor: stat.color }"
      >
        <div class="flex justify-between items-start">
          <div>
            <h3 class="text-gray-400 text-sm mb-1">{{ stat.title }}</h3>
            <div class="text-2xl font-bold text-white">{{ stat.value }}</div>
            <div class="text-xs mt-2" :style="{ color: stat.trendColor }">
              <i :class="stat.trendIcon"></i>
              {{ stat.trend }}
            </div>
          </div>
          <div class="stat-icon w-12 h-12 rounded-full flex items-center justify-center" :style="{ backgroundColor: stat.iconBg }">
            <i :class="stat.icon + ' text-xl'" :style="{ color: stat.color }"></i>
          </div>
        </div>
      </div>
    </div>

    <!-- 图表和数据区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
      <!-- 用户增长图表 -->
      <div class="chart-card bg-gray-800 rounded-xl p-6 lg:col-span-2">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold text-white">用户增长趋势</h2>
          <div class="chart-actions flex">
            <Button
              v-for="period in ['周', '月', '年']"
              :key="period"
              :label="period"
              class="p-button-text p-button-sm"
              :class="{ 'p-button-outlined': selectedPeriod === period }"
              @click="selectedPeriod = period"
            />
          </div>
        </div>

        <div class="chart-container h-80 flex items-center justify-center">
          <div v-if="loadingChart" class="text-center">
            <ProgressSpinner style="width:50px;height:50px" />
            <p class="text-gray-400 mt-2">加载图表数据...</p>
          </div>
          <div v-else class="w-full h-full">
            <!-- 这里将来放置实际的图表组件 -->
            <div class="mock-chart w-full h-full bg-gray-700/20 rounded-lg flex items-center justify-center">
              <p class="text-gray-400">用户增长趋势图表</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 活跃用户分布 -->
      <div class="chart-card bg-gray-800 rounded-xl p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold text-white">活跃用户分布</h2>
          <Button icon="pi pi-refresh" class="p-button-text p-button-rounded p-button-sm" @click="refreshData" />
        </div>

        <div class="chart-container h-80 flex items-center justify-center">
          <div v-if="loadingChart" class="text-center">
            <ProgressSpinner style="width:50px;height:50px" />
            <p class="text-gray-400 mt-2">加载图表数据...</p>
          </div>
          <div v-else class="w-full h-full">
            <!-- 这里将来放置实际的图表组件 -->
            <div class="mock-chart w-full h-full bg-gray-700/20 rounded-lg flex items-center justify-center">
              <p class="text-gray-400">用户分布饼图</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 最近活动和系统状态 -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 最近活动 -->
      <div class="recent-activities bg-gray-800 rounded-xl p-6 lg:col-span-2">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold text-white">最近活动</h2>
          <Button label="查看全部" class="p-button-text p-button-sm" />
        </div>

        <div class="activities space-y-4">
          <div v-for="(activity, index) in recentActivities" :key="index" class="activity flex gap-4">
            <div class="activity-icon w-10 h-10 rounded-full flex items-center justify-center" :style="{ backgroundColor: activity.iconBg }">
              <i :class="activity.icon + ' text-sm'" :style="{ color: activity.iconColor }"></i>
            </div>

            <div class="flex-1">
              <div class="flex justify-between">
                <h4 class="font-medium text-white">{{ activity.title }}</h4>
                <span class="text-xs text-gray-500">{{ activity.time }}</span>
              </div>
              <p class="text-sm text-gray-400">{{ activity.description }}</p>
              <div v-if="activity.user" class="flex items-center mt-2">
                <Avatar :image="activity.user.avatar" size="small" class="mr-2" />
                <span class="text-xs text-gray-400">{{ activity.user.name }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 系统状态 -->
      <div class="system-status bg-gray-800 rounded-xl p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold text-white">系统状态</h2>
          <Button icon="pi pi-refresh" class="p-button-text p-button-rounded p-button-sm" @click="refreshSystemStatus" />
        </div>

        <div class="status-items space-y-4">
          <div v-for="(status, index) in systemStatus" :key="index" class="status-item">
            <div class="flex justify-between items-center mb-1">
              <span class="text-sm text-gray-300">{{ status.name }}</span>
              <span class="text-xs" :style="{ color: status.statusColor }">{{ status.statusText }}</span>
            </div>
            <div class="h-2 bg-gray-700 rounded-full overflow-hidden">
              <div class="h-full rounded-full" :style="{ width: `${status.value}%`, backgroundColor: status.color }"></div>
            </div>
          </div>
        </div>

        <div class="mt-4 pt-4 border-t border-gray-700">
          <h3 class="text-sm font-medium text-gray-300 mb-3">快速操作</h3>
          <div class="grid grid-cols-2 gap-2">
            <Button label="清除缓存" icon="pi pi-refresh" class="p-button-sm" />
            <Button label="备份数据" icon="pi pi-database" class="p-button-sm" />
            <Button label="系统日志" icon="pi pi-list" class="p-button-sm" />
            <Button label="检查更新" icon="pi pi-sync" class="p-button-sm" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DashboardViews from '@/server/view/admin/DashboardViews'
</script>

<style>
@use '../../styles/view/admin/dashboard.scss'
</style>
