<template>
  <div class="settings-view">
    <div class="settings-header">
      <h1>账号设置</h1>
      <p>管理您的个人信息和偏好设置</p>
    </div>

    <div class="settings-content">
      <TabView>
        <!-- 个人资料设置 -->
        <TabPanel header="个人资料">
          <div class="settings-form">
            <h2>基本信息</h2>
            <div class="form-group">
              <label for="username">用户名</label>
              <InputText id="username" v-model="profile.username" class="w-full" />
            </div>
            <div class="form-group">
              <label for="email">电子邮箱</label>
              <InputText id="email" v-model="profile.email" type="email" class="w-full" disabled />
              <small>更改邮箱需要验证，请联系客服</small>
            </div>
            <div class="form-group">
              <label for="bio">个人简介</label>
              <Textarea id="bio" v-model="profile.bio" rows="3" class="w-full" />
            </div>
            <div class="form-group">
              <label for="phone">手机号码</label>
              <InputText id="phone" v-model="profile.phone" class="w-full" />
            </div>
            <div class="form-group">
              <label for="location">所在地区</label>
              <Dropdown id="location" v-model="profile.location" :options="locationOptions" optionLabel="name" class="w-full" />
            </div>

            <h2>社交账号</h2>
            <div class="form-group">
              <label for="weixin">微信</label>
              <InputText id="weixin" v-model="profile.socialLinks.weixin" class="w-full" />
            </div>
            <div class="form-group">
              <label for="weibo">微博</label>
              <InputText id="weibo" v-model="profile.socialLinks.weibo" class="w-full" />
            </div>
            <div class="form-group">
              <label for="qq">QQ</label>
              <InputText id="qq" v-model="profile.socialLinks.qq" class="w-full" />
            </div>

            <div class="form-actions">
              <Button label="保存更改" icon="pi pi-save" @click="saveProfile" :loading="saving" />
            </div>
          </div>
        </TabPanel>

        <!-- 安全设置 -->
        <TabPanel header="安全设置">
          <div class="settings-form">
            <h2>修改密码</h2>
            <div class="form-group">
              <label for="currentPassword">当前密码</label>
              <Password id="currentPassword" v-model="security.currentPassword" toggleMask class="w-full" />
            </div>
            <div class="form-group">
              <label for="newPassword">新密码</label>
              <Password id="newPassword" v-model="security.newPassword" toggleMask class="w-full" />
            </div>
            <div class="form-group">
              <label for="confirmPassword">确认新密码</label>
              <Password id="confirmPassword" v-model="security.confirmPassword" toggleMask class="w-full" />
            </div>

            <div class="form-actions">
              <Button label="更新密码" icon="pi pi-lock" @click="updatePassword" :loading="updatingPassword" />
            </div>

            <h2>两步验证</h2>
            <div class="form-group">
              <div class="two-factor-status">
                <div class="status-info">
                  <h3>两步验证状态</h3>
                  <p>{{ security.twoFactorEnabled ? '已启用' : '未启用' }}</p>
                </div>
                <div class="status-action">
                  <Button v-if="!security.twoFactorEnabled" label="启用" icon="pi pi-shield" @click="enableTwoFactor" />
                  <Button v-else label="禁用" icon="pi pi-shield" class="p-button-danger" @click="disableTwoFactor" />
                </div>
              </div>
            </div>

            <h2>登录设备</h2>
            <DataTable :value="security.loginDevices" :paginator="true" :rows="5" stripedRows>
              <Column field="device" header="设备" />
              <Column field="location" header="位置" />
              <Column field="lastLogin" header="最后登录时间" />
              <Column field="status" header="状态">
                <template #body="slotProps">
                  <Tag :value="slotProps.data.status" :severity="getDeviceSeverity(slotProps.data.status)" />
                </template>
              </Column>
              <Column header="操作">
                <template #body="slotProps">
                  <Button icon="pi pi-times" class="p-button-rounded p-button-danger p-button-text"
                    @click="revokeDevice(slotProps.data.id)" />
                </template>
              </Column>
            </DataTable>
          </div>
        </TabPanel>

        <!-- 隐私设置 -->
        <TabPanel header="隐私设置">
          <div class="settings-form">
            <h2>个人资料隐私</h2>
            <div class="form-group">
              <div class="privacy-option">
                <div class="option-label">
                  <h3>个人资料可见性</h3>
                  <p>控制谁可以查看您的个人资料</p>
                </div>
                <div class="option-control">
                  <Dropdown v-model="privacy.profileVisibility" :options="visibilityOptions" optionLabel="name" class="w-full" />
                </div>
              </div>
            </div>

            <div class="form-group">
              <div class="privacy-option">
                <div class="option-label">
                  <h3>在线状态</h3>
                  <p>控制谁可以看到您的在线状态</p>
                </div>
                <div class="option-control">
                  <Dropdown v-model="privacy.onlineStatus" :options="visibilityOptions" optionLabel="name" class="w-full" />
                </div>
              </div>
            </div>

            <div class="form-group">
              <div class="privacy-option">
                <div class="option-label">
                  <h3>好友请求</h3>
                  <p>控制谁可以向您发送好友请求</p>
                </div>
                <div class="option-control">
                  <Dropdown v-model="privacy.friendRequests" :options="visibilityOptions" optionLabel="name" class="w-full" />
                </div>
              </div>
            </div>

            <h2>空间隐私</h2>
            <div class="form-group">
              <div class="privacy-option">
                <div class="option-label">
                  <h3>空间可见性</h3>
                  <p>控制谁可以访问您的虚拟空间</p>
                </div>
                <div class="option-control">
                  <Dropdown v-model="privacy.spaceVisibility" :options="visibilityOptions" optionLabel="name" class="w-full" />
                </div>
              </div>
            </div>

            <div class="form-actions">
              <Button label="保存隐私设置" icon="pi pi-save" @click="savePrivacy" :loading="savingPrivacy" />
            </div>
          </div>
        </TabPanel>

        <!-- 通知设置 -->
        <TabPanel header="通知设置">
          <div class="settings-form">
            <h2>通知偏好</h2>

            <div class="form-group">
              <div class="notification-option">
                <div class="option-label">
                  <h3>好友请求</h3>
                  <p>当有人向您发送好友请求时通知您</p>
                </div>
                <div class="option-control">
                  <InputSwitch v-model="notifications.friendRequests" />
                </div>
              </div>
            </div>

            <div class="form-group">
              <div class="notification-option">
                <div class="option-label">
                  <h3>消息通知</h3>
                  <p>当您收到新消息时通知您</p>
                </div>
                <div class="option-control">
                  <InputSwitch v-model="notifications.messages" />
                </div>
              </div>
            </div>

            <div class="form-group">
              <div class="notification-option">
                <div class="option-label">
                  <h3>空间访问</h3>
                  <p>当有人访问您的虚拟空间时通知您</p>
                </div>
                <div class="option-control">
                  <InputSwitch v-model="notifications.spaceVisits" />
                </div>
              </div>
            </div>

            <div class="form-group">
              <div class="notification-option">
                <div class="option-label">
                  <h3>系统公告</h3>
                  <p>接收系统更新和公告</p>
                </div>
                <div class="option-control">
                  <InputSwitch v-model="notifications.systemAnnouncements" />
                </div>
              </div>
            </div>

            <h2>通知方式</h2>
            <div class="form-group">
              <div class="notification-option">
                <div class="option-label">
                  <h3>站内通知</h3>
                </div>
                <div class="option-control">
                  <InputSwitch v-model="notifications.methods.inApp" />
                </div>
              </div>
            </div>

            <div class="form-group">
              <div class="notification-option">
                <div class="option-label">
                  <h3>邮件通知</h3>
                </div>
                <div class="option-control">
                  <InputSwitch v-model="notifications.methods.email" />
                </div>
              </div>
            </div>

            <div class="form-group">
              <div class="notification-option">
                <div class="option-label">
                  <h3>桌面通知</h3>
                </div>
                <div class="option-control">
                  <InputSwitch v-model="notifications.methods.desktop" />
                </div>
              </div>
            </div>

            <div class="form-actions">
              <Button label="保存通知设置" icon="pi pi-save" @click="saveNotifications" :loading="savingNotifications" />
            </div>
          </div>
        </TabPanel>

        <!-- 账号管理 -->
        <TabPanel header="账号管理">
          <div class="settings-form">
            <h2>账号状态</h2>
            <div class="account-status">
              <div class="status-info">
                <h3>当前状态</h3>
                <Tag :value="account.status" :severity="getAccountSeverity(account.status)" />
              </div>
              <div class="status-details">
                <p>账号类型: {{ account.type }}</p>
                <p>创建时间: {{ formatDate(account.createdAt) }}</p>
                <p>会员到期: {{ account.membershipExpiry ? formatDate(account.membershipExpiry) : '无会员' }}</p>
              </div>
            </div>

            <h2>危险操作</h2>
            <div class="danger-zone">
              <div class="danger-action">
                <div class="action-info">
                  <h3>注销账号</h3>
                  <p>永久删除您的账号和所有相关数据，此操作不可撤销</p>
                </div>
                <div class="action-button">
                  <Button label="注销账号" icon="pi pi-trash" class="p-button-danger" @click="confirmDeleteAccount" />
                </div>
              </div>
            </div>
          </div>
        </TabPanel>
      </TabView>
    </div>

    <!-- 确认删除账号对话框 -->
    <Dialog v-model:visible="showDeleteConfirm" header="确认注销账号" :style="{ width: '450px' }" :modal="true">
      <div class="confirmation-content">
        <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem; color: var(--red-500);" />
        <span>您确定要永久注销您的账号吗？此操作将删除所有数据且<b>不可恢复</b>。</span>
      </div>
      <div class="mt-4">
        <div class="form-group">
          <label for="confirmPassword">请输入您的密码以确认</label>
          <Password id="confirmDeletePassword" v-model="deleteAccountPassword" toggleMask class="w-full" />
        </div>
      </div>
      <template #footer>
        <Button label="取消" icon="pi pi-times" class="p-button-text" @click="showDeleteConfirm = false" />
        <Button label="确认注销" icon="pi pi-trash" class="p-button-danger" @click="deleteAccount" :loading="deletingAccount" />
      </template>
    </Dialog>
  </div>
</template>

<script>
import SettingsViews from '@/server/view/user/SettingsViews'
</script>

<style lang="scss">
@use '@styles/view/user/settings.scss';
</style>
