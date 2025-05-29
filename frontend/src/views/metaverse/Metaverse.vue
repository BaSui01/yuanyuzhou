<template>
  <div class="metaverse-container">
    <AppNavbar class="metaverse-navbar" />

    <div class="metaverse-header">
      <h1>元宇宙空间</h1>
      <p>探索虚拟世界，与朋友互动，创造无限可能</p>
    </div>

    <div class="metaverse-canvas" ref="canvasContainer"></div>

    <div class="metaverse-ui">
      <div class="controls-panel">
        <Button icon="pi pi-home" @click="goToDashboard" class="p-button-rounded p-button-secondary"
          v-tooltip="'返回首页'" />
        <Button icon="pi pi-cog" @click="showSettings = true" class="p-button-rounded p-button-secondary"
          v-tooltip="'设置'" />
        <Button icon="pi pi-comments" @click="showChat = true" class="p-button-rounded p-button-secondary"
          v-tooltip="'聊天'" />
        <Button icon="pi pi-users" @click="showFriends = true" class="p-button-rounded p-button-secondary"
          v-tooltip="'好友'" />
        <Button icon="pi pi-map" @click="showMap = true" class="p-button-rounded p-button-secondary" v-tooltip="'地图'" />
        <Button icon="pi pi-camera" @click="takeScreenshot" class="p-button-rounded p-button-secondary"
          v-tooltip="'截图'" />
      </div>

      <!-- 设置侧边栏 -->
      <Sidebar v-model:visible="showSettings" position="right" class="settings-sidebar">
        <h3>空间设置</h3>
        <div class="setting-group">
          <label>环境主题</label>
          <Dropdown v-model="settings.theme" :options="themeOptions" optionLabel="name" class="w-full" />
        </div>

        <div class="setting-group">
          <label>光照强度</label>
          <Slider v-model="settings.lightIntensity" :min="0" :max="2" :step="0.1" class="w-full" />
        </div>

        <div class="setting-group">
          <label>粒子数量</label>
          <Slider v-model="settings.particleCount" :min="100" :max="10000" :step="100" class="w-full" />
        </div>

        <div class="setting-group">
          <label>角色外观</label>
          <div class="avatar-options">
            <div v-for="(avatar, index) in avatarOptions" :key="index"
              :class="['avatar-option', settings.avatarId === avatar.id ? 'selected' : '']"
              @click="settings.avatarId = avatar.id">
              <img :src="avatar.thumbnail" :alt="avatar.name" />
              <span>{{ avatar.name }}</span>
            </div>
          </div>
        </div>

        <div class="setting-group">
          <label>性能设置</label>
          <div class="performance-options">
            <Dropdown v-model="settings.quality" :options="qualityOptions" optionLabel="name" class="w-full" />
            <div class="setting-item">
              <Checkbox v-model="settings.enableShadows" binary inputId="shadows" />
              <label for="shadows">启用阴影</label>
            </div>
            <div class="setting-item">
              <Checkbox v-model="settings.enablePostProcessing" binary inputId="postProcessing" />
              <label for="postProcessing">后期处理</label>
            </div>
          </div>
        </div>

        <div class="setting-group">
          <Button label="应用设置" class="w-full" @click="applySettings" />
        </div>
      </Sidebar>

      <!-- 聊天侧边栏 -->
      <Sidebar v-model:visible="showChat" position="right" class="chat-sidebar">
        <h3>社交聊天</h3>
        <div class="chat-messages" ref="chatMessages">
          <div v-for="(msg, index) in chatMessages" :key="index"
            :class="['chat-message', msg.sender === 'me' ? 'my-message' : 'other-message']">
            <div class="message-avatar">
              <Avatar :image="msg.avatar" shape="circle" />
            </div>
            <div class="message-content">
              <div class="message-sender">{{ msg.senderName }}</div>
              <div class="message-text">{{ msg.text }}</div>
              <div class="message-time">{{ msg.time }}</div>
            </div>
          </div>
        </div>

        <div class="chat-input">
          <InputText v-model="newMessage" placeholder="输入消息..." class="w-full" @keyup.enter="sendMessage" />
          <Button icon="pi pi-send" @click="sendMessage" />
        </div>
      </Sidebar>

      <!-- 好友侧边栏 -->
      <Sidebar v-model:visible="showFriends" position="right" class="friends-sidebar">
        <h3>在线好友</h3>
        <div class="friends-list">
          <div v-for="(friend, index) in onlineFriends" :key="index" class="friend-item">
            <Avatar :image="friend.avatar" shape="circle" />
            <div class="friend-info">
              <div class="friend-name">{{ friend.name }}</div>
              <div class="friend-status">{{ friend.status }}</div>
            </div>
            <div class="friend-actions">
              <Button icon="pi pi-comments" text rounded @click="startChat(friend)" v-tooltip="'私聊'" />
              <Button icon="pi pi-map-marker" text rounded @click="teleportToFriend(friend)" v-tooltip="'传送'" />
            </div>
          </div>
        </div>
      </Sidebar>

      <!-- 地图对话框 -->
      <Dialog v-model:visible="showMap" header="元宇宙地图" modal class="map-dialog">
        <div class="map-container">
          <img src="/img/metaverse-map.svg" alt="元宇宙地图" class="metaverse-map" />

          <div v-for="(location, index) in mapLocations" :key="index" class="map-marker"
            :style="{ left: location.x + '%', top: location.y + '%' }" @click="teleportToLocation(location)">
            <i class="pi pi-map-marker"></i>
            <div class="location-tooltip">
              <div class="location-name">{{ location.name }}</div>
              <div class="location-users">当前: {{ location.users }}人</div>
            </div>
          </div>
        </div>
        <div class="map-actions">
          <Button label="关闭" @click="showMap = false" />
        </div>
      </Dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import AppNavbar from '@/components/layout/AppNavbar.vue';

