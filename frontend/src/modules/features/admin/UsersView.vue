<template>
  <div class="users-view">
    <div class="users-header">
      <div class="header-left">
        <h2>用户管理</h2>
        <p>管理系统中的所有用户账号</p>
      </div>
      <div class="header-right">
        <Button label="创建用户" icon="pi pi-plus" @click="openNewUserDialog" />
      </div>
    </div>

    <div class="users-filters">
      <div class="filter-group">
        <span class="p-input-icon-left">
          <i class="pi pi-search" />
          <InputText v-model="filters.search" placeholder="搜索用户..." class="search-input" />
        </span>
      </div>

      <div class="filter-group">
        <Dropdown v-model="filters.status" :options="statusOptions" optionLabel="name" placeholder="状态" class="filter-dropdown" />
      </div>

      <div class="filter-group">
        <Dropdown v-model="filters.role" :options="roleOptions" optionLabel="name" placeholder="角色" class="filter-dropdown" />
      </div>

      <div class="filter-group">
        <Button icon="pi pi-filter" label="更多筛选" @click="showFilterSidebar = true" class="p-button-outlined" />
      </div>

      <div class="filter-group ml-auto">
        <Button icon="pi pi-refresh" @click="resetFilters" class="p-button-text" />
      </div>
    </div>

    <div class="users-table">
      <DataTable
        :value="usersList"
        :paginator="true"
        :rows="pagination.pageSize"
        :rowsPerPageOptions="[5, 10, 20, 50]"
        v-model:selection="selectedUsers"
        :loading="loading"
        stripedRows
        responsiveLayout="scroll"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        currentPageReportTemplate="显示第 {first} 到 {last} 条，共 {totalRecords} 条"
        :totalRecords="totalUsers"
        :lazy="true"
        @page="onPage"
      >
        <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
        <Column field="id" header="ID" sortable style="width: 5%"></Column>
        <Column field="username" header="用户名" sortable style="width: 15%">
          <template #body="slotProps">
            <div class="user-cell">
              <Avatar :image="slotProps.data.avatar" shape="circle" />
              <span>{{ slotProps.data.username }}</span>
            </div>
          </template>
        </Column>
        <Column field="email" header="邮箱" sortable style="width: 20%"></Column>
        <Column field="role" header="角色" sortable style="width: 10%">
          <template #body="slotProps">
            <Tag :value="slotProps.data.role" :severity="getRoleSeverity(slotProps.data.role)" />
          </template>
        </Column>
        <Column field="status" header="状态" sortable style="width: 10%">
          <template #body="slotProps">
            <Tag :value="slotProps.data.status" :severity="getStatusSeverity(slotProps.data.status)" />
          </template>
        </Column>
        <Column field="registerDate" header="注册日期" sortable style="width: 15%"></Column>
        <Column field="lastLogin" header="最后登录" sortable style="width: 15%"></Column>
        <Column header="操作" style="width: 10%">
          <template #body="slotProps">
            <Button icon="pi pi-eye" class="p-button-rounded p-button-text" @click="viewUser(slotProps.data.id)" />
            <Button icon="pi pi-pencil" class="p-button-rounded p-button-text" @click="editUser(slotProps.data.id)" />
            <Button icon="pi pi-trash" class="p-button-rounded p-button-text p-button-danger" @click="confirmDeleteUser(slotProps.data)" />
          </template>
        </Column>
      </DataTable>
    </div>

    <Sidebar v-model:visible="showFilterSidebar" position="right" class="filter-sidebar">
      <h3>高级筛选</h3>

      <div class="filter-section">
        <h4>注册日期</h4>
        <div class="date-range">
          <Calendar v-model="filters.dateRange[0]" placeholder="开始日期" class="w-full mb-2" />
          <Calendar v-model="filters.dateRange[1]" placeholder="结束日期" class="w-full" />
        </div>
      </div>

      <div class="filter-section">
        <h4>登录设备</h4>
        <div class="p-field-checkbox">
          <Checkbox v-model="filters.devices.desktop" :binary="true" id="desktop" />
          <label for="desktop" class="ml-2">桌面端</label>
        </div>
        <div class="p-field-checkbox">
          <Checkbox v-model="filters.devices.mobile" :binary="true" id="mobile" />
          <label for="mobile" class="ml-2">移动端</label>
        </div>
        <div class="p-field-checkbox">
          <Checkbox v-model="filters.devices.tablet" :binary="true" id="tablet" />
          <label for="tablet" class="ml-2">平板</label>
        </div>
      </div>

      <div class="filter-section">
        <h4>活跃度</h4>
        <Dropdown v-model="filters.activity" :options="activityOptions" optionLabel="name" placeholder="选择活跃度" class="w-full" />
      </div>

      <div class="filter-actions">
        <Button label="应用筛选" @click="applyFilters" class="w-full mb-2" />
        <Button label="重置" @click="resetFilters" class="w-full p-button-outlined" />
      </div>
    </Sidebar>

    <Dialog v-model:visible="newUserDialog" header="创建新用户" :style="{ width: '450px' }" :modal="true">
      <div class="p-fluid">
        <div class="p-field mb-3">
          <label for="username">用户名</label>
          <InputText id="username" v-model="newUser.username" required />
        </div>
        <div class="p-field mb-3">
          <label for="email">邮箱</label>
          <InputText id="email" v-model="newUser.email" type="email" required />
        </div>
        <div class="p-field mb-3">
          <label for="password">密码</label>
          <Password id="password" v-model="newUser.password" toggleMask required />
        </div>
        <div class="p-field mb-3">
          <label for="role">角色</label>
          <Dropdown id="role" v-model="newUser.role" :options="roleOptions" optionLabel="name" placeholder="选择角色" required />
        </div>
        <div class="p-field mb-3">
          <label for="status">状态</label>
          <Dropdown id="status" v-model="newUser.status" :options="statusOptions" optionLabel="name" placeholder="选择状态" required />
        </div>
      </div>
      <template #footer>
        <Button label="取消" icon="pi pi-times" class="p-button-text" @click="newUserDialog = false" />
        <Button label="创建" icon="pi pi-check" @click="createUser" :loading="submitting" />
      </template>
    </Dialog>

    <Dialog v-model:visible="deleteUserDialog" header="确认删除" :style="{ width: '450px' }" :modal="true">
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span>确定要删除用户 <b>{{ userToDelete.username }}</b> 吗?</span>
      </div>
      <template #footer>
        <Button label="取消" icon="pi pi-times" class="p-button-text" @click="deleteUserDialog = false" />
        <Button label="删除" icon="pi pi-trash" class="p-button-danger" @click="deleteUser" :loading="submitting" />
      </template>
    </Dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminUsers } from './composables/useAdminUsers'

