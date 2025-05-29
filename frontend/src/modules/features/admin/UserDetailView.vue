<template>
  <div class="user-detail-view">
    <div class="detail-header">
      <div class="header-left">
        <Button icon="pi pi-arrow-left" class="p-button-text" @click="goBack" />
        <h2>用户详情</h2>
      </div>
      <div class="header-right">
        <Button label="编辑" icon="pi pi-pencil" class="p-button-outlined mr-2" @click="editMode = !editMode" />
        <Button label="删除" icon="pi pi-trash" class="p-button-danger p-button-outlined" @click="confirmDelete" />
      </div>
    </div>

    <div class="detail-content" v-if="!loading">
      <div class="user-profile">
        <div class="profile-header">
          <div class="profile-avatar">
            <Avatar :image="userDetail.avatar || '/img/default-avatar.png'" size="xlarge" shape="circle" />
            <div class="avatar-upload" v-if="editMode">
              <Button icon="pi pi-camera" class="p-button-rounded p-button-sm" @click="triggerFileInput" />
              <input type="file" ref="fileInput" style="display: none" @change="uploadAvatar" accept="image/*" />
            </div>
          </div>
          <div class="profile-info">
            <div class="profile-name" v-if="!editMode">{{ userDetail.username }}</div>
            <InputText v-else v-model="editedUser.username" class="profile-name-input" />

            <div class="profile-meta">
              <span class="meta-item">
                <i class="pi pi-envelope"></i>
                <span v-if="!editMode">{{ userDetail.email }}</span>
                <InputText v-else v-model="editedUser.email" class="meta-input" />
              </span>
              <span class="meta-item">
                <i class="pi pi-id-card"></i>
                <Tag v-if="!editMode" :value="userDetail.role" :severity="getRoleSeverity(userDetail.role)" />
                <Dropdown v-else v-model="editedUser.role" :options="roleOptions" optionLabel="name" class="meta-input" />
              </span>
              <span class="meta-item">
                <i class="pi pi-circle"></i>
                <Tag v-if="!editMode" :value="userDetail.status" :severity="getStatusSeverity(userDetail.status)" />
                <Dropdown v-else v-model="editedUser.status" :options="statusOptions" optionLabel="name" class="meta-input" />
              </span>
            </div>
          </div>
        </div>

        <TabView>
          <TabPanel header="基本信息">
            <div class="profile-details">
              <div class="detail-row">
                <div class="detail-label">用户ID</div>
                <div class="detail-value">{{ userDetail.id }}</div>
              </div>
              <div class="detail-row">
                <div class="detail-label">注册日期</div>
                <div class="detail-value">{{ userDetail.registerDate }}</div>
              </div>
              <div class="detail-row">
                <div class="detail-label">最后登录</div>
                <div class="detail-value">{{ userDetail.lastLogin }}</div>
              </div>
              <div class="detail-row">
                <div class="detail-label">手机号码</div>
                <div class="detail-value" v-if="!editMode">{{ userDetail.phone || '未设置' }}</div>
                <InputText v-else v-model="editedUser.phone" class="detail-input" placeholder="未设置" />
              </div>
              <div class="detail-row">
                <div class="detail-label">地区</div>
                <div class="detail-value" v-if="!editMode">{{ userDetail.region || '未设置' }}</div>
                <InputText v-else v-model="editedUser.region" class="detail-input" placeholder="未设置" />
              </div>
              <div class="detail-row">
                <div class="detail-label">个人简介</div>
                <div class="detail-value" v-if="!editMode">{{ userDetail.bio || '未设置' }}</div>
                <Textarea v-else v-model="editedUser.bio" rows="3" class="detail-input" placeholder="未设置" />
              </div>
            </div>

            <div class="action-buttons" v-if="editMode">
              <Button label="取消" icon="pi pi-times" class="p-button-text" @click="cancelEdit" />
              <Button label="保存" icon="pi pi-check" @click="saveChanges" :loading="submitting" />
            </div>
          </TabPanel>

          <TabPanel header="登录历史">
            <DataTable :value="loginHistory" :paginator="true" :rows="5" stripedRows>
              <Column field="id" header="ID" style="width: 5%"></Column>
              <Column field="date" header="登录时间" style="width: 20%"></Column>
              <Column field="ip" header="IP地址" style="width: 15%"></Column>
              <Column field="device" header="设备" style="width: 15%">
                <template #body="slotProps">
                  <span>
                    <i :class="getDeviceIcon(slotProps.data.device)" class="mr-2"></i>
                    {{ slotProps.data.device }}
                  </span>
                </template>
              </Column>
              <Column field="browser" header="浏览器" style="width: 15%"></Column>
              <Column field="location" header="地点" style="width: 15%"></Column>
              <Column field="status" header="状态" style="width: 15%">
                <template #body="slotProps">
                  <Tag :value="slotProps.data.status" :severity="getLoginStatusSeverity(slotProps.data.status)" />
                </template>
              </Column>
            </DataTable>
          </TabPanel>

          <TabPanel header="活动日志">
            <DataTable :value="activityLog" :paginator="true" :rows="5" stripedRows>
              <Column field="id" header="ID" style="width: 5%"></Column>
              <Column field="date" header="时间" style="width: 20%"></Column>
              <Column field="action" header="操作" style="width: 15%"></Column>
              <Column field="module" header="模块" style="width: 15%"></Column>
              <Column field="details" header="详情" style="width: 30%"></Column>
              <Column field="ip" header="IP地址" style="width: 15%"></Column>
            </DataTable>
          </TabPanel>

          <TabPanel header="账户安全">
            <div class="security-actions">
              <div class="security-action-item">
                <div class="action-info">
                  <h3>重置密码</h3>
                  <p>生成新的随机密码并发送给用户</p>
                </div>
                <Button label="重置密码" icon="pi pi-key" @click="confirmResetPassword" />
              </div>

              <div class="security-action-item">
                <div class="action-info">
                  <h3>两步验证</h3>
                  <p>{{ userDetail.twoFactorEnabled ? '已启用' : '未启用' }} 两步验证</p>
                </div>
                <Button v-if="userDetail.twoFactorEnabled" label="禁用" icon="pi pi-lock-open" class="p-button-danger" @click="toggleTwoFactor" />
                <Button v-else label="启用" icon="pi pi-lock" @click="toggleTwoFactor" />
              </div>

              <div class="security-action-item">
                <div class="action-info">
                  <h3>账户状态</h3>
                  <p>{{ userDetail.status === '活跃' ? '账户当前处于活跃状态' : '账户当前处于非活跃状态' }}</p>
                </div>
                <Button v-if="userDetail.status === '活跃'" label="禁用账户" icon="pi pi-ban" class="p-button-danger" @click="toggleAccountStatus" />
                <Button v-else label="激活账户" icon="pi pi-check-circle" @click="toggleAccountStatus" />
              </div>
            </div>
          </TabPanel>
        </TabView>
      </div>
    </div>

    <div class="detail-loading" v-else>
      <ProgressSpinner />
      <p>加载用户数据中...</p>
    </div>

    <Dialog v-model:visible="resetPasswordDialog" header="确认重置密码" :style="{ width: '450px' }" :modal="true">
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span>确定要重置用户 <b>{{ userDetail.username }}</b> 的密码吗?</span>
      </div>
      <template #footer>
        <Button label="取消" icon="pi pi-times" class="p-button-text" @click="resetPasswordDialog = false" />
        <Button label="重置" icon="pi pi-key" @click="resetPassword" :loading="submitting" />
      </template>
    </Dialog>

    <Dialog v-model:visible="newPasswordDialog" header="密码已重置" :style="{ width: '450px' }" :modal="true">
      <div class="password-content">
        <i class="pi pi-check-circle mr-3 text-success" style="font-size: 2rem; color: var(--green-500)" />
        <div>
          <p>用户 <b>{{ userDetail.username }}</b> 的密码已重置。</p>
          <p>新密码: <strong>{{ newPassword }}</strong></p>
          <small class="text-muted">请记下此密码或告知用户，此密码将不会再次显示。</small>
        </div>
      </div>
      <template #footer>
        <Button label="复制密码" icon="pi pi-copy" @click="copyPassword" />
        <Button label="关闭" icon="pi pi-times" class="p-button-text" @click="newPasswordDialog = false" />
      </template>
    </Dialog>

    <Dialog v-model:visible="deleteDialog" header="确认删除" :style="{ width: '450px' }" :modal="true">
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
        <span>确定要删除用户 <b>{{ userDetail.username }}</b> 吗? 此操作不可撤销。</span>
      </div>
      <template #footer>
        <Button label="取消" icon="pi pi-times" class="p-button-text" @click="deleteDialog = false" />
        <Button label="删除" icon="pi pi-trash" class="p-button-danger" @click="deleteUser" :loading="submitting" />
      </template>
    </Dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { useAdminUsers } from './composables/useAdminUsers'