// 导入PrimeVue组件
import Button from 'primevue/button';
import Sidebar from 'primevue/sidebar';
import Dropdown from 'primevue/dropdown';
import Slider from 'primevue/slider';
import InputText from 'primevue/inputtext';
import Avatar from 'primevue/avatar';
import Dialog from 'primevue/dialog';
import Checkbox from 'primevue/checkbox';

const router = useRouter();
const canvasContainer = ref(null);

// UI控制状态
const showSettings = ref(false);
const showChat = ref(false);
const showFriends = ref(false);
const showMap = ref(false);

// 设置相关
const settings = reactive({
  theme: { name: '太空站', value: 'space-station' },
  lightIntensity: 1.0,
  particleCount: 1000,
  avatarId: 'avatar1',
  quality: { name: '高', value: 'high' },
  enableShadows: true,
  enablePostProcessing: true
});

const themeOptions = [
  { name: '太空站', value: 'space-station' },
  { name: '海底世界', value: 'underwater' },
  { name: '未来城市', value: 'future-city' },
  { name: '幻想森林', value: 'fantasy-forest' },
  { name: '沙漠绿洲', value: 'desert-oasis' }
];

const avatarOptions = [
  { id: 'avatar1', name: '未来战士', thumbnail: '/avatars/avatar1-thumb.svg' },
  { id: 'avatar2', name: '科技精灵', thumbnail: '/avatars/avatar2-thumb.svg' },
  { id: 'avatar3', name: '机械师', thumbnail: '/avatars/avatar3-thumb.svg' },
  { id: 'avatar4', name: '星际旅人', thumbnail: '/avatars/avatar4-thumb.svg' }
];

const qualityOptions = [
  { name: '低', value: 'low' },
  { name: '中', value: 'medium' },
  { name: '高', value: 'high' },
  { name: '超高', value: 'ultra' }
];

// 聊天相关
const chatMessages = ref([
  {
    sender: 'other',
    senderName: '星际导游',
    text: '欢迎来到元宇宙空间站！需要帮助请随时联系我。',
    time: '刚刚',
    avatar: '/avatars/guide-avatar.svg'
  }
]);
const newMessage = ref('');

