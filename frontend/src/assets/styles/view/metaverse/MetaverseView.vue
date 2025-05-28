<template>
  <div class="metaverse-view">
    <!-- 3D场景容器 -->
    <div ref="sceneContainer" class="scene-container"></div>

    <!-- 控制面板 -->
    <div class="control-panel glass-panel">
      <div class="panel-header">
        <h3>元宇宙控制台</h3>
        <Button icon="pi pi-cog" class="p-button-text p-button-rounded" @click="showSettings = true" />
      </div>

      <div class="panel-content">
        <div class="control-group">
          <h4>场景选择</h4>
          <div class="scene-selector">
            <div
              v-for="scene in availableScenes"
              :key="scene.id"
              class="scene-option"
              :class="{ 'active': currentScene === scene.id }"
              @click="changeScene(scene.id)"
            >
              <img :src="scene.thumbnail" :alt="scene.name" />
              <span>{{ scene.name }}</span>
            </div>
          </div>
        </div>

        <div class="control-group">
          <h4>角色控制</h4>
          <div class="avatar-controls">
            <Button label="行走模式" icon="pi pi-directions" :class="{ 'p-button-outlined': !walkMode }" @click="toggleWalkMode" />
            <Button label="飞行模式" icon="pi pi-send" :class="{ 'p-button-outlined': walkMode }" @click="toggleWalkMode" />
            <Button label="跳舞" icon="pi pi-spin pi-star" @click="triggerAnimation('dance')" />
            <Button label="打招呼" icon="pi pi-thumbs-up" @click="triggerAnimation('wave')" />
          </div>
        </div>

        <div class="control-group">
          <h4>社交互动</h4>
          <div class="online-users">
            <div v-for="user in onlineUsers" :key="user.id" class="online-user">
              <Avatar :image="user.avatar" size="small" />
              <span>{{ user.name }}</span>
              <div class="user-actions">
                <Button icon="pi pi-comments" class="p-button-text p-button-rounded p-button-sm" @click="startChat(user.id)" />
                <Button icon="pi pi-video" class="p-button-text p-button-rounded p-button-sm" @click="startCall(user.id)" />
              </div>
            </div>

            <div v-if="onlineUsers.length === 0" class="empty-state">
              <i class="pi pi-users text-2xl mb-2"></i>
              <p>暂无其他用户在线</p>
            </div>
          </div>
        </div>
      </div>

      <div class="panel-footer">
        <Button label="退出空间" icon="pi pi-sign-out" class="p-button-danger" @click="exitMetaverse" />
      </div>
    </div>

    <!-- 聊天窗口 -->
    <div v-if="showChat" class="chat-window glass-panel">
      <div class="panel-header">
        <div class="flex items-center">
          <Avatar :image="chatTarget.avatar" size="small" />
          <h3 class="ml-2">{{ chatTarget.name }}</h3>
        </div>
        <Button icon="pi pi-times" class="p-button-text p-button-rounded" @click="closeChat" />
      </div>

      <div class="chat-messages">
        <div v-for="(msg, index) in chatMessages" :key="index" class="message" :class="msg.sender === 'me' ? 'sent' : 'received'">
          <div class="message-content">
            <p>{{ msg.text }}</p>
            <span class="timestamp">{{ formatTime(msg.timestamp) }}</span>
          </div>
        </div>
      </div>

      <div class="chat-input">
        <InputText v-model="newMessage" placeholder="输入消息..." @keyup.enter="sendMessage" />
        <Button icon="pi pi-send" @click="sendMessage" />
      </div>
    </div>

    <!-- 设置对话框 -->
    <Dialog v-model:visible="showSettings" header="元宇宙设置" :style="{width: '500px'}" modal>
      <div class="settings-content">
        <div class="setting-group">
          <h4>图形质量</h4>
          <div class="quality-options">
            <div class="p-field-radiobutton">
              <RadioButton v-model="graphicsQuality" inputId="quality1" name="quality" value="low" />
              <label for="quality1">低</label>
            </div>
            <div class="p-field-radiobutton">
              <RadioButton v-model="graphicsQuality" inputId="quality2" name="quality" value="medium" />
              <label for="quality2">中</label>
            </div>
            <div class="p-field-radiobutton">
              <RadioButton v-model="graphicsQuality" inputId="quality3" name="quality" value="high" />
              <label for="quality3">高</label>
            </div>
          </div>
        </div>

        <div class="setting-group">
          <h4>音效</h4>
          <div class="flex items-center justify-between">
            <label>背景音乐</label>
            <InputSwitch v-model="audioSettings.bgm" />
          </div>
          <div class="flex items-center justify-between mt-2">
            <label>环境音效</label>
            <InputSwitch v-model="audioSettings.sfx" />
          </div>
          <div class="mt-2">
            <label>音量</label>
            <Slider v-model="audioSettings.volume" />
          </div>
        </div>

        <div class="setting-group">
          <h4>隐私设置</h4>
          <div class="flex items-center justify-between">
            <label>显示我的在线状态</label>
            <InputSwitch v-model="privacySettings.showOnlineStatus" />
          </div>
          <div class="flex items-center justify-between mt-2">
            <label>允许陌生人发起对话</label>
            <InputSwitch v-model="privacySettings.allowStrangerChat" />
          </div>
        </div>
      </div>

      <template #footer>
        <Button label="取消" icon="pi pi-times" class="p-button-text" @click="showSettings = false" />
        <Button label="保存" icon="pi pi-check" @click="saveSettings" />
      </template>
    </Dialog>

    <!-- 桌宠AI助手 -->
    <PetAssistant />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { useAuthStore } from '@/stores/auth';
