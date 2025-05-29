<template>
  <div class="admin-dashboard">
    <div class="dashboard-stats">
      <div class="stat-card">
        <div class="stat-icon">
          <i class="pi pi-users"></i>
        </div>
        <div class="stat-content">
          <h3>总用户数</h3>
          <div class="stat-value">{{ stats.totalUsers }}</div>
          <div class="stat-trend" :class="{ 'positive': stats.userGrowth > 0, 'negative': stats.userGrowth < 0 }">
            <i :class="stats.userGrowth > 0 ? 'pi pi-arrow-up' : 'pi pi-arrow-down'"></i>
            <span>{{ Math.abs(stats.userGrowth) }}% 较上月</span>
          </div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <i class="pi pi-comments"></i>
        </div>
        <div class="stat-content">
          <h3>AI对话数</h3>
          <div class="stat-value">{{ stats.totalConversations }}</div>
          <div class="stat-trend" :class="{ 'positive': stats.conversationGrowth > 0, 'negative': stats.conversationGrowth < 0 }">
            <i :class="stats.conversationGrowth > 0 ? 'pi pi-arrow-up' : 'pi pi-arrow-down'"></i>
            <span>{{ Math.abs(stats.conversationGrowth) }}% 较上月</span>
          </div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <i class="pi pi-globe"></i>
        </div>
        <div class="stat-content">
          <h3>活跃空间数</h3>
          <div class="stat-value">{{ stats.activeSpaces }}</div>
          <div class="stat-trend" :class="{ 'positive': stats.spaceGrowth > 0, 'negative': stats.spaceGrowth < 0 }">
            <i :class="stats.spaceGrowth > 0 ? 'pi pi-arrow-up' : 'pi pi-arrow-down'"></i>
            <span>{{ Math.abs(stats.spaceGrowth) }}% 较上月</span>
          </div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <i class="pi pi-clock"></i>
        </div>
        <div class="stat-content">
          <h3>平均使用时长</h3>
          <div class="stat-value">{{ stats.avgUsageTime }}分钟</div>
          <div class="stat-trend" :class="{ 'positive': stats.usageTimeGrowth > 0, 'negative': stats.usageTimeGrowth < 0 }">
            <i :class="stats.usageTimeGrowth > 0 ? 'pi pi-arrow-up' : 'pi pi-arrow-down'"></i>
            <span>{{ Math.abs(stats.usageTimeGrowth) }}% 较上月</span>
          </div>
        </div>
      </div>
    </div>

    <div class="dashboard-charts">
      <div class="chart-card">
        <div class="chart-header">
          <h3>用户增长趋势</h3>
          <div class="chart-actions">
            <Dropdown v-model="selectedPeriod" :options="chartPeriods" optionLabel="name" class="mr-2" />
            <Button icon="pi pi-download" class="p-button-text p-button-rounded" @click="downloadChart('userGrowth')" />
          </div>
        </div>
        <div class="chart-content">
          <canvas ref="userGrowthChart"></canvas>
        </div>
      </div>

      <div class="chart-card">
        <div class="chart-header">
          <h3>活跃用户分布</h3>
          <div class="chart-actions">
            <Button icon="pi pi-download" class="p-button-text p-button-rounded" @click="downloadChart('activeUsers')" />
          </div>
        </div>
        <div class="chart-content">
          <canvas ref="activeUsersChart"></canvas>
        </div>
      </div>
    </div>

    <div class="dashboard-tables">
      <div class="table-card">
        <div class="table-header">
          <h3>最近注册用户</h3>
          <Button label="查看全部" icon="pi pi-arrow-right" class="p-button-text" @click="goToUsers" />
        </div>
        <DataTable :value="recentUsers" :paginator="false" :rows="5" stripedRows>
          <Column field="id" header="ID" style="width: 5%"></Column>
          <Column field="username" header="用户名" style="width: 20%">
            <template #body="slotProps">
              <div class="user-cell">
                <Avatar :image="slotProps.data.avatar" shape="circle" />
                <span>{{ slotProps.data.username }}</span>
              </div>
            </template>
          </Column>
          <Column field="email" header="邮箱" style="width: 25%"></Column>
          <Column field="registerDate" header="注册日期" style="width: 20%"></Column>
          <Column field="status" header="状态" style="width: 15%">
            <template #body="slotProps">
              <Tag :value="slotProps.data.status" :severity="getStatusSeverity(slotProps.data.status)" />
            </template>
          </Column>
          <Column header="操作" style="width: 15%">
            <template #body="slotProps">
              <Button icon="pi pi-eye" class="p-button-rounded p-button-text" @click="viewUser(slotProps.data.id)" />
              <Button icon="pi pi-pencil" class="p-button-rounded p-button-text" @click="editUser(slotProps.data.id)" />
            </template>
          </Column>
        </DataTable>
      </div>

      <div class="table-card">
        <div class="table-header">
          <h3>系统通知</h3>
          <Button label="创建通知" icon="pi pi-plus" class="p-button-text" @click="createNotification" />
        </div>
        <DataTable :value="systemNotifications" :paginator="false" :rows="5" stripedRows>
          <Column field="id" header="ID" style="width: 5%"></Column>
          <Column field="title" header="标题" style="width: 30%"></Column>
          <Column field="type" header="类型" style="width: 15%">
            <template #body="slotProps">
              <Tag :value="slotProps.data.type" :severity="getNotificationSeverity(slotProps.data.type)" />
            </template>
          </Column>
          <Column field="date" header="发布日期" style="width: 20%"></Column>
          <Column field="status" header="状态" style="width: 15%">
            <template #body="slotProps">
              <Tag :value="slotProps.data.status" :severity="getStatusSeverity(slotProps.data.status)" />
            </template>
          </Column>
          <Column header="操作" style="width: 15%">
            <template #body="slotProps">
              <Button icon="pi pi-eye" class="p-button-rounded p-button-text" @click="viewNotification(slotProps.data.id)" />
              <Button icon="pi pi-pencil" class="p-button-rounded p-button-text" @click="editNotification(slotProps.data.id)" />
            </template>
          </Column>
        </DataTable>
      </div>
    </div>

    <Dialog v-model:visible="notificationDialog" :header="notificationDialogMode === 'create' ? '创建通知' : '编辑通知'" :style="{ width: '500px' }" :modal="true">
      <div class="p-fluid">
        <div class="p-field mb-3">
          <label for="title">标题</label>
          <InputText id="title" v-model="notification.title" required />
        </div>
        <div class="p-field mb-3">
          <label for="content">内容</label>
          <Textarea id="content" v-model="notification.content" rows="5" required />
        </div>
        <div class="p-field mb-3">
          <label for="type">类型</label>
          <Dropdown id="type" v-model="notification.type" :options="notificationTypes" optionLabel="name" placeholder="选择类型" required />
        </div>
        <div class="p-field mb-3">
          <label for="status">状态</label>
          <Dropdown id="status" v-model="notification.status" :options="notificationStatuses" optionLabel="name" placeholder="选择状态" required />
        </div>
      </div>
      <template #footer>
        <Button label="取消" icon="pi pi-times" class="p-button-text" @click="notificationDialog = false" />
        <Button label="保存" icon="pi pi-check" @click="saveNotification" :loading="submitting" />
      </template>
    </Dialog>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminDashboard } from './composables/useAdminDashboard'

