<template>
  <div class="social-view p-4 md:p-6">
    <div class="max-w-7xl mx-auto">
      <!-- 页面标题 -->
      <div class="page-header mb-8">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h1 class="text-3xl font-bold text-white mb-2">社交广场</h1>
            <p class="text-gray-400">与其他用户互动交流，分享您的元宇宙体验</p>
          </div>
          <div class="flex gap-3">
            <Button label="发布动态" icon="pi pi-plus" class="btn-primary" @click="showPostDialog = true" />
            <Button label="创建群组" icon="pi pi-users" class="btn-secondary" @click="showGroupDialog = true" />
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- 左侧边栏 -->
        <div class="lg:col-span-1">
          <!-- 在线好友 -->
          <div class="glass rounded-xl p-6 mb-6">
            <h3 class="text-lg font-semibold text-white mb-4 flex items-center">
              <i class="pi pi-users mr-2 text-green-400"></i>
              在线好友 ({{ onlineFriends.length }})
            </h3>
            <div class="space-y-3">
              <div v-for="friend in onlineFriends" :key="friend.id"
                class="flex items-center space-x-3 p-2 rounded-lg hover:bg-white/5 cursor-pointer transition-colors"
                @click="startChat(friend)">
                <div class="relative">
                  <Avatar :image="friend.avatar" size="normal" />
                  <div class="absolute -bottom-1 -right-1 w-3 h-3 bg-green-400 rounded-full border-2 border-gray-900">
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-white text-sm font-medium truncate">{{ friend.name }}</p>
                  <p class="text-gray-400 text-xs truncate">{{ friend.status }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 热门群组 -->
          <div class="glass rounded-xl p-6">
            <h3 class="text-lg font-semibold text-white mb-4 flex items-center">
              <i class="pi pi-hashtag mr-2 text-purple-400"></i>
              热门群组
            </h3>
            <div class="space-y-3">
              <div v-for="group in popularGroups" :key="group.id"
                class="flex items-center space-x-3 p-2 rounded-lg hover:bg-white/5 cursor-pointer transition-colors"
                @click="joinGroup(group)">
                <Avatar :image="group.avatar" size="normal" shape="square" />
                <div class="flex-1 min-w-0">
                  <p class="text-white text-sm font-medium truncate">{{ group.name }}</p>
                  <p class="text-gray-400 text-xs">{{ group.memberCount }} 成员</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 主内容区 -->
        <div class="lg:col-span-2">
          <!-- 发布框 -->
          <div class="glass rounded-xl p-6 mb-6">
            <div class="flex items-start space-x-4">
              <Avatar :image="userAvatar" size="normal" />
              <div class="flex-1">
                <Textarea v-model="newPostContent" placeholder="分享您的想法..." rows="3" class="w-full mb-3"
                  @focus="showPostOptions = true" />
                <div v-if="showPostOptions" class="flex justify-between items-center">
                  <div class="flex space-x-2">
                    <Button icon="pi pi-image" class="p-button-text p-button-rounded" title="添加图片" />
                    <Button icon="pi pi-video" class="p-button-text p-button-rounded" title="添加视频" />
                    <Button icon="pi pi-map-marker" class="p-button-text p-button-rounded" title="添加位置" />
                  </div>
                  <div class="flex space-x-2">
                    <Button label="取消" class="p-button-text" @click="cancelPost" />
                    <Button label="发布" icon="pi pi-send" @click="publishPost" :disabled="!newPostContent.trim()" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 动态列表 -->
          <div class="space-y-6">
            <div v-for="post in posts" :key="post.id" class="glass rounded-xl p-6">
              <!-- 用户信息 -->
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center space-x-3">
                  <Avatar :image="post.user.avatar" size="normal" />
                  <div>
                    <h4 class="text-white font-medium">{{ post.user.name }}</h4>
                    <p class="text-gray-400 text-sm">{{ formatTime(post.createdAt) }}</p>
                  </div>
                </div>
                <Button icon="pi pi-ellipsis-h" class="p-button-text p-button-rounded" />
              </div>

              <!-- 内容 -->
              <div class="mb-4">
                <p class="text-gray-200 leading-relaxed">{{ post.content }}</p>
                <div v-if="post.images && post.images.length" class="mt-3 grid grid-cols-2 gap-2">
                  <img v-for="(image, index) in post.images" :key="index" :src="image" :alt="`图片${index + 1}`"
                    class="rounded-lg w-full h-32 object-cover cursor-pointer" @click="viewImage(image)" />
                </div>
              </div>

              <!-- 互动按钮 -->
              <div class="flex items-center justify-between pt-4 border-t border-white/10">
                <div class="flex space-x-6">
                  <button class="flex items-center space-x-2 text-gray-400 hover:text-red-400 transition-colors"
                    @click="toggleLike(post)">
                    <i :class="post.isLiked ? 'pi pi-heart-fill text-red-400' : 'pi pi-heart'"></i>
                    <span>{{ post.likes }}</span>
                  </button>
                  <button class="flex items-center space-x-2 text-gray-400 hover:text-blue-400 transition-colors"
                    @click="showComments(post)">
                    <i class="pi pi-comment"></i>
                    <span>{{ post.comments }}</span>
                  </button>
                  <button class="flex items-center space-x-2 text-gray-400 hover:text-green-400 transition-colors"
                    @click="sharePost(post)">
                    <i class="pi pi-share-alt"></i>
                    <span>分享</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- 加载更多 -->
          <div class="text-center mt-8">
            <Button label="加载更多" icon="pi pi-refresh" class="p-button-outlined" @click="loadMorePosts" />
          </div>
        </div>

        <!-- 右侧边栏 -->
        <div class="lg:col-span-1">
          <!-- 推荐用户 -->
          <div class="glass rounded-xl p-6 mb-6">
            <h3 class="text-lg font-semibold text-white mb-4 flex items-center">
              <i class="pi pi-user-plus mr-2 text-cyan-400"></i>
              推荐关注
            </h3>
            <div class="space-y-4">
              <div v-for="user in recommendedUsers" :key="user.id" class="flex items-center justify-between">
                <div class="flex items-center space-x-3">
                  <Avatar :image="user.avatar" size="normal" />
                  <div>
                    <p class="text-white text-sm font-medium">{{ user.name }}</p>
                    <p class="text-gray-400 text-xs">{{ user.mutualFriends }} 个共同好友</p>
                  </div>
                </div>
                <Button label="关注" size="small" @click="followUser(user)" />
              </div>
            </div>
          </div>

          <!-- 活动推荐 -->
          <div class="glass rounded-xl p-6">
            <h3 class="text-lg font-semibold text-white mb-4 flex items-center">
              <i class="pi pi-calendar mr-2 text-amber-400"></i>
              活动推荐
            </h3>
            <div class="space-y-4">
              <div v-for="event in recommendedEvents" :key="event.id"
                class="p-3 rounded-lg bg-white/5 hover:bg-white/10 cursor-pointer transition-colors">
                <h4 class="text-white font-medium text-sm mb-1">{{ event.title }}</h4>
                <p class="text-gray-400 text-xs mb-2">{{ event.time }}</p>
                <div class="flex justify-between items-center">
                  <span class="text-cyan-400 text-xs">{{ event.participants }} 人参与</span>
                  <Button label="参与" size="small" class="p-button-outlined" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 发布动态对话框 -->
    <Dialog v-model:visible="showPostDialog" header="发布动态" :style="{ width: '600px' }" modal>
      <div class="space-y-4">
        <Textarea v-model="newPostContent" placeholder="分享您的想法..." rows="5" class="w-full" />
        <div class="flex justify-between items-center">
          <div class="flex space-x-2">
            <Button icon="pi pi-image" label="图片" class="p-button-outlined" />
            <Button icon="pi pi-video" label="视频" class="p-button-outlined" />
            <Button icon="pi pi-map-marker" label="位置" class="p-button-outlined" />
          </div>
          <Dropdown v-model="postPrivacy" :options="privacyOptions" optionLabel="label" optionValue="value"
            placeholder="选择可见性" class="w-32" />
        </div>
      </div>
      <template #footer>
        <Button label="取消" icon="pi pi-times" class="p-button-text" @click="showPostDialog = false" />
        <Button label="发布" icon="pi pi-send" @click="publishPost" :disabled="!newPostContent.trim()" />
      </template>
    </Dialog>

    <!-- 创建群组对话框 -->
    <Dialog v-model:visible="showGroupDialog" header="创建群组" :style="{ width: '500px' }" modal>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">群组名称</label>
          <InputText v-model="newGroup.name" placeholder="输入群组名称" class="w-full" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">群组描述</label>
          <Textarea v-model="newGroup.description" placeholder="描述群组的目的和规则" rows="3" class="w-full" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">隐私设置</label>
          <div class="space-y-2">
            <div class="flex items-center">
              <RadioButton v-model="newGroup.privacy" inputId="public" value="public" />
              <label for="public" class="ml-2 text-gray-300">公开群组 - 任何人都可以加入</label>
            </div>
            <div class="flex items-center">
              <RadioButton v-model="newGroup.privacy" inputId="private" value="private" />
              <label for="private" class="ml-2 text-gray-300">私密群组 - 需要邀请才能加入</label>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <Button label="取消" icon="pi pi-times" class="p-button-text" @click="showGroupDialog = false" />
        <Button label="创建" icon="pi pi-check" @click="createGroup" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

// 响应式数据
const newPostContent = ref('')
const showPostOptions = ref(false)
const showPostDialog = ref(false)
const showGroupDialog = ref(false)
const postPrivacy = ref('public')

// 用户信息
const userAvatar = computed(() => authStore.userAvatar)

// 隐私选项
const privacyOptions = ref([
  { label: '公开', value: 'public' },
  { label: '好友', value: 'friends' },
  { label: '仅自己', value: 'private' }
])

// 新群组数据
const newGroup = ref({
  name: '',
  description: '',
  privacy: 'public'
})

// 在线好友数据
const onlineFriends = ref([
  {
    id: 1,
    name: '星辰漫游者',
    avatar: '/avatars/user1.jpg',
    status: '正在元宇宙探索'
  },
  {
    id: 2,
    name: '数字幻影',
    avatar: '/avatars/user2.jpg',
    status: '与AI助手聊天中'
  },
  {
    id: 3,
    name: '虚拟旅者',
    avatar: '/avatars/user3.jpg',
    status: '在线'
  }
])

// 热门群组数据
const popularGroups = ref([
  {
    id: 1,
    name: 'AI技术交流',
    avatar: '/groups/ai-tech.jpg',
    memberCount: 1247
  },
  {
    id: 2,
    name: '元宇宙探索者',
    avatar: '/groups/metaverse.jpg',
    memberCount: 892
  },
  {
    id: 3,
    name: '创意工作室',
    avatar: '/groups/creative.jpg',
    memberCount: 634
  }
])

// 推荐用户数据
const recommendedUsers = ref([
  {
    id: 1,
    name: '科技达人',
    avatar: '/avatars/rec1.jpg',
    mutualFriends: 5
  },
  {
    id: 2,
    name: '设计师小王',
    avatar: '/avatars/rec2.jpg',
    mutualFriends: 3
  },
  {
    id: 3,
    name: '程序员老李',
    avatar: '/avatars/rec3.jpg',
    mutualFriends: 8
  }
])

// 推荐活动数据
const recommendedEvents = ref([
  {
    id: 1,
    title: 'AI技术分享会',
    time: '今晚 8:00',
    participants: 156
  },
  {
    id: 2,
    title: '元宇宙音乐节',
    time: '明天 19:30',
    participants: 892
  },
  {
    id: 3,
    title: '创意设计大赛',
    time: '本周六 14:00',
    participants: 234
  }
])

// 动态数据
const posts = ref([
  {
    id: 1,
    user: {
      name: '星辰漫游者',
      avatar: '/avatars/user1.jpg'
    },
    content: '今天在元宇宙空间里遇到了很多有趣的朋友，AI助手也变得越来越智能了！期待明天的新探索 🚀',
    createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000),
    likes: 24,
    comments: 8,
    isLiked: false,
    images: ['/posts/post1-1.jpg', '/posts/post1-2.jpg']
  },
  {
    id: 2,
    user: {
      name: '数字幻影',
      avatar: '/avatars/user2.jpg'
    },
    content: '刚刚完成了一个超酷的3D场景设计，在赛博朋克城市里漫步的感觉太棒了！谁想来体验一下？',
    createdAt: new Date(Date.now() - 4 * 60 * 60 * 1000),
    likes: 67,
    comments: 15,
    isLiked: true,
    images: ['/posts/post2-1.jpg']
  },
  {
    id: 3,
    user: {
      name: '虚拟旅者',
      avatar: '/avatars/user3.jpg'
    },
    content: '和AI伴侣一起学习新技能，感觉效率提升了好多！推荐大家也试试看～',
    createdAt: new Date(Date.now() - 6 * 60 * 60 * 1000),
    likes: 43,
    comments: 12,
    isLiked: false
  }
])