import PetAssistant from '@/components/ai/PetAssistant.vue';

// 路由
const router = useRouter();
const authStore = useAuthStore();

// 3D场景相关
const sceneContainer = ref(null);
let scene, camera, renderer, controls;
let animationMixer, clock;
let avatarModel;

// 状态管理
const currentScene = ref('space-station');
const walkMode = ref(true);
const showSettings = ref(false);
const showChat = ref(false);
const chatTarget = ref({});
const chatMessages = ref([]);
const newMessage = ref('');
const graphicsQuality = ref('medium');
const audioSettings = ref({
  bgm: true,
  sfx: true,
  volume: 80
});
const privacySettings = ref({
  showOnlineStatus: true,
  allowStrangerChat: false
});

// 场景选项
const availableScenes = ref([
  {
    id: 'space-station',
    name: '空间站',
    thumbnail: '/images/scenes/space-station.jpg'
  },
  {
    id: 'forest',
    name: '魔法森林',
    thumbnail: '/images/scenes/forest.jpg'
  },
  {
    id: 'cyberpunk',
    name: '赛博城市',
    thumbnail: '/images/scenes/cyberpunk.jpg'
  },
  {
    id: 'beach',
    name: '海滩度假',
    thumbnail: '/images/scenes/beach.jpg'
  }
]);

// 在线用户
const onlineUsers = ref([
  {
    id: 'user1',
    name: '星辰漫游者',
    avatar: '/avatars/user1.jpg'
  },
  {
    id: 'user2',
    name: '数字幻影',
    avatar: '/avatars/user2.jpg'
  }
]);

// 初始化3D场景
const initScene = () => {
  // 创建场景
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000000);

  // 创建相机
  camera = new THREE.PerspectiveCamera(
    75,
    sceneContainer.value.clientWidth / sceneContainer.value.clientHeight,
    0.1,
    1000
  );
  camera.position.set(0, 1.6, 5);

  // 创建渲染器
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(sceneContainer.value.clientWidth, sceneContainer.value.clientHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.shadowMap.enabled = true;
  sceneContainer.value.appendChild(renderer.domElement);

  // 添加控制器
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;

  // 添加灯光
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
  directionalLight.position.set(5, 10, 7.5);
  directionalLight.castShadow = true;
  scene.add(directionalLight);

  // 初始化时钟
  clock = new THREE.Clock();

  // 加载场景
  loadScene(currentScene.value);

  // 加载用户角色
  loadAvatar();

  // 开始动画循环
  animate();
};

// 加载场景模型
const loadScene = (sceneId) => {
  // 清除当前场景中的对象（保留灯光和相机）
  scene.traverse((object) => {
    if (object.type === 'Mesh' && object !== avatarModel) {
      scene.remove(object);
    }
  });

  // 根据场景ID加载不同的模型和环境
  const loader = new GLTFLoader();

  // 添加地面
  const groundGeometry = new THREE.PlaneGeometry(100, 100);
  const groundMaterial = new THREE.MeshStandardMaterial({
    color: 0x333333,
    roughness: 0.8,
    metalness: 0.2
  });
  const ground = new THREE.Mesh(groundGeometry, groundMaterial);
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  scene.add(ground);

  // 根据场景ID加载特定模型
  let modelPath = '';
  switch (sceneId) {
    case 'space-station':
      modelPath = '/models/space-station.glb';
      scene.background = new THREE.Color(0x000011);
      break;
    case 'forest':
      modelPath = '/models/forest.glb';
      scene.background = new THREE.Color(0x113322);
      break;
    case 'cyberpunk':
      modelPath = '/models/cyberpunk.glb';
      scene.background = new THREE.Color(0x110022);
      break;
    case 'beach':
      modelPath = '/models/beach.glb';
      scene.background = new THREE.Color(0x88CCFF);
      break;
  }

  // 加载场景模型
  if (modelPath) {
    loader.load(
      modelPath,
      (gltf) => {
        scene.add(gltf.scene);
        gltf.scene.traverse((node) => {
          if (node.isMesh) {
            node.castShadow = true;
            node.receiveShadow = true;
          }
        });
      },
      (xhr) => {
        console.log((xhr.loaded / xhr.total * 100) + '% loaded');
      },
      (error) => {
        console.error('加载模型出错:', error);
      }
    );
  }
};