export default {
  name: 'UserDetailView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const toast = useToast()
    const {
      userDetail,
      loginHistory,
      activityLog,
      loading,
      submitting,
      getUserDetail,
      updateUser,
      deleteUser: apiDeleteUser,
      confirmResetUserPassword,
      updateUserStatus
    } = useAdminUsers()

    // 文件上传
    const fileInput = ref(null)

    // 编辑模式
    const editMode = ref(false)
    const editedUser = ref({})

    // 对话框
    const resetPasswordDialog = ref(false)
    const newPasswordDialog = ref(false)
    const deleteDialog = ref(false)
    const newPassword = ref('')

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

    // 计算属性
    const userId = computed(() => route.params.id)

    // 获取用户详情
    const fetchUserDetail = async () => {
      await getUserDetail(userId.value)
      if (userDetail.value) {
        editedUser.value = { ...userDetail.value }

        // 转换为下拉选项对象
        editedUser.value.role = roleOptions.find(r => r.value === userDetail.value.role || r.name === userDetail.value.role)
        editedUser.value.status = statusOptions.find(s => s.value === userDetail.value.status || s.name === userDetail.value.status)
      }
    }

    // 返回上一页
    const goBack = () => {
      router.push('/admin/users')
    }

    // 触发文件上传
    const triggerFileInput = () => {
      fileInput.value.click()
    }

    // 上传头像
    const uploadAvatar = (event) => {
      const file = event.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          editedUser.value.avatar = e.target.result
        }
        reader.readAsDataURL(file)
      }
    }

    // 取消编辑
    const cancelEdit = () => {
      editMode.value = false
      editedUser.value = { ...userDetail.value }
      editedUser.value.role = roleOptions.find(r => r.value === userDetail.value.role || r.name === userDetail.value.role)
      editedUser.value.status = statusOptions.find(s => s.value === userDetail.value.status || s.name === userDetail.value.status)
    }

    // 保存更改
    const saveChanges = async () => {
      const userData = {
        username: editedUser.value.username,
        email: editedUser.value.email,
        phone: editedUser.value.phone,
        region: editedUser.value.region,
        bio: editedUser.value.bio,
        role: editedUser.value.role?.value,
        status: editedUser.value.status?.value,
        avatar: editedUser.value.avatar
      }

      const result = await updateUser(userId.value, userData)
      if (result.success) {
        editMode.value = false
        toast.add({
          severity: 'success',
          summary: '更新成功',
          detail: '用户信息已更新',
          life: 3000
        })
      }
    }

    // 确认重置密码
    const confirmResetPassword = () => {
      resetPasswordDialog.value = true
    }

    // 重置密码
    const resetPassword = async () => {
      resetPasswordDialog.value = false

      confirmResetUserPassword(userDetail.value, (password) => {
        newPassword.value = password
        newPasswordDialog.value = true
      })
    }

    // 复制密码
    const copyPassword = () => {
      navigator.clipboard.writeText(newPassword.value)
      toast.add({
        severity: 'info',
        summary: '已复制',
        detail: '密码已复制到剪贴板',
        life: 3000
      })
    }

    // 切换两步验证
    const toggleTwoFactor = async () => {
      const newStatus = !userDetail.value.twoFactorEnabled
      const result = await updateUser(userId.value, {
        twoFactorEnabled: newStatus
      })

      if (result.success) {
        toast.add({
          severity: 'success',
          summary: '更新成功',
          detail: `两步验证已${newStatus ? '启用' : '禁用'}`,
          life: 3000
        })
      }
    }

    // 切换账户状态
    const toggleAccountStatus = async () => {
      const newStatus = userDetail.value.status === '活跃' ? 'disabled' : 'active'
      const result = await updateUserStatus(userId.value, newStatus)

      if (result.success) {
        toast.add({
          severity: 'success',
          summary: '更新成功',
          detail: `账户已${newStatus === 'active' ? '激活' : '禁用'}`,
          life: 3000
        })
      }
    }

    // 确认删除
    const confirmDelete = () => {
      deleteDialog.value = true
    }

    // 删除用户
    const deleteUser = async () => {
      const result = await apiDeleteUser(userId.value)
      if (result.success) {
        deleteDialog.value = false
        toast.add({
          severity: 'success',
          summary: '删除成功',
          detail: '用户已成功删除',
          life: 3000
        })
        router.push('/admin/users')
      }
    }

    // 获取角色样式
    const getRoleSeverity = (role) => {
      switch (role) {
        case '管理员':
        case 'admin':
          return 'danger'
        case '高级用户':
        case 'premium':
          return 'warning'
        case '普通用户':
        case 'user':
          return 'info'
        default:
          return 'info'
      }
    }

    // 获取状态样式
    const getStatusSeverity = (status) => {
      switch (status) {
        case '活跃':
        case 'active':
          return 'success'
        case '待验证':
        case 'pending':
          return 'warning'
        case '禁用':
        case 'disabled':
          return 'danger'
        default:
          return 'info'
      }
    }

    // 获取登录状态样式
    const getLoginStatusSeverity = (status) => {
      switch (status) {
        case '成功':
          return 'success'
        case '失败':
          return 'danger'
        default:
          return 'info'
      }
    }

    // 获取设备图标
    const getDeviceIcon = (device) => {
      switch (device.toLowerCase()) {
        case 'desktop':
        case '桌面':
          return 'pi pi-desktop'
        case 'mobile':
        case '手机':
          return 'pi pi-mobile'
        case 'tablet':
        case '平板':
          return 'pi pi-tablet'
        default:
          return 'pi pi-desktop'
      }
    }

    // 初始化
    onMounted(() => {
      fetchUserDetail()
    })

    return {
      userDetail,
      loginHistory,
      activityLog,
      loading,
      submitting,
      fileInput,
      editMode,
      editedUser,
      resetPasswordDialog,
      newPasswordDialog,
      deleteDialog,
      newPassword,
      statusOptions,
      roleOptions,
      goBack,
      triggerFileInput,
      uploadAvatar,
      cancelEdit,
      saveChanges,
      confirmResetPassword,
      resetPassword,
      copyPassword,
      toggleTwoFactor,
      toggleAccountStatus,
      confirmDelete,
      deleteUser,
      getRoleSeverity,
      getStatusSeverity,
      getLoginStatusSeverity,
      getDeviceIcon
    }
  }
}
</script>

