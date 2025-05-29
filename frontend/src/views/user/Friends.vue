<template>
  <div class="friends-view">
    <div class="friends-header">
      <h1>好友管理</h1>
      <div class="friends-actions">
        <span class="p-input-icon-left search-box">
          <i class="pi pi-search" />
          <InputText v-model="searchQuery" placeholder="搜索好友" />
        </span>
        <Button label="查找新朋友" icon="pi pi-user-plus" @click="openFindFriends" />
      </div>
    </div>

    <div class="friends-content">
      <TabView>
        <!-- 好友列表标签页 -->
        <TabPanel header="我的好友">
          <div class="friends-list" v-if="filteredFriends.length > 0">
            <DataTable :value="filteredFriends" :paginator="true" :rows="10"
              :rowsPerPageOptions="[5, 10, 20]" stripedRows>
              <Column>
                <template #body="slotProps">
                  <div class="friend-item">
                    <div class="friend-avatar">
                      <Avatar :image="slotProps.data.avatar" shape="circle" size="large" />
                      <span class="status-badge" :class="slotProps.data.online ? 'online' : 'offline'"></span>
                    </div>
                    <div class="friend-info">
                      <h3>{{ slotProps.data.username }}</h3>
                      <p>{{ slotProps.data.status }}</p>
                    </div>
                    <div class="friend-actions">
                      <Button icon="pi pi-comments" class="p-button-rounded p-button-text"
                        @click="chatWithFriend(slotProps.data.id)" tooltip="发送消息" />
                      <Button icon="pi pi-user" class="p-button-rounded p-button-text"
                        @click="viewFriendProfile(slotProps.data.id)" tooltip="查看资料" />
                      <Button icon="pi pi-ellipsis-v" class="p-button-rounded p-button-text"
                        @click="openFriendMenu($event, slotProps.data)" />
                    </div>
                  </div>
                </template>
              </Column>
            </DataTable>
          </div>
          <div class="empty-state" v-else>
            <i class="pi pi-users empty-icon"></i>
            <h3>您的好友列表为空</h3>
            <p>添加好友，一起探索元宇宙</p>
            <Button label="查找好友" icon="pi pi-search" @click="openFindFriends" />
          </div>
        </TabPanel>

        <!-- 好友请求标签页 -->
        <TabPanel header="好友请求">
          <div class="friends-requests" v-if="friendRequests.length > 0">
            <h3>收到的请求</h3>
            <div class="request-list">
              <div v-for="(request, index) in friendRequests" :key="index" class="request-item">
                <div class="request-avatar">
                  <Avatar :image="request.avatar" shape="circle" />
                </div>
                <div class="request-info">
                  <h4>{{ request.username }}</h4>
                  <p>{{ request.message || '希望添加您为好友' }}</p>
                  <span class="request-time">{{ formatTime(request.requestTime) }}</span>
                </div>
                <div class="request-actions">
                  <Button label="接受" icon="pi pi-check" class="p-button-success p-button-sm"
                    @click="acceptFriendRequest(request.id)" />
                  <Button label="拒绝" icon="pi pi-times" class="p-button-danger p-button-sm"
                    @click="rejectFriendRequest(request.id)" />
                </div>
              </div>
            </div>
          </div>
          <div class="friends-requests" v-if="sentRequests.length > 0">
            <h3>发送的请求</h3>
            <div class="request-list">
              <div v-for="(request, index) in sentRequests" :key="index" class="request-item">
                <div class="request-avatar">
                  <Avatar :image="request.avatar" shape="circle" />
                </div>
                <div class="request-info">
                  <h4>{{ request.username }}</h4>
                  <p>{{ request.message || '您发送了好友请求' }}</p>
                  <span class="request-time">{{ formatTime(request.requestTime) }}</span>
                </div>
                <div class="request-actions">
                  <Button label="取消" icon="pi pi-times" class="p-button-outlined p-button-sm"
                    @click="cancelFriendRequest(request.id)" />
                </div>
              </div>
            </div>
          </div>
          <div class="empty-state" v-if="friendRequests.length === 0 && sentRequests.length === 0">
            <i class="pi pi-inbox empty-icon"></i>
            <h3>没有待处理的好友请求</h3>
            <p>当您收到或发送好友请求时，会显示在这里</p>
          </div>
        </TabPanel>

        <!-- 黑名单标签页 -->
        <TabPanel header="黑名单">
          <div class="blocked-users" v-if="blockedUsers.length > 0">
            <DataTable :value="blockedUsers" :paginator="true" :rows="10" stripedRows>
              <Column>
                <template #body="slotProps">
                  <div class="blocked-item">
                    <div class="blocked-avatar">
                      <Avatar :image="slotProps.data.avatar" shape="circle" />
                    </div>
                    <div class="blocked-info">
                      <h4>{{ slotProps.data.username }}</h4>
                      <p>已屏蔽于 {{ formatDate(slotProps.data.blockedAt) }}</p>
                    </div>
                    <div class="blocked-actions">
                      <Button label="解除屏蔽" icon="pi pi-unlock" class="p-button-outlined p-button-sm"
                        @click="unblockUser(slotProps.data.id)" />
                    </div>
                  </div>
                </template>
              </Column>
            </DataTable>
          </div>
          <div class="empty-state" v-else>
            <i class="pi pi-shield empty-icon"></i>
            <h3>黑名单为空</h3>
            <p>您没有屏蔽任何用户</p>
          </div>
        </TabPanel>
      </TabView>
    </div>

    <!-- 查找好友对话框 -->
    <Dialog v-model:visible="showFindFriends" header="查找好友" :style="{ width: '500px' }">
      <div class="find-friends-content">
        <div class="search-section">
          <span class="p-input-icon-left w-full">
            <i class="pi pi-search" />
            <InputText v-model="findFriendsQuery" placeholder="输入用户名、邮箱或ID搜索" class="w-full" />
          </span>
          <Button label="搜索" icon="pi pi-search" @click="searchUsers" :loading="searching" />
        </div>

        <div class="search-results" v-if="searchResults.length > 0">
          <div v-for="(user, index) in searchResults" :key="index" class="user-result-item">
            <div class="user-result-avatar">
              <Avatar :image="user.avatar" shape="circle" />
            </div>
            <div class="user-result-info">
              <h4>{{ user.username }}</h4>
              <p>{{ user.bio || '这个用户很懒，还没有填写个人简介' }}</p>
            </div>
            <div class="user-result-actions">
              <Button v-if="!user.isFriend && !user.requestSent" label="添加好友" icon="pi pi-user-plus"
                class="p-button-sm" @click="sendFriendRequest(user.id)" />
              <Button v-else-if="user.requestSent" label="已发送请求" icon="pi pi-clock"
                class="p-button-sm p-button-outlined" disabled />
              <Button v-else label="已是好友" icon="pi pi-check"
                class="p-button-sm p-button-success" disabled />
            </div>
          </div>
        </div>
        <div class="empty-search" v-else-if="searched && searchResults.length === 0">
          <i class="pi pi-search empty-icon"></i>
          <p>未找到匹配的用户</p>
        </div>
      </div>
    </Dialog>

    <!-- 好友菜单 -->
    <Menu id="friend-menu" ref="friendMenu" :model="friendMenuItems" :popup="true" />

    <!-- 发送好友请求对话框 -->
    <Dialog v-model:visible="showSendRequest" header="发送好友请求" :style="{ width: '450px' }">
      <div class="send-request-content">
        <div class="selected-user-info" v-if="selectedUser">
          <div class="user-avatar">
            <Avatar :image="selectedUser.avatar" shape="circle" size="large" />
          </div>
          <div class="user-details">
            <h3>{{ selectedUser.username }}</h3>
          </div>
        </div>
        <div class="request-message-form">
          <label for="requestMessage">留言（可选）</label>
          <Textarea id="requestMessage" v-model="friendRequestMessage" rows="3" class="w-full"
            placeholder="向对方介绍一下自己..." />
        </div>
      </div>
      <template #footer>
        <Button label="取消" icon="pi pi-times" class="p-button-text" @click="showSendRequest = false" />
        <Button label="发送请求" icon="pi pi-send" @click="confirmSendFriendRequest" :loading="sendingRequest" />
      </template>
    </Dialog>
  </div>
</template>

<script>
import FriendsViews from '@/server/view/user/FriendsViews'
</script>

<style lang="scss">
@use '@styles/view/user/friends.scss';
</style>
