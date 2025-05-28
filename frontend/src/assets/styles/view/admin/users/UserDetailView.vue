<template>
  <div class="admin-user-detail">
    <div class="flex justify-between items-center mb-6">
      <div class="flex items-center">
        <Button
          icon="pi pi-arrow-left"
          class="p-button-text p-button-rounded mr-2"
          @click="$router.push({ name: 'AdminUsers' })"
        />
        <h1 class="text-2xl font-bold text-white">用户详情</h1>
      </div>
      <div class="flex gap-2">
        <Button label="编辑用户" icon="pi pi-pencil" @click="editUser" />
        <Button label="删除用户" icon="pi pi-trash" class="p-button-danger" @click="confirmDeleteUser" />
      </div>
    </div>

    <div v-if="loading" class="loading-container flex items-center justify-center h-64">
      <ProgressSpinner style="width:50px;height:50px" />
      <p class="text-gray-400 ml-4">加载用户数据...</p>
    </div>

    <div v-else-if="!user" class="error-container bg-red-500/20 border border-red-500/30 text-red-400 p-6 rounded-xl">
      <h2 class="text-xl font-bold mb-2">用户不存在</h2>
      <p>无法找到ID为 {{ $route.params.id }} 的用户，请返回用户列表。</p>
      <Button label="返回用户列表" icon="pi pi-arrow-left" class="p-button-outlined mt-4" @click="$router.push({ name: 'AdminUsers' })" />
    </div>

    <div v-else class="user-detail-container grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 用户基本信息 -->
      <div class="user-profile bg-gray-800 rounded-xl p-6 lg:col-span-1">
        <div class="text-center mb-6">
          <Avatar :image="user.avatar" size="xlarge" class="w-32 h-32 mb-4" />
          <h2 class="text-xl font-bold text-white">{{ user.name }}</h2>
          <p class="text-gray-400">{{ user.email }}</p>

          <div class="mt-4 flex justify-center">
            <Tag :value="user.role" :severity="getRoleSeverity(user.role)" class="mr-2" />
            <Tag :value="user.status" :severity="getStatusSeverity(user.status)" />
          </div>
        </div>

        <div class="user-stats space-y-4">
          <div class="stat">
            <div class="flex justify-between items-center mb-1">
              <span class="text-sm text-gray-400">注册时间</span>
              <span class="text-xs text-gray-500">{{ user.createdAt }}</span>
            </div>
            <div class="text-white">{{ formatDate(user.createdAt) }}</div>
          </div>

          <div class="stat">
            <div class="flex justify-between items-center mb-1">
              <span class="text-sm text-gray-400">最后登录</span>
              <span class="text-xs text-gray-500">{{ formatTimeAgo(user.lastLogin) }}</span>
            </div>
            <div class="text-white">{{ user.lastLogin }}</div>
          </div>

          <div class="stat">
            <div class="flex justify-between items-center mb-1">
              <span class="text-sm text-gray-400">用户ID</span>
            </div>
            <div class="text-white">#{{ user.id }}</div>
          </div>
        </div>

        <div class="mt-6 pt-6 border-t border-gray-700">
          <h3 class="text-lg font-medium text-white mb-4">快速操作</h3>
          <div class="grid grid-cols-2 gap-2">
            <Button label="重置密码" icon="pi pi-lock" class="p-button-outlined p-button-sm" @click="resetPassword" />
            <Button :label="user.status === 'active' ? '禁用账户' : '启用账户'"
                  :icon="user.status === 'active' ? 'pi pi-ban' : 'pi pi-check'"
                  :class="user.status === 'active' ? 'p-button-danger p-button-sm' : 'p-button-success p-button-sm'"
                  @click="toggleUserStatus" />
            <Button label="登录记录" icon="pi pi-history" class="p-button-outlined p-button-sm" @click="viewLoginHistory" />
            <Button label="发送通知" icon="pi pi-envelope" class="p-button-outlined p-button-sm" @click="openSendNotification" />
          </div>
        </div>
      </div>

      <!-- 用户详细信息和活动 -->
      <div class="user-details bg-gray-800 rounded-xl p-6 lg:col-span-2">
        <TabView>
          <!-- 个人资料选项卡 -->
          <TabPanel header="个人资料">
            <div class="profile-details space-y-6">
              <div class="profile-section">
                <h3 class="text-lg font-medium text-white mb-4">基本信息</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div class="field">
                    <label class="block text-sm text-gray-400 mb-1">姓名</label>
                    <div class="text-white">{{ user.name }}</div>
                  </div>
                  <div class="field">
                    <label class="block text-sm text-gray-400 mb-1">邮箱</label>
                    <div class="text-white">{{ user.email }}</div>
                  </div>
                  <div class="field">
                    <label class="block text-sm text-gray-400 mb-1">手机号</label>
                    <div class="text-white">{{ user.phone || '未设置' }}</div>
                  </div>
                  <div class="field">
                    <label class="block text-sm text-gray-400 mb-1">生日</label>
                    <div class="text-white">{{ user.birthday || '未设置' }}</div>
                  </div>
                  <div class="field">
                    <label class="block text-sm text-gray-400 mb-1">性别</label>
                    <div class="text-white">{{ user.gender || '未设置' }}</div>
                  </div>
                  <div class="field">
                    <label class="block text-sm text-gray-400 mb-1">地区</label>
                    <div class="text-white">{{ user.location || '未设置' }}</div>
                  </div>
                </div>
              </div>

              <div class="profile-section">
                <h3 class="text-lg font-medium text-white mb-4">账户信息</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div class="field">
                    <label class="block text-sm text-gray-400 mb-1">账户类型</label>
                    <div class="text-white">{{ user.accountType || '标准账户' }}</div>
                  </div>
                  <div class="field">
                    <label class="block text-sm text-gray-400 mb-1">会员等级</label>
                    <div class="text-white">{{ user.membershipLevel || '普通会员' }}</div>
                  </div>
                  <div class="field">
                    <label class="block text-sm text-gray-400 mb-1">会员到期</label>
                    <div class="text-white">{{ user.membershipExpiry || '无会员' }}</div>
                  </div>
                  <div class="field">
                    <label class="block text-sm text-gray-400 mb-1">账户余额</label>
                    <div class="text-white">¥{{ user.balance || '0.00' }}</div>
                  </div>
                </div>
              </div>

              <div class="profile-section">
                <h3 class="text-lg font-medium text-white mb-4">安全信息</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div class="field">
                    <label class="block text-sm text-gray-400 mb-1">邮箱验证</label>
                    <div class="text-white">{{ user.emailVerified ? '已验证' : '未验证' }}</div>
                  </div>
                  <div class="field">
                    <label class="block text-sm text-gray-400 mb-1">手机验证</label>
                    <div class="text-white">{{ user.phoneVerified ? '已验证' : '未验证' }}</div>
                  </div>
                  <div class="field">
                    <label class="block text-sm text-gray-400 mb-1">两步验证</label>
                    <div class="text-white">{{ user.twoFactorEnabled ? '已启用' : '未启用' }}</div>
                  </div>
                  <div class="field">
                    <label class="block text-sm text-gray-400 mb-1">最后密码修改</label>
                    <div class="text-white">{{ user.lastPasswordChange || '未知' }}</div>
                  </div>
                </div>
              </div>
            </div>
          </TabPanel>

          <!-- 活动记录选项卡 -->
          <TabPanel header="活动记录">
            <div class="activities space-y-4">
              <div v-for="(activity, index) in userActivities" :key="index" class="activity flex gap-4">
                <div class="activity-icon w-10 h-10 rounded-full flex items-center justify-center" :style="{ backgroundColor: activity.iconBg }">
                  <i :class="activity.icon + ' text-sm'" :style="{ color: activity.iconColor }"></i>
                </div>

                <div class="flex-1">
                  <div class="flex justify-between">
                    <h4 class="font-medium text-white">{{ activity.title }}</h4>
                    <span class="text-xs text-gray-500">{{ activity.time }}</span>
                  </div>
                  <p class="text-sm text-gray-400">{{ activity.description }}</p>
                </div>
              </div>

              <div v-if="userActivities.length === 0" class="text-center py-8">
                <i class="pi pi-history text-4xl text-gray-600 mb-4"></i>
                <p class="text-gray-400">暂无活动记录</p>
              </div>
            </div>
          </TabPanel>

          <!-- 统计数据选项卡 -->
          <TabPanel header="统计数据">
            <div class="stats-container">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div class="stat-card bg-gray-700/30 rounded-lg p-4">
                  <h3 class="text-lg font-medium text-white mb-2">AI互动次数</h3>
                  <div class="text-3xl font-bold text-cyan-400">{{ userStats.aiInteractions || 0 }}</div>
                  <div class="text-xs text-gray-400 mt-1">过去30天: {{ userStats.aiInteractionsLast30Days || 0 }}</div>
                </div>

                <div class="stat-card bg-gray-700/30 rounded-lg p-4">
                  <h3 class="text-lg font-medium text-white mb-2">元宇宙访问</h3>
                  <div class="text-3xl font-bold text-purple-400">{{ userStats.metaverseVisits || 0 }}</div>
                  <div class="text-xs text-gray-400 mt-1">过去30天: {{ userStats.metaverseVisitsLast30Days || 0 }}</div>
                </div>

                <div class="stat-card bg-gray-700/30 rounded-lg p-4">
                  <h3 class="text-lg font-medium text-white mb-2">在线时长</h3>
                  <div class="text-3xl font-bold text-pink-400">{{ formatHours(userStats.onlineHours || 0) }}</div>
                  <div class="text-xs text-gray-400 mt-1">过去30天: {{ formatHours(userStats.onlineHoursLast30Days || 0) }}</div>
                </div>

                <div class="stat-card bg-gray-700/30 rounded-lg p-4">
                  <h3 class="text-lg font-medium text-white mb-2">消费金额</h3>
                  <div class="text-3xl font-bold text-amber-400">¥{{ userStats.totalSpent || '0.00' }}</div>
                  <div class="text-xs text-gray-400 mt-1">过去30天: ¥{{ userStats.spentLast30Days || '0.00' }}</div>
                </div>
              </div>

              <!-- 这里将来放置用户统计图表 -->
              <div class="stats-chart bg-gray-700/30 rounded-lg p-4 h-64 flex items-center justify-center">
                <p class="text-gray-400">用户活动趋势图表</p>
              </div>
            </div>
          </TabPanel>
        </TabView>
      </div>
    </div>

    <!-- 删除确认对话框 -->
    <Dialog
      v-model:visible="deleteUserDialog"
      :style="{ width: '450px' }"
      header="确认删除"
      :modal="true"
    >
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle text-yellow-500 text-2xl mr-2"></i>
        <span v-if="user">您确定要删除用户 <b>{{ user.name }}</b> 吗?</span>
      </div>
      <template #footer>
        <Button label="否" icon="pi pi-times" class="p-button-text" @click="deleteUserDialog = false" />
        <Button label="是" icon="pi pi-check" class="p-button-danger" @click="deleteUser" />
      </template>
    </Dialog>

    <!-- 发送通知对话框 -->
    <Dialog
      v-model:visible="sendNotificationDialog"
      :style="{ width: '500px' }"
      header="发送通知"
      :modal="true"
    >
      <div class="notification-form space-y-4">
        <div class="form-group">
          <label for="notificationTitle" class="block text-sm font-medium text-gray-300 mb-2">通知标题</label>
          <InputText id="notificationTitle" v-model="notification.title" class="w-full" />
        </div>

        <div class="form-group">
          <label for="notificationMessage" class="block text-sm font-medium text-gray-300 mb-2">通知内容</label>
          <Textarea id="notificationMessage" v-model="notification.message" rows="5" class="w-full" />
        </div>

        <div class="form-group">
          <label for="notificationType" class="block text-sm font-medium text-gray-300 mb-2">通知类型</label>
          <Dropdown
            id="notificationType"
            v-model="notification.type"
            :options="notificationTypes"
            optionLabel="label"
            optionValue="value"
            placeholder="选择通知类型"
            class="w-full"
          />
        </div>
      </div>
      <template #footer>
        <Button label="取消" icon="pi pi-times" class="p-button-text" @click="sendNotificationDialog = false" />
        <Button label="发送" icon="pi pi-send" @click="sendNotification" />
      </template>
    </Dialog>
  </div>
</template>

<script>
import UserDetailViews from '@/server/view/admin/users/UserDetailViews'
</script>

<style lang="scss" scoped>
@use '../../../styles/view/admin/dashboard.scss'
</style>