export default {
  name: 'DashboardView',
  setup() {
    const router = useRouter()
    const {
      stats,
      recentUsers,
      systemNotifications,
      loading,
      charts,
      chartPeriods,
      selectedPeriod,
      getAllDashboardData,
      initCharts,
      createNotification: apiCreateNotification,
      getNotificationDetail,
      updateNotification: apiUpdateNotification,
      getStatusSeverity,
      getNotificationSeverity
    } = useAdminDashboard()

    // 图表引用
    const userGrowthChart = ref(null)
    const activeUsersChart = ref(null)

    // 通知对话框
    const notificationDialog = ref(false)
    const notificationDialogMode = ref('create')
    const submitting = ref(false)
    const notification = ref({
      title: '',
      content: '',
      type: null,
      status: null
    })

    // 通知类型选项
    const notificationTypes = [
      { name: '系统', value: 'system' },
      { name: '更新', value: 'update' },
      { name: '警告', value: 'warning' },
      { name: '错误', value: 'error' }
    ]

    // 通知状态选项
    const notificationStatuses = [
      { name: '活跃', value: 'active' },
      { name: '草稿', value: 'draft' },
      { name: '已过期', value: 'expired' }
    ]

    // 获取仪表盘数据
    const fetchDashboardData = async () => {
      const response = await getAllDashboardData()
      if (response && response.charts) {
        initCharts(response.charts, userGrowthChart.value, activeUsersChart.value)
      }
    }

    // 查看用户列表
    const goToUsers = () => {
      router.push('/admin/users')
    }

    // 查看用户详情
    const viewUser = (userId) => {
      router.push(`/admin/users/${userId}`)
    }

    // 编辑用户
    const editUser = (userId) => {
      router.push(`/admin/users/${userId}/edit`)
    }

    // 下载图表
    const downloadChart = (chartId) => {
      if (charts[chartId]) {
        const link = document.createElement('a')
        link.download = `${chartId}-chart.png`
        link.href = charts[chartId].toBase64Image()
        link.click()
      }
    }

    // 创建通知
    const createNotification = () => {
      notificationDialogMode.value = 'create'
      notification.value = {
        title: '',
        content: '',
        type: null,
        status: notificationStatuses[0]
      }
      notificationDialog.value = true
    }

    // 查看通知详情
    const viewNotification = async (notificationId) => {
      const detail = await getNotificationDetail(notificationId)
      if (detail) {
        router.push(`/admin/notifications/${notificationId}`)
      }
    }

    // 编辑通知
    const editNotification = async (notificationId) => {
      submitting.value = true
      try {
        const detail = await getNotificationDetail(notificationId)
        if (detail) {
          notification.value = {
            id: detail.id,
            title: detail.title,
            content: detail.content,
            type: notificationTypes.find(t => t.value === detail.type),
            status: notificationStatuses.find(s => s.value === detail.status)
          }
          notificationDialogMode.value = 'edit'
          notificationDialog.value = true
        }
      } finally {
        submitting.value = false
      }
    }

    // 保存通知
    const saveNotification = async () => {
      submitting.value = true
      try {
        const data = {
          title: notification.value.title,
          content: notification.value.content,
          type: notification.value.type?.value,
          status: notification.value.status?.value
        }

        if (notificationDialogMode.value === 'create') {
          await apiCreateNotification(data)
        } else {
          await apiUpdateNotification(notification.value.id, data)
        }

        notificationDialog.value = false
        await fetchDashboardData()
      } finally {
        submitting.value = false
      }
    }

    // 监听周期变化
    watch(selectedPeriod, async () => {
      await fetchDashboardData()
    })

    // 初始化
    onMounted(() => {
      fetchDashboardData()
    })

    return {
      stats,
      recentUsers,
      systemNotifications,
      loading,
      userGrowthChart,
      activeUsersChart,
      chartPeriods,
      selectedPeriod,
      notificationDialog,
      notificationDialogMode,
      submitting,
      notification,
      notificationTypes,
      notificationStatuses,
      goToUsers,
      viewUser,
      editUser,
      downloadChart,
      createNotification,
      viewNotification,
      editNotification,
      saveNotification,
      getStatusSeverity,
      getNotificationSeverity
    }
  }
}
</script>