export default {
  name: 'UsersView',
  setup() {
    const router = useRouter()
    const {
      usersList,
      selectedUsers,
      loading,
      submitting,
      totalUsers,
      pagination,
      filters,
      getUsers,
      createUser: apiCreateUser,
      confirmDeleteUser,
      deleteUser: apiDeleteUser,
      applyFilters: apiApplyFilters,
      resetFilters: apiResetFilters,
      changePage,
      changePageSize
    } = useAdminUsers()

    // 侧边栏
    const showFilterSidebar = ref(false)

    // 对话框
    const newUserDialog = ref(false)
    const deleteUserDialog = ref(false)
    const userToDelete = ref({})

    // 新用户
    const newUser = reactive({
      username: '',
      email: '',
      password: '',
      role: null,
      status: null
    })

    // 选项
    const statusOptions = [
      { name: '活跃', value: 'active' },
      { name: '待验证', value: 'pending' },
      { name: '禁用', value: 'disabled' }
    ]

    const roleOptions = [
      { name: '管理员', value: 'admin' },
      { name: '高级用户', value: 'premium' },
      { name: '普通用户', value: 'user' }
    ]

    const activityOptions = [
      { name: '非常活跃', value: 'very_active' },
      { name: '活跃', value: 'active' },
      { name: '一般', value: 'moderate' },
      { name: '不活跃', value: 'inactive' }
    ]

    // 应用过滤器
    const applyFilters = () => {
      showFilterSidebar.value = false
      apiApplyFilters()
    }

    // 重置过滤器
    const resetFilters = () => {
      apiResetFilters()
      showFilterSidebar.value = false
    }

    // 查看用户详情
    const viewUser = (userId) => {
      router.push(`/admin/users/${userId}`)
    }

    // 编辑用户
    const editUser = (userId) => {
      router.push(`/admin/users/${userId}/edit`)
    }

    // 确认删除用户
    const confirmUserDelete = (user) => {
      userToDelete.value = user
      deleteUserDialog.value = true
    }

    // 删除用户
    const deleteUser = async () => {
      await apiDeleteUser(userToDelete.value.id)
      deleteUserDialog.value = false
    }

    // 打开新用户对话框
    const openNewUserDialog = () => {
      // 重置表单
      newUser.username = ''
      newUser.email = ''
      newUser.password = ''
      newUser.role = null
      newUser.status = null

      newUserDialog.value = true
    }

    // 创建用户
    const createUser = async () => {
      const result = await apiCreateUser({
        username: newUser.username,
        email: newUser.email,
        password: newUser.password,
        role: newUser.role?.value,
        status: newUser.status?.value
      })

      if (result.success) {
        newUserDialog.value = false
      }
    }

    // 分页处理
    const onPage = (event) => {
      changePage(event.page + 1)
      changePageSize(event.rows)
    }

    // 获取角色样式
    const getRoleSeverity = (role) => {
      switch (role) {
        case '管理员':
          return 'danger'
        case '高级用户':
          return 'warning'
        case '普通用户':
          return 'info'
        default:
          return 'info'
      }
    }

    // 获取状态样式
    const getStatusSeverity = (status) => {
      switch (status) {
        case '活跃':
          return 'success'
        case '待验证':
          return 'warning'
        case '禁用':
          return 'danger'
        default:
          return 'info'
      }
    }

    // 初始化
    onMounted(() => {
      getUsers()
    })

    return {
      usersList,
      selectedUsers,
      loading,
      submitting,
      totalUsers,
      pagination,
      filters,
      showFilterSidebar,
      newUserDialog,
      deleteUserDialog,
      userToDelete,
      newUser,
      statusOptions,
      roleOptions,
      activityOptions,
      applyFilters,
      resetFilters,
      viewUser,
      editUser,
      confirmDeleteUser,
      deleteUser,
      openNewUserDialog,
      createUser,
      onPage,
      getRoleSeverity,
      getStatusSeverity
    }
  }
}
</script>

<style lang="scss" scoped>
.users-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.users-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .header-left {
    h2 {
      margin: 0;
      font-size: 1.5rem;
      font-weight: 600;
    }

    p {
      margin: 4px 0 0;
      color: #666;
    }
  }
}

.users-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
  background-color: #ffffff;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);

  .filter-group {
    .search-input {
      width: 250px;
    }

    .filter-dropdown {
      width: 150px;
    }
  }

  .ml-auto {
    margin-left: auto;
  }
}

.users-table {
  background-color: #ffffff;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.filter-sidebar {
  width: 350px;
  padding: 16px;

  h3 {
    margin-top: 0;
    margin-bottom: 24px;
    font-size: 1.2rem;
    font-weight: 600;
  }

  .filter-section {
    margin-bottom: 24px;

    h4 {
      margin-top: 0;
      margin-bottom: 12px;
      font-size: 1rem;
      font-weight: 500;
    }

    .date-range {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .p-field-checkbox {
      margin-bottom: 8px;
    }
  }

  .filter-actions {
    margin-top: 32px;
  }
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.confirmation-content {
  display: flex;
  align-items: center;
  padding: 16px 0;
}
</style>
