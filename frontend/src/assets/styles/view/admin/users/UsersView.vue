<template>
  <div class="admin-users">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-white">用户管理</h1>
      <div class="flex gap-2">
        <Button label="新增用户" icon="pi pi-plus" @click="openNewUserDialog" />
        <Button label="导出数据" icon="pi pi-download" class="p-button-outlined" @click="exportUserData" />
      </div>
    </div>

    <!-- 搜索和筛选工具栏 -->
    <div class="filters bg-gray-800 p-4 rounded-xl mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="search-box">
          <span class="p-input-icon-left w-full">
            <i class="pi pi-search" />
            <InputText v-model="filters.search" placeholder="搜索用户..." class="w-full" />
          </span>
        </div>

        <div class="filter-item">
          <Dropdown
            v-model="filters.role"
            :options="roleOptions"
            placeholder="角色"
            class="w-full"
            optionLabel="label"
            optionValue="value"
          />
        </div>

        <div class="filter-item">
          <Dropdown
            v-model="filters.status"
            :options="statusOptions"
            placeholder="状态"
            class="w-full"
            optionLabel="label"
            optionValue="value"
          />
        </div>

        <div class="filter-actions flex justify-end">
          <Button label="重置" icon="pi pi-refresh" class="p-button-text" @click="resetFilters" />
          <Button label="筛选" icon="pi pi-filter" class="ml-2" @click="applyFilters" />
        </div>
      </div>
    </div>

    <!-- 用户数据表格 -->
    <div class="users-table bg-gray-800 rounded-xl overflow-hidden">
      <DataTable
        :value="users"
        :paginator="true"
        :rows="10"
        :loading="loading"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        :rowsPerPageOptions="[10, 20, 50]"
        currentPageReportTemplate="显示第 {first} 至 {last} 条，共 {totalRecords} 条"
        responsiveLayout="scroll"
        stripedRows
        v-model:selection="selectedUsers"
        :filters="tableFilters"
        filterDisplay="menu"
      >
        <template #empty>
          <div class="text-center p-4">
            <p class="text-gray-400">暂无用户数据</p>
          </div>
        </template>

        <template #loading>
          <div class="text-center p-4">
            <ProgressSpinner style="width:50px;height:50px" />
            <p class="text-gray-400 mt-2">加载用户数据...</p>
          </div>
        </template>

        <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>

        <Column field="id" header="ID" sortable style="width: 5rem">
          <template #body="{ data }">
            <span class="text-gray-400">#{{ data.id }}</span>
          </template>
        </Column>

        <Column field="name" header="用户名" sortable>
          <template #body="{ data }">
            <div class="flex items-center">
              <Avatar :image="data.avatar" class="mr-2" size="small" />
              <div>
                <div class="font-medium text-white">{{ data.name }}</div>
                <div class="text-xs text-gray-400">{{ data.email }}</div>
              </div>
            </div>
          </template>
        </Column>

        <Column field="role" header="角色" sortable style="width: 10rem">
          <template #body="{ data }">
            <Tag :value="data.role" :severity="getRoleSeverity(data.role)" />
          </template>
        </Column>

        <Column field="status" header="状态" sortable style="width: 10rem">
          <template #body="{ data }">
            <Tag :value="data.status" :severity="getStatusSeverity(data.status)" />
          </template>
        </Column>

        <Column field="lastLogin" header="最后登录" sortable>
          <template #body="{ data }">
            <span class="text-gray-400">{{ data.lastLogin }}</span>
          </template>
        </Column>

        <Column field="createdAt" header="注册时间" sortable>
          <template #body="{ data }">
            <span class="text-gray-400">{{ data.createdAt }}</span>
          </template>
        </Column>

        <Column header="操作" style="width: 8rem">
          <template #body="{ data }">
            <div class="flex gap-2">
              <Button
                icon="pi pi-pencil"
                class="p-button-rounded p-button-text p-button-sm"
                @click="editUser(data)"
                tooltip="编辑"
                tooltipOptions="{ position: 'top' }"
              />
              <Button
                icon="pi pi-eye"
                class="p-button-rounded p-button-text p-button-sm"
                @click="viewUserDetails(data)"
                tooltip="查看"
                tooltipOptions="{ position: 'top' }"
              />
              <Button
                icon="pi pi-trash"
                class="p-button-rounded p-button-text p-button-danger p-button-sm"
                @click="confirmDeleteUser(data)"
                tooltip="删除"
                tooltipOptions="{ position: 'top' }"
              />
            </div>
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- 批量操作工具栏 -->
    <div v-if="selectedUsers.length > 0" class="bulk-actions bg-gray-800 p-3 rounded-xl mt-4 flex justify-between items-center">
      <span class="text-gray-300">已选择 {{ selectedUsers.length }} 个用户</span>
      <div class="flex gap-2">
        <Button label="批量删除" icon="pi pi-trash" class="p-button-danger p-button-sm" @click="confirmDeleteSelected" />
        <Button label="批量导出" icon="pi pi-download" class="p-button-outlined p-button-sm" @click="exportSelected" />
        <Button label="取消选择" icon="pi pi-times" class="p-button-text p-button-sm" @click="clearSelection" />
      </div>
    </div>

    <!-- 新增/编辑用户对话框 -->
    <Dialog
      v-model:visible="userDialog"
      :style="{ width: '450px' }"
      :header="editingUser.id ? '编辑用户' : '新增用户'"
      :modal="true"
      class="p-fluid"
    >
      <div class="user-form space-y-4">
        <div class="form-group">
          <label for="name" class="block text-sm font-medium text-gray-300 mb-2">用户名</label>
          <InputText id="name" v-model="editingUser.name" required autofocus />
        </div>

        <div class="form-group">
          <label for="email" class="block text-sm font-medium text-gray-300 mb-2">邮箱</label>
          <InputText id="email" v-model="editingUser.email" required type="email" />
        </div>

        <div class="form-group" v-if="!editingUser.id">
          <label for="password" class="block text-sm font-medium text-gray-300 mb-2">密码</label>
          <Password id="password" v-model="editingUser.password" toggleMask />
        </div>

        <div class="form-group">
          <label for="role" class="block text-sm font-medium text-gray-300 mb-2">角色</label>
          <Dropdown
            id="role"
            v-model="editingUser.role"
            :options="roleOptions"
            optionLabel="label"
            optionValue="value"
            placeholder="选择角色"
          />
        </div>

        <div class="form-group">
          <label for="status" class="block text-sm font-medium text-gray-300 mb-2">状态</label>
          <Dropdown
            id="status"
            v-model="editingUser.status"
            :options="statusOptions"
            optionLabel="label"
            optionValue="value"
            placeholder="选择状态"
          />
        </div>
      </div>

      <template #footer>
        <Button label="取消" icon="pi pi-times" class="p-button-text" @click="hideDialog" />
        <Button label="保存" icon="pi pi-check" @click="saveUser" />
      </template>
    </Dialog>

    <!-- 删除确认对话框 -->
    <Dialog
      v-model:visible="deleteUserDialog"
      :style="{ width: '450px' }"
      header="确认删除"
      :modal="true"
    >
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle text-yellow-500 text-2xl mr-2"></i>
        <span v-if="editingUser">您确定要删除用户 <b>{{ editingUser.name }}</b> 吗?</span>
      </div>
      <template #footer>
        <Button label="否" icon="pi pi-times" class="p-button-text" @click="deleteUserDialog = false" />
        <Button label="是" icon="pi pi-check" class="p-button-danger" @click="deleteUser" />
      </template>
    </Dialog>

    <!-- 批量删除确认对话框 -->
    <Dialog
      v-model:visible="deleteUsersDialog"
      :style="{ width: '450px' }"
      header="确认删除"
      :modal="true"
    >
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle text-yellow-500 text-2xl mr-2"></i>
        <span>您确定要删除选中的 {{ selectedUsers.length }} 个用户吗?</span>
      </div>
      <template #footer>
        <Button label="否" icon="pi pi-times" class="p-button-text" @click="deleteUsersDialog = false" />
        <Button label="是" icon="pi pi-check" class="p-button-danger" @click="deleteSelectedUsers" />
      </template>
    </Dialog>
  </div>