// 加载用户角色模型
const loadAvatar = () => {
  const loader = new GLTFLoader();

  loader.load(
    '/models/avatar.glb',
    (gltf) => {
      avatarModel = gltf.scene;
      avatarModel.scale.set(0.5, 0.5, 0.5);
      avatarModel.position.y = 0;
      scene.add(avatarModel);

      // 设置动画混合器
      animationMixer = new THREE.AnimationMixer(avatarModel);
      if (gltf.animations && gltf.animations.length) {
        // 播放默认动画
        const idleAction = animationMixer.clipAction(gltf.animations[0]);
        idleAction.play();
      }

      avatarModel.traverse((node) => {
        if (node.isMesh) {
          node.castShadow = true;
        }
      });
    },
    (xhr) => {
      console.log((xhr.loaded / xhr.total * 100) + '% loaded');
    },
    (error) => {
      console.error('加载角色模型出错:', error);
    }
  );
};

// 动画循环
const animate = () => {
  requestAnimationFrame(animate);

  // 更新控制器
  controls.update();

  // 更新动画混合器
  if (animationMixer) {
    const delta = clock.getDelta();
    animationMixer.update(delta);
  }

  // 渲染场景
  renderer.render(scene, camera);
};

// 窗口大小调整处理
const handleResize = () => {
  if (camera && renderer && sceneContainer.value) {
    camera.aspect = sceneContainer.value.clientWidth / sceneContainer.value.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(sceneContainer.value.clientWidth, sceneContainer.value.clientHeight);
  }
};

// 场景切换
const changeScene = (sceneId) => {
  currentScene.value = sceneId;
  loadScene(sceneId);
};

// 切换行走/飞行模式
const toggleWalkMode = () => {
  walkMode.value = !walkMode.value;

  // 在实际项目中，这里应该修改控制器和物理约束
  if (walkMode.value) {
    // 启用重力和碰撞检测
  } else {
    // 禁用重力和碰撞检测
  }
};

// 触发角色动画
const triggerAnimation = (animationType) => {
  if (!animationMixer || !avatarModel) return;

  // 在实际项目中，这里应该加载并播放相应的动画
  console.log(`播放${animationType}动画`);
};

// 开始聊天
const startChat = (userId) => {
  const user = onlineUsers.value.find(u => u.id === userId);
  if (!user) return;

  chatTarget.value = user;
  chatMessages.value = [
    {
      sender: 'other',
      text: '嗨，你好！欢迎来到元宇宙空间！',
      timestamp: new Date()
    }
  ];
  showChat.value = true;
};

// 发起通话
const startCall = (userId) => {
  const user = onlineUsers.value.find(u => u.id === userId);
  if (!user) return;

  // 在实际项目中，这里应该调用WebRTC相关API
  console.log(`与${user.name}发起通话`);
};

// 发送消息
const sendMessage = () => {
  if (!newMessage.value.trim()) return;

  chatMessages.value.push({
    sender: 'me',
    text: newMessage.value,
    timestamp: new Date()
  });

  newMessage.value = '';

  // 模拟回复
  setTimeout(() => {
    chatMessages.value.push({
      sender: 'other',
      text: '收到你的消息了！这是一个自动回复。',
      timestamp: new Date()
    });
  }, 1000);
};

// 关闭聊天
const closeChat = () => {
  showChat.value = false;
};

// 保存设置
const saveSettings = () => {
  // 应用图形质量设置
  switch (graphicsQuality.value) {
    case 'low':
      renderer.setPixelRatio(1);
      break;
    case 'medium':
      renderer.setPixelRatio(window.devicePixelRatio);
      break;
    case 'high':
      renderer.setPixelRatio(window.devicePixelRatio * 1.5);
      break;
  }

  // 保存设置到本地存储
  localStorage.setItem('metaverse_settings', JSON.stringify({
    graphicsQuality: graphicsQuality.value,
    audioSettings: audioSettings.value,
    privacySettings: privacySettings.value
  }));

  showSettings.value = false;
};

// 退出元宇宙
const exitMetaverse = () => {
  router.push('/dashboard');
};

// 格式化时间
const formatTime = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
};

// 生命周期钩子
onMounted(async () => {
  // 加载保存的设置
  const savedSettings = localStorage.getItem('metaverse_settings');
  if (savedSettings) {
    const settings = JSON.parse(savedSettings);
    graphicsQuality.value = settings.graphicsQuality || 'medium';
    audioSettings.value = settings.audioSettings || { bgm: true, sfx: true, volume: 80 };
    privacySettings.value = settings.privacySettings || { showOnlineStatus: true, allowStrangerChat: false };
  }

  // 初始化3D场景
  await nextTick();
  initScene();

  // 添加窗口大小调整监听
  window.addEventListener('resize', handleResize);
});

onBeforeUnmount(() => {
  // 移除事件监听
  window.removeEventListener('resize', handleResize);

  // 清理Three.js资源
  if (renderer) {
    renderer.dispose();
    sceneContainer.value.removeChild(renderer.domElement);
  }

  if (scene) {
    scene.traverse((object) => {
      if (object.geometry) object.geometry.dispose();
      if (object.material) {
        if (Array.isArray(object.material)) {
          object.material.forEach(material => material.dispose());
        } else {
          object.material.dispose();
        }
      }
    });
  }
});
</script>

<style lang="scss" scoped>
@use '../../styles/view/metaverse.scss';
</style>