<style lang="scss" scoped>
.user-detail-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .header-left {
    display: flex;
    align-items: center;
    gap: 12px;

    h2 {
      margin: 0;
      font-size: 1.5rem;
      font-weight: 600;
    }
  }
}

.detail-content {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  overflow: hidden;

  .user-profile {
    .profile-header {
      display: flex;
      align-items: center;
      padding: 24px;
      border-bottom: 1px solid #f0f0f0;

      .profile-avatar {
        position: relative;
        margin-right: 24px;

        .avatar-upload {
          position: absolute;
          bottom: 0;
          right: 0;
        }
      }

      .profile-info {
        flex: 1;

        .profile-name {
          font-size: 1.5rem;
          font-weight: 600;
          margin-bottom: 8px;
        }

        .profile-name-input {
          font-size: 1.2rem;
          font-weight: 600;
          margin-bottom: 8px;
          width: 100%;
        }

        .profile-meta {
          display: flex;
          flex-wrap: wrap;
          gap: 16px;

          .meta-item {
            display: flex;
            align-items: center;
            gap: 8px;

            i {
              color: #666;
            }

            .meta-input {
              width: 200px;
            }
          }
        }
      }
    }

    .profile-details {
      padding: 24px;

      .detail-row {
        display: flex;
        margin-bottom: 16px;

        .detail-label {
          width: 120px;
          font-weight: 500;
          color: #666;
        }

        .detail-value {
          flex: 1;
        }

        .detail-input {
          width: 100%;
        }
      }
    }

    .action-buttons {
      display: flex;
      justify-content: flex-end;
      gap: 12px;
      padding: 0 24px 24px;
    }

    .security-actions {
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 24px;

      .security-action-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 24px;
        border-bottom: 1px solid #f0f0f0;

        &:last-child {
          border-bottom: none;
          padding-bottom: 0;
        }

        .action-info {
          h3 {
            margin: 0 0 8px;
            font-size: 1.1rem;
            font-weight: 500;
          }

          p {
            margin: 0;
            color: #666;
          }
        }
      }
    }
  }
}

.detail-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);

  p {
    margin-top: 16px;
    color: #666;
  }
}

.confirmation-content,
.password-content {
  display: flex;
  align-items: flex-start;
  padding: 16px 0;
}

.text-success {
  color: var(--green-500);
}

.text-muted {
  color: #666;
}
</style>