</template>

<script>
import UsersViews from '@/server/view/admin/users/UsersViews'
</script>

<style lang="scss" scoped>
.admin-users {
  :deep(.p-datatable) {
    background-color: transparent;

    .p-datatable-header {
      background-color: #1e1e2d;
      border: none;
    }

    .p-datatable-thead > tr > th {
      background-color: #1e1e2d;
      color: white;
      border-color: rgba(255, 255, 255, 0.1);
    }

    .p-datatable-tbody > tr {
      background-color: #1e1e2d;
      color: white;

      &:nth-child(even) {
        background-color: #252538;
      }

      &:hover {
        background-color: #2a2a42;
      }

      > td {
        border-color: rgba(255, 255, 255, 0.05);
      }
    }

    .p-paginator {
      background-color: #1e1e2d;
      border: none;
      color: white;

      .p-paginator-element {
        color: white;

        &:hover {
          background-color: rgba(255, 255, 255, 0.1);
        }

        &.p-highlight {
          background-color: rgba(6, 182, 212, 0.2);
          color: #06b6d4;
        }
      }
    }
  }

  :deep(.p-dropdown) {
    background-color: #1e1e2d;
    border-color: rgba(255, 255, 255, 0.1);

    .p-dropdown-label {
      color: white;
    }

    .p-dropdown-trigger {
      color: white;
    }
  }

  :deep(.p-inputtext) {
    background-color: #1e1e2d;
    border-color: rgba(255, 255, 255, 0.1);
    color: white;

    &:hover {
      border-color: rgba(255, 255, 255, 0.2);
    }

    &:focus {
      border-color: #06b6d4;
      box-shadow: 0 0 0 1px rgba(6, 182, 212, 0.2);
    }
  }

  :deep(.p-dialog) {
    .p-dialog-header {
      background-color: #1e1e2d;
      color: white;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .p-dialog-content {
      background-color: #1e1e2d;
      color: white;
    }

    .p-dialog-footer {
      background-color: #1e1e2d;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
  }
}
</style>