<style lang="scss" scoped>
.admin-dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;

  .stat-card {
    background: #ffffff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    display: flex;
    align-items: center;

    .stat-icon {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 16px;

      i {
        font-size: 1.8rem;
      }
    }

    &:nth-child(1) .stat-icon {
      background-color: rgba(76, 175, 80, 0.1);
      color: #4CAF50;
    }

    &:nth-child(2) .stat-icon {
      background-color: rgba(33, 150, 243, 0.1);
      color: #2196F3;
    }

    &:nth-child(3) .stat-icon {
      background-color: rgba(156, 39, 176, 0.1);
      color: #9C27B0;
    }

    &:nth-child(4) .stat-icon {
      background-color: rgba(255, 152, 0, 0.1);
      color: #FF9800;
    }

    .stat-content {
      flex: 1;

      h3 {
        margin: 0;
        font-size: 0.9rem;
        font-weight: 500;
        color: #666;
      }

      .stat-value {
        font-size: 1.8rem;
        font-weight: 600;
        margin: 8px 0;
      }

      .stat-trend {
        display: flex;
        align-items: center;
        font-size: 0.8rem;

        i {
          margin-right: 4px;
        }

        &.positive {
          color: #4CAF50;
        }

        &.negative {
          color: #F44336;
        }
      }
    }
  }
}

.dashboard-charts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 24px;

  .chart-card {
    background: #ffffff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);

    .chart-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;

      h3 {
        margin: 0;
        font-size: 1.1rem;
        font-weight: 600;
      }

      .chart-actions {
        display: flex;
        align-items: center;
      }
    }

    .chart-content {
      height: 300px;
      position: relative;
    }
  }
}

.dashboard-tables {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 24px;

  .table-card {
    background: #ffffff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);

    .table-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;

      h3 {
        margin: 0;
        font-size: 1.1rem;
        font-weight: 600;
      }
    }
  }
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