// 好友列表
const onlineFriends = ref([
  { id: 1, name: '宇宙漫游者', status: '太空站中心', avatar: '/avatars/friend1.svg' },
  { id: 2, name: '数据收集者', status: '科技实验室', avatar: '/avatars/friend2.svg' },
  { id: 3, name: '星际艺术家', status: '创意中心', avatar: '/avatars/friend3.svg' }
]);

// 地图位置
const mapLocations = ref([
  { id: 1, name: '中央广场', x: 50, y: 50, users: 42 },
  { id: 2, name: '科技实验室', x: 75, y: 30, users: 18 },
  { id: 3, name: '创意中心', x: 30, y: 70, users: 23 },
  { id: 4, name: '休闲花园', x: 20, y: 25, users: 12 },
  { id: 5, name: '虚拟市场', x: 65, y: 75, users: 35 }
]);

// 方法
const goToDashboard = () => {
  router.push('/Dashboard');
};

const applySettings = () => {
  // 应用设置到3D场景
  console.log('应用设置:', settings);
  showSettings.value = false;

  // 这里将调用3D渲染引擎的方法
};

const sendMessage = () => {
  if (!newMessage.value.trim()) return;

  chatMessages.value.push({
    sender: 'me',
    senderName: '我',
    text: newMessage.value,
    time: '刚刚',
    avatar: '/avatars/default-user.svg'
  });

  newMessage.value = '';

  // 模拟回复
  setTimeout(() => {
    chatMessages.value.push({
      sender: 'other',
      senderName: '星际导游',
      text: '我收到了您的消息，请问还有其他需要帮助的吗？',
      time: '刚刚',
      avatar: '/avatars/guide-avatar.svg'
    });
  }, 1000);
};

const startChat = (friend) => {
  showChat.value = true;
  // 添加与好友的聊天
  chatMessages.value.push({
    sender: 'system',
    senderName: '系统',
    text: `已连接到与${friend.name}的私聊`,
    time: '刚刚',
    avatar: '/avatars/system-avatar.svg'
  });
};

const teleportToFriend = (friend) => {
  console.log('传送到好友位置:', friend);
  // 这里将调用3D引擎的传送方法
};

const teleportToLocation = (location) => {
  console.log('传送到位置:', location);
  showMap.value = false;
  // 这里将调用3D引擎的传送方法
};

const takeScreenshot = () => {
  console.log('拍摄截图');
  // 这里将调用截图功能
};

// 生命周期钩子
onMounted(() => {
  // 初始化3D场景
  console.log('初始化元宇宙场景');
  // 这里将调用3D引擎初始化方法
});

onUnmounted(() => {
  // 清理3D资源
  console.log('清理元宇宙场景资源');
  // 这里将调用3D引擎清理方法
});
</script>

<style lang="scss" scoped>
.metaverse-container {
  width: 100%;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

.metaverse-navbar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: 10;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
}

.metaverse-header {
  text-align: center;
  padding: 80px 20px 20px;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.7) 0%, rgba(0, 0, 0, 0) 100%);
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: 5;
  color: #fff;

  h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
  }

  p {
    font-size: 1.1rem;
    opacity: 0.8;
    max-width: 600px;
    margin: 0 auto;
  }
}

.metaverse-canvas {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #090030, #1f0050);
  position: absolute;
  top: 0;
  left: 0;
}

.metaverse-ui {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;

  >* {
    pointer-events: auto;
  }
}

.controls-panel {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 15px;

  button {
    width: 50px;
    height: 50px;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(5px);
    border: 2px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;

    &:hover {
      background: rgba(0, 0, 0, 0.8);
      transform: scale(1.1);
    }
  }
}

.settings-sidebar,
.chat-sidebar,
.friends-sidebar {
  padding: 20px;
  background: rgba(30, 30, 50, 0.9) !important;
  backdrop-filter: blur(10px);
  border-left: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;

  h3 {
    margin-top: 0;
    margin-bottom: 20px;
    font-size: 1.5rem;
    font-weight: 600;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 10px;
  }
}