// 方法
const cancelPost = () => {
  newPostContent.value = ''
  showPostOptions.value = false
}

const publishPost = () => {
  if (!newPostContent.value.trim()) return

  const newPost = {
    id: posts.value.length + 1,
    user: {
      name: authStore.userName,
      avatar: userAvatar.value
    },
    content: newPostContent.value,
    createdAt: new Date(),
    likes: 0,
    comments: 0,
    isLiked: false
  }

  posts.value.unshift(newPost)
  newPostContent.value = ''
  showPostOptions.value = false
  showPostDialog.value = false
}

const toggleLike = (post) => {
  post.isLiked = !post.isLiked
  post.likes += post.isLiked ? 1 : -1
}

const showComments = (post) => {
  // 实现评论功能
  console.log('显示评论:', post.id)
}

const sharePost = (post) => {
  // 实现分享功能
  console.log('分享动态:', post.id)
}

const loadMorePosts = () => {
  // 实现加载更多功能
  console.log('加载更多动态')
}

const startChat = (friend) => {
  // 跳转到聊天页面
  router.push(`/chat/${friend.id}`)
}

const joinGroup = (group) => {
  // 加入群组
  console.log('加入群组:', group.name)
}

const followUser = (user) => {
  // 关注用户
  console.log('关注用户:', user.name)
}

const createGroup = () => {
  if (!newGroup.value.name.trim()) return

  // 创建群组逻辑
  console.log('创建群组:', newGroup.value)
  showGroupDialog.value = false

  // 重置表单
  newGroup.value = {
    name: '',
    description: '',
    privacy: 'public'
  }
}

const viewImage = (image) => {
  // 查看大图
  console.log('查看图片:', image)
}

const formatTime = (date) => {
  const now = new Date()
  const diff = now - date
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  return date.toLocaleDateString()
}

// 生命周期
onMounted(() => {
  // 页面加载时的初始化逻辑
  console.log('社交页面已加载')
})
</script>

<style lang="scss" scoped>
.social-view {
  min-height: calc(100vh - 80px);
}

.glass {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-primary {
  @apply bg-gradient-to-r from-cyan-500 to-blue-600 text-white;
  @apply hover:shadow-lg hover:shadow-cyan-500/25;
}

.btn-secondary {
  @apply bg-gradient-to-r from-purple-500 to-pink-600 text-white;
  @apply hover:shadow-lg hover:shadow-purple-500/25;
}
</style>
