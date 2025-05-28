<template>
  <div class="metaverse-container">
    <div class="metaverse-canvas" ref="canvasContainer"></div>

    <div class="metaverse-ui">
      <div class="controls-panel">
        <Button icon="pi pi-home" @click="goToDashboard" class="p-button-rounded p-button-secondary" />
        <Button icon="pi pi-cog" @click="showSettings = true" class="p-button-rounded p-button-secondary" />
        <Button icon="pi pi-comments" @click="showChat = true" class="p-button-rounded p-button-secondary" />
      </div>

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
          <Button label="应用设置" class="w-full" @click="applySettings" />
        </div>
      </Sidebar>

      <Sidebar v-model:visible="showChat" position="right" class="chat-sidebar">
        <h3>社交聊天</h3>
        <div class="chat-messages" ref="chatMessages">
          <div v-for="(msg, index) in chatMessages" :key="index" :class="['chat-message', msg.sender === 'me' ? 'my-message' : 'other-message']">
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
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import { useRouter } from 'vue-router';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

const router = useRouter();

// 3D场景相关
const canvasContainer = ref(null);
let scene, camera, renderer, controls;
let particles, particleSystem;

// UI状态
const showSettings = ref(false);
const showChat = ref(false);

// 设置选项
const settings = ref({
  theme: { name: '太空', value: 'space' },
  lightIntensity: 1,
  particleCount: 1000
});

const themeOptions = [
  { name: '太空', value: 'space' },
  { name: '海底', value: 'underwater' },
  { name: '森林', value: 'forest' },
  { name: '城市', value: 'city' }
];

// 聊天相关
const chatMessages = ref([
  {
    sender: 'other',
    senderName: '小明',
    avatar: 'https://randomuser.me/api/portraits/men/32.jpg',
    text: '你好，欢迎来到元宇宙空间！',
    time: '10:30'
  },
  {
    sender: 'me',
    senderName: '我',
    avatar: 'https://randomuser.me/api/portraits/women/26.jpg',
    text: '谢谢！这里看起来很棒！',
    time: '10:31'
  }
]);
const chatMessages = ref(null);
const newMessage = ref('');

// 初始化Three.js场景
const initThreeJs = () => {
  // 创建场景
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000011);

  // 创建相机
  camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  camera.position.z = 5;

  // 创建渲染器
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  canvasContainer.value.appendChild(renderer.domElement);

  // 添加轨道控制
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;

  // 添加光源
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
  directionalLight.position.set(1, 1, 1);
  scene.add(directionalLight);

  // 创建粒子系统
  createParticles();

  // 开始动画循环
  animate();

  // 处理窗口大小变化
  window.addEventListener('resize', onWindowResize);
};

// 创建粒子系统
const createParticles = () => {
  if (particleSystem) {
    scene.remove(particleSystem);
  }

  const particleCount = settings.value.particleCount;
  const particles = new THREE.BufferGeometry();
  const positions = new Float32Array(particleCount * 3);
  const colors = new Float32Array(particleCount * 3);

  const color = new THREE.Color();

  for (let i = 0; i < particleCount * 3; i += 3) {
    // 位置
    positions[i] = (Math.random() - 0.5) * 20;
    positions[i + 1] = (Math.random() - 0.5) * 20;
    positions[i + 2] = (Math.random() - 0.5) * 20;

    // 颜色
    const theme = settings.value.theme.value;
    if (theme === 'space') {
      color.setHSL(Math.random() * 0.2 + 0.5, 1, 0.5); // 蓝紫色调
    } else if (theme === 'underwater') {
      color.setHSL(Math.random() * 0.1 + 0.5, 1, 0.5); // 蓝绿色调
    } else if (theme === 'forest') {
      color.setHSL(Math.random() * 0.1 + 0.3, 1, 0.5); // 绿色调
    } else if (theme === 'city') {
      color.setHSL(Math.random() * 0.1 + 0.1, 1, 0.5); // 黄色调
    }

    colors[i] = color.r;
    colors[i + 1] = color.g;
    colors[i + 2] = color.b;
  }

  particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  particles.setAttribute('color', new THREE.BufferAttribute(colors, 3));

  const material = new THREE.PointsMaterial({
    size: 0.1,
    vertexColors: true,
    transparent: true,
    opacity: 0.8
  });

  particleSystem = new THREE.Points(particles, material);
  scene.add(particleSystem);
};

// 动画循环
const animate = () => {
  requestAnimationFrame(animate);

  if (particleSystem) {
    particleSystem.rotation.x += 0.0005;
    particleSystem.rotation.y += 0.001;
  }

  controls.update();
  renderer.render(scene, camera);
};

// 处理窗口大小变化
const onWindowResize = () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
};

// 应用设置
const applySettings = () => {
  createParticles();
  showSettings.value = false;
};

// 发送聊天消息
const sendMessage = () => {
  if (!newMessage.value.trim()) return;

  chatMessages.value.push({
    sender: 'me',
    senderName: '我',
    avatar: 'https://randomuser.me/api/portraits/women/26.jpg',
    text: newMessage.value,
    time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  });

  newMessage.value = '';

  // 自动滚动到底部
  setTimeout(() => {
    if (chatMessages.value) {
      chatMessages.value.scrollTop = chatMessages.value.scrollHeight;
    }
  }, 100);
};

// 返回仪表盘
const goToDashboard = () => {
  router.push('/dashboard');
};

// 生命周期钩子
onMounted(() => {
  initThreeJs();
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', onWindowResize);

  // 清理Three.js资源
  if (renderer) {
    renderer.dispose();
  }

  if (controls) {
    controls.dispose();
  }

  if (particleSystem) {
    particleSystem.geometry.dispose();
    particleSystem.material.dispose();
  }
});

// 监听设置变化
watch(() => settings.value.theme, () => {
  createParticles();
});

watch(() => settings.value.lightIntensity, (newValue) => {
  scene.children.forEach(child => {
    if (child instanceof THREE.DirectionalLight) {
      child.intensity = newValue;
    }
  });
});
</script>

<style lang="scss">
@import '@/assets/styles/view/metaverse.scss';
</style>