.setting-group {
  margin-bottom: 20px;

  label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
  }
}

.avatar-options {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;

  .avatar-option {
    border-radius: 8px;
    padding: 10px;
    text-align: center;
    cursor: pointer;
    border: 2px solid transparent;
    transition: all 0.3s;

    &:hover {
      background: rgba(255, 255, 255, 0.1);
    }

    &.selected {
      border-color: #4caf50;
      background: rgba(76, 175, 80, 0.1);
    }

    img {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      margin-bottom: 5px;
    }

    span {
      display: block;
      font-size: 0.9rem;
    }
  }
}

.setting-item {
  display: flex;
  align-items: center;
  margin-top: 10px;

  label {
    margin-left: 10px;
    margin-bottom: 0;
  }
}

.chat-messages {
  height: 300px;
  overflow-y: auto;
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
  gap: 15px;

  .chat-message {
    display: flex;
    gap: 10px;

    &.my-message {
      flex-direction: row-reverse;

      .message-content {
        align-items: flex-end;

        .message-text {
          background: #4caf50;
          border-radius: 15px 15px 0 15px;
        }

        .message-sender {
          text-align: right;
        }

        .message-time {
          text-align: right;
        }
      }
    }

    .message-avatar {
      flex-shrink: 0;
    }

    .message-content {
      display: flex;
      flex-direction: column;

      .message-sender {
        font-size: 0.8rem;
        margin-bottom: 3px;
        color: rgba(255, 255, 255, 0.7);
      }

      .message-text {
        background: rgba(255, 255, 255, 0.1);
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0;
        max-width: 250px;
      }

      .message-time {
        font-size: 0.75rem;
        margin-top: 3px;
        color: rgba(255, 255, 255, 0.5);
      }
    }
  }
}

.chat-input {
  display: flex;
  gap: 10px;

  .p-inputtext {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: white;
  }
}

.friends-list {
  display: flex;
  flex-direction: column;
  gap: 15px;

  .friend-item {
    display: flex;
    align-items: center;
    padding: 10px;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.05);

    .friend-info {
      flex: 1;
      margin-left: 15px;

      .friend-name {
        font-weight: 500;
      }

      .friend-status {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.6);
      }
    }

    .friend-actions {
      display: flex;
      gap: 5px;
    }
  }
}

.map-dialog {
  .p-dialog-content {
    padding: 0;
  }

  .map-container {
    position: relative;
    width: 600px;
    height: 400px;
    overflow: hidden;

    .metaverse-map {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .map-marker {
      position: absolute;
      transform: translate(-50%, -100%);
      color: #ff4081;
      font-size: 1.5rem;
      cursor: pointer;
      transition: all 0.3s;

      &:hover {
        transform: translate(-50%, -100%) scale(1.2);

        .location-tooltip {
          opacity: 1;
          transform: translateY(0);
        }
      }

      .location-tooltip {
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%) translateY(10px);
        background: rgba(0, 0, 0, 0.8);
        padding: 5px 10px;
        border-radius: 5px;
        min-width: 120px;
        opacity: 0;
        transition: all 0.3s;
        pointer-events: none;

        &:after {
          content: '';
          position: absolute;
          top: 100%;
          left: 50%;
          margin-left: -5px;
          border-width: 5px;
          border-style: solid;
          border-color: rgba(0, 0, 0, 0.8) transparent transparent transparent;
        }

        .location-name {
          font-weight: 500;
          text-align: center;
          margin-bottom: 3px;
        }

        .location-users {
          font-size: 0.8rem;
          color: rgba(255, 255, 255, 0.7);
          text-align: center;
        }
      }
    }
  }

  .map-actions {
    padding: 15px;
    display: flex;
    justify-content: flex-end;
  }
}

@media (max-width: 768px) {
  .controls-panel {
    left: 10px;

    button {
      width: 40px;
      height: 40px;
    }
  }

  .map-container {
    width: 100% !important;
    height: 300px !important;
  }
}
</style>
