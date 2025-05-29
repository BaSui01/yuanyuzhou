<template>
  <div class="profile-view">
    <div class="profile-header">
      <div class="header-content">
        <div class="user-avatar">
          <Avatar :image="user.avatar || '/img/default.png'" size="xlarge" shape="circle" />
          <Button icon="pi pi-camera" class="avatar-edit-button" @click="openAvatarUpload" />
        </div>
        <div class="user-info">
          <h1>{{ user.username }}</h1>
          <p class="user-bio">{{ user.bio || '这个用户还没有填写个人简介' }}</p>
          <div class="user-stats">
            <div class="stat-item">
              <span class="stat-value">{{ user.friendsCount || 0 }}</span>
              <span class="stat-label">好友</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ user.spacesCount || 0 }}</span>
              <span class="stat-label">空间</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ user.petsCount || 0 }}</span>
              <span class="stat-label">AI伙伴</span>
            </div>
          </div>
        </div>
        <div class="profile-actions">
          <Button label="编辑资料" icon="pi pi-user-edit" @click="navigateToSettings" />
        </div>
      </div>
    </div>

    <div class="profile-content">
      <TabView>
        <!-- 个人信息标签页 -->
        <TabPanel header="个人信息">
          <div class="info-section">
            <div class="info-card">
              <h2>基本信息</h2>
              <div class="info-item">
                <span class="info-label">用户名</span>
                <span class="info-value">{{ user.username }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">邮箱</span>
                <span class="info-value">{{ user.email }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">注册时间</span>
                <span class="info-value">{{ formatDate(user.createdAt) }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">最后登录</span>
                <span class="info-value">{{ formatDate(user.lastLogin) }}</span>
              </div>
            </div>

            <div class="info-card">
              <h2>联系方式</h2>
              <div class="info-item">
                <span class="info-label">手机</span>
                <span class="info-value">{{ user.phone || '未设置' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">地区</span>
                <span class="info-value">{{ user.location || '未设置' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">社交账号</span>
                <div class="social-links">
                  <Button v-if="user.socialLinks?.weixin" icon="pi pi-wechat" class="p-button-rounded p-button-text" />
                  <Button v-if="user.socialLinks?.weibo" icon="pi pi-weibo" class="p-button-rounded p-button-text" />
                  <Button v-if="user.socialLinks?.qq" icon="pi pi-qq" class="p-button-rounded p-button-text" />
                  <span v-if="!user.socialLinks">未设置</span>
                </div>
              </div>
            </div>
          </div>
        </TabPanel>

        <!-- 我的AI伙伴标签页 -->
        <TabPanel header="我的AI伙伴">
          <div class="pets-section" v-if="userPets.length > 0">
            <div class="pets-grid">
              <div v-for="(pet, index) in userPets" :key="index" class="pet-card">
                <div class="pet-avatar">
                  <img :src="pet.avatar" :alt="pet.name" />
                </div>
                <div class="pet-info">
                  <h3>{{ pet.name }}</h3>
                  <p>{{ pet.description }}</p>
                  <div class="pet-stats">
                    <div class="pet-stat">
                      <i class="pi pi-heart"></i>
                      <span>亲密度: {{ pet.intimacy }}</span>
                    </div>
                    <div class="pet-stat">
                      <i class="pi pi-calendar"></i>
                      <span>创建于: {{ formatDate(pet.createdAt) }}</span>
                    </div>
                  </div>
                </div>
                <div class="pet-actions">
                  <Button label="互动" icon="pi pi-comments" class="p-button-sm" @click="interactWithPet(pet.id)" />
                  <Button label="设置" icon="pi pi-cog" class="p-button-sm p-button-outlined" @click="editPet(pet.id)" />
                </div>
              </div>
            </div>
          </div>
          <div class="empty-state" v-else>
            <i class="pi pi-robot empty-icon"></i>
            <h3>您还没有创建AI伙伴</h3>
            <p>创建一个AI伙伴，开始您的元宇宙社交之旅</p>
            <Button label="创建AI伙伴" icon="pi pi-plus" @click="navigateToCreatePet" />
          </div>
        </TabPanel>

        <!-- 我的空间标签页 -->
        <TabPanel header="我的空间">
          <div class="spaces-section" v-if="userSpaces.length > 0">
            <div class="spaces-grid">
              <div v-for="(space, index) in userSpaces" :key="index" class="space-card">
                <div class="space-preview">
                  <img :src="space.thumbnail" :alt="space.name" />
                </div>
                <div class="space-info">
                  <h3>{{ space.name }}</h3>
                  <p>{{ space.description }}</p>
                  <div class="space-stats">
                    <div class="space-stat">
                      <i class="pi pi-users"></i>
                      <span>访客: {{ space.visitorCount }}</span>
                    </div>
                    <div class="space-stat">
                      <i class="pi pi-calendar"></i>
                      <span>创建于: {{ formatDate(space.createdAt) }}</span>
                    </div>
                  </div>
                </div>
                <div class="space-actions">
                  <Button label="访问" icon="pi pi-sign-in" class="p-button-sm" @click="visitSpace(space.id)" />
                  <Button label="编辑" icon="pi pi-pencil" class="p-button-sm p-button-outlined" @click="editSpace(space.id)" />
                </div>
              </div>
            </div>
          </div>
          <div class="empty-state" v-else>
            <i class="pi pi-globe empty-icon"></i>
            <h3>您还没有创建虚拟空间</h3>
            <p>创建一个虚拟空间，邀请朋友来访问</p>
            <Button label="创建空间" icon="pi pi-plus" @click="navigateToCreateSpace" />
          </div>
        </TabPanel>

        <!-- 好友列表标签页 -->
        <TabPanel header="好友列表">
          <div class="friends-section" v-if="userFriends.length > 0">
            <div class="friends-grid">
              <div v-for="(friend, index) in userFriends" :key="index" class="friend-card">
                <div class="friend-avatar">
                  <Avatar :image="friend.avatar" shape="circle" />
                </div>
                <div class="friend-info">
                  <h3>{{ friend.username }}</h3>
                  <p>{{ friend.status }}</p>
                </div>
                <div class="friend-actions">
                  <Button icon="pi pi-comments" class="p-button-rounded p-button-text" @click="chatWithFriend(friend.id)" />
                  <Button icon="pi pi-user" class="p-button-rounded p-button-text" @click="viewFriendProfile(friend.id)" />
                </div>
              </div>
            </div>
          </div>
          <div class="empty-state" v-else>
            <i class="pi pi-users empty-icon"></i>
            <h3>您的好友列表为空</h3>
            <p>添加好友，一起探索元宇宙</p>
            <Button label="查找好友" icon="pi pi-search" @click="navigateToFindFriends" />
          </div>
        </TabPanel>
      </TabView>
    </div>

    <!-- 头像上传对话框 -->
    <Dialog v-model:visible="showAvatarUpload" header="更新头像" :style="{ width: '450px' }">
      <div class="avatar-upload-content">
        <div class="current-avatar">
          <Avatar :image="user.avatar || '/img/default.png'" size="xlarge" shape="circle" />
        </div>
        <div class="upload-controls">
          <FileUpload mode="basic" name="avatar" url="/api/user/avatar" accept="image/*" :maxFileSize="1000000" @upload="onAvatarUpload" />
        </div>
      </div>
      <template #footer>
        <Button label="取消" icon="pi pi-times" class="p-button-text" @click="showAvatarUpload = false" />
        <Button label="保存" icon="pi pi-check" @click="saveAvatar" :loading="uploading" />
      </template>
    </Dialog>
  </div>
</template>

<script>
import ProfileViews from '@/server/view/user/ProfileViews'
</script>

<style lang="scss">
@use '@styles/view/user/profile.scss';
</style>
