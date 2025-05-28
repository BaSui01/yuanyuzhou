<template>
  <div class="pet-assistant">
    <!-- 浮动桌宠 -->
    <div
      v-if="showPet"
      class="pet-container"
      :class="{ 'expanded': expanded, 'dragging': isDragging }"
      :style="petPosition"
      @mousedown="startDrag"
    >
      <!-- 3D模型容器 -->
      <div ref="petModelContainer" class="pet-model-container"></div>

      <!-- 表情气泡 -->
      <div v-if="showEmotionBubble" class="emotion-bubble">
        <i :class="emotionIcon" class="text-2xl" :style="{ color: emotionColor }"></i>
      </div>

      <!-- 思考气泡 -->
      <div v-if="showThoughtBubble" class="thought-bubble">
        <p>{{ currentThought }}</p>
      </div>

      <!-- 控制按钮 -->
      <div class="pet-controls">
        <button class="control-button" @click.stop="toggleChat">
          <i class="pi pi-comments"></i>
        </button>
        <button class="control-button" @click.stop="toggleExpand">
          <i :class="expanded ? 'pi pi-minus' : 'pi pi-plus'"></i>
        </button>
        <button class="control-button" @click.stop="togglePet">
          <i class="pi pi-times"></i>
        </button>
      </div>
    </div>

    <!-- 聊天窗口 -->
    <div v-if="showChat" class="chat-window" :style="chatPosition">
      <div class="chat-header">
        <div class="flex items-center">
          <div class="avatar">
            <img :src="petAvatar" alt="AI助手" />
          </div>
          <h3>{{ petName }}</h3>
        </div>
        <button class="close-button" @click="toggleChat">
          <i class="pi pi-times"></i>
        </button>
      </div>

      <div ref="chatMessages" class="chat-messages">
        <div
          v-for="(msg, index) in chatHistory"
          :key="index"
          class="message"
          :class="msg.sender === 'ai' ? 'ai' : 'user'"
        >
          <div class="message-content">
            <p>{{ msg.text }}</p>
            <span class="timestamp">{{ formatTime(msg.timestamp) }}</span>
          </div>
        </div>

        <div v-if="isTyping" class="message ai">
          <div class="message-content">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>

      <div class="chat-input">
        <input
          v-model="userInput"
          type="text"
          placeholder="输入消息..."
          @keyup.enter="sendMessage"
        />
        <button class="send-button" @click="sendMessage" :disabled="!userInput.trim()">
          <i class="pi pi-send"></i>
        </button>
      </div>
    </div>

    <!-- 浮动按钮 -->
    <div v-if="!showPet" class="pet-toggle" @click="togglePet">
      <i class="pi pi-comments"></i>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick, watch } from 'vue';
import { useAIStore } from '@/stores/ai';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

const aiStore = useAIStore();

// 状态变量
const showPet = ref(true);
const expanded = ref(false);
const showChat = ref(false);
const isDragging = ref(false);
const petPosition = ref({ left: 'auto', right: '20px', top: '20px', bottom: 'auto' });
const dragOffset = ref({ x: 0, y: 0 });
const showEmotionBubble = ref(false);
const showThoughtBubble = ref(false);
const currentThought = ref('');
const emotionIcon = ref('pi pi-heart');
const emotionColor = ref('#ec4899');
const isTyping = ref(false);
const userInput = ref('');
const chatMessages = ref(null);

// 3D模型相关
const petModelContainer = ref(null);
let scene, camera, renderer, controls, mixer, clock;
let petModel = null;

// 桌宠信息
const petName = computed(() => aiStore.petName || '小助手');
const petAvatar = computed(() => `/avatars/pet-${aiStore.petSettings?.appearance?.color?.replace('#', '') || '06b6d4'}.png`);

// 聊天历史
const chatHistory = ref([
  {
    sender: 'ai',
    text: '你好！我是你的AI助手，有什么可以帮助你的吗？',
    timestamp: new Date()
  }
]);

// 聊天窗口位置
const chatPosition = computed(() => {
  // 根据宠物位置计算聊天窗口位置
  const pos = { ...petPosition.value };
  if (pos.right !== 'auto') {
    pos.right = '20px';
    pos.left = 'auto';
  } else {
    pos.left = '20px';
    pos.right = 'auto';
  }

  if (pos.bottom !== 'auto') {
    pos.bottom = '80px';
    pos.top = 'auto';
  } else {
    pos.top = '80px';
    pos.bottom = 'auto';
  }

  return pos;
});

// 初始化3D场景
const initScene = () => {
  if (!petModelContainer.value) return;

  // 创建场景
  scene = new THREE.Scene();

  // 创建相机
  camera = new THREE.PerspectiveCamera(
    75,
    petModelContainer.value.clientWidth / petModelContainer.value.clientHeight,
    0.1,
    1000
  );
  camera.position.set(0, 0, 5);

  // 创建渲染器
  renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: true
  });
  renderer.setSize(petModelContainer.value.clientWidth, petModelContainer.value.clientHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  petModelContainer.value.appendChild(renderer.domElement);

  // 添加控制器
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.rotateSpeed = 0.5;
  controls.enableZoom = false;

  // 添加灯光
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
  directionalLight.position.set(5, 5, 5);
  scene.add(directionalLight);

  // 初始化时钟
  clock = new THREE.Clock();

  // 加载模型
  loadPetModel();

  // 开始动画循环
  animate();
};

// 加载桌宠模型
const loadPetModel = () => {
  const loader = new GLTFLoader();
  const modelType = aiStore.petSettings?.appearance?.model || 'cat';
  const modelPath = `/models/pets/${modelType}.glb`;

  loader.load(
    modelPath,
    (gltf) => {
      // 移除之前的模型
      if (petModel) {
        scene.remove(petModel);
      }

      petModel = gltf.scene;
      petModel.scale.set(2, 2, 2);
      petModel.position.y = -1;
      scene.add(petModel);

      // 设置动画混合器
      mixer = new THREE.AnimationMixer(petModel);
      if (gltf.animations && gltf.animations.length) {
        const idleAction = mixer.clipAction(gltf.animations[0]);
        idleAction.play();
      }

      // 应用颜色
      const color = new THREE.Color(aiStore.petSettings?.appearance?.color || '#06b6d4');
      petModel.traverse((node) => {
        if (node.isMesh && node.material) {
          if (node.material.name === 'Main') {
            node.material.color = color;
          }
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
};

// 动画循环
const animate = () => {
  if (!scene || !camera || !renderer) return;

  requestAnimationFrame(animate);

  // 更新控制器
  controls.update();

  // 更新动画混合器
  if (mixer) {
    const delta = clock.getDelta();
    mixer.update(delta);
  }

  // 渲染场景
  renderer.render(scene, camera);
};

// 处理窗口大小变化
const handleResize = () => {
  if (camera && renderer && petModelContainer.value) {
    camera.aspect = petModelContainer.value.clientWidth / petModelContainer.value.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(petModelContainer.value.clientWidth, petModelContainer.value.clientHeight);
  }
};

// 显示/隐藏桌宠
const togglePet = () => {
  showPet.value = !showPet.value;

  if (showPet.value) {
    // 重新初始化场景
    nextTick(() => {
      initScene();
    });

    // 显示欢迎信息
    showThought('欢迎回来！');
  } else {
    // 关闭聊天窗口
    showChat.value = false;
  }
};

// 展开/收起桌宠
const toggleExpand = () => {
  expanded.value = !expanded.value;
};

// 显示/隐藏聊天窗口
const toggleChat = () => {
  showChat.value = !showChat.value;

  if (showChat.value) {
    // 滚动到底部
    nextTick(() => {
      scrollToBottom();
    });
  }
};

// 开始拖动
const startDrag = (event) => {
  if (event.target.closest('.control-button')) return;

  isDragging.value = true;

  // 计算点击位置与元素左上角的偏移
  const rect = event.currentTarget.getBoundingClientRect();
  dragOffset.value.x = event.clientX - rect.left;
  dragOffset.value.y = event.clientY - rect.top;

  // 添加移动和停止拖动的事件监听
  document.addEventListener('mousemove', onDrag);
  document.addEventListener('mouseup', stopDrag);
};

// 拖动中
const onDrag = (event) => {
  if (!isDragging.value) return;

  const x = event.clientX - dragOffset.value.x;
  const y = event.clientY - dragOffset.value.y;

  // 计算是靠近哪个边缘
  const windowWidth = window.innerWidth;
  const windowHeight = window.innerHeight;

  // 确定水平位置
  if (x < windowWidth / 2) {
    petPosition.value.left = `${Math.max(0, x)}px`;
    petPosition.value.right = 'auto';
  } else {
    petPosition.value.right = `${Math.max(0, windowWidth - x - 60)}px`;
    petPosition.value.left = 'auto';
  }

  // 确定垂直位置
  if (y < windowHeight / 2) {
    petPosition.value.top = `${Math.max(0, y)}px`;
    petPosition.value.bottom = 'auto';
  } else {
    petPosition.value.bottom = `${Math.max(0, windowHeight - y - 60)}px`;
    petPosition.value.top = 'auto';
  }
};

// 停止拖动
const stopDrag = () => {
  isDragging.value = false;

  // 移除事件监听
  document.removeEventListener('mousemove', onDrag);
  document.removeEventListener('mouseup', stopDrag);

  // 保存位置到本地存储
  localStorage.setItem('pet_position', JSON.stringify(petPosition.value));
};

// 显示情绪气泡
const showEmotion = (icon, color) => {
  emotionIcon.value = icon;
  emotionColor.value = color;
  showEmotionBubble.value = true;

  setTimeout(() => {
    showEmotionBubble.value = false;
  }, 3000);
};

// 显示思考气泡
const showThought = (thought) => {
  currentThought.value = thought;
  showThoughtBubble.value = true;

  setTimeout(() => {
    showThoughtBubble.value = false;
  }, 4000);
};

// 发送消息
const sendMessage = async () => {
  if (!userInput.value.trim()) return;

  const message = userInput.value.trim();
  userInput.value = '';

  // 添加用户消息到聊天历史
  chatHistory.value.push({
    sender: 'user',
    text: message,
    timestamp: new Date()
  });

  // 滚动到底部
  scrollToBottom();

  // 显示AI正在输入
  isTyping.value = true;

  try {
    // 调用AI API获取回复
    const response = await aiStore.sendMessage(message);

    // 添加AI回复到聊天历史
    chatHistory.value.push({
      sender: 'ai',
      text: response.data.message,
      timestamp: new Date()
    });

    // 显示情绪
    showEmotion('pi pi-comments', '#06b6d4');

    // 如果启用了语音，播放语音
    if (aiStore.voiceSettings.enabled) {
      playVoice(response.data.message);
    }
  } catch (error) {
    console.error('发送消息失败:', error);

    // 添加错误消息
    chatHistory.value.push({
      sender: 'ai',
      text: '抱歉，我遇到了一些问题，无法回答你的问题。',
      timestamp: new Date()
    });

    // 显示情绪
    showEmotion('pi pi-exclamation-circle', '#ef4444');
  } finally {
    // 隐藏输入指示器
    isTyping.value = false;

    // 滚动到底部
    scrollToBottom();
  }
};

// 播放语音
const playVoice = async (text) => {
  try {
    const response = await aiStore.textToSpeech({
      text,
      voice: aiStore.voiceSettings.voice,
      speed: aiStore.voiceSettings.speed,
      pitch: 1.0
    });

    if (response.success && response.data.audioUrl) {
      const audio = new Audio(response.data.audioUrl);
      audio.play();
    }
  } catch (error) {
    console.error('语音播放失败:', error);
  }
};

// 滚动到底部
const scrollToBottom = () => {
  if (chatMessages.value) {
    chatMessages.value.scrollTop = chatMessages.value.scrollHeight;
  }
};

// 格式化时间
const formatTime = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
};

// 监听聊天历史变化，自动滚动到底部
watch(chatHistory, () => {
  nextTick(() => {
    scrollToBottom();
  });
});

// 生命周期钩子
onMounted(async () => {
  // 初始化AI助手
  await aiStore.initializePet();

  // 加载保存的位置
  const savedPosition = localStorage.getItem('pet_position');
  if (savedPosition) {
    try {
      petPosition.value = JSON.parse(savedPosition);
    } catch (e) {
      console.error('解析保存的位置失败:', e);
    }
  }

  // 初始化3D场景
  nextTick(() => {
    initScene();
  });

  // 添加窗口大小调整监听
  window.addEventListener('resize', handleResize);

  // 显示欢迎信息
  setTimeout(() => {
    showThought('有什么需要帮助的吗？');
  }, 1000);
});

onBeforeUnmount(() => {
  // 移除事件监听
  window.removeEventListener('resize', handleResize);

  // 清理Three.js资源
  if (renderer) {
    renderer.dispose();
    if (petModelContainer.value) {
      petModelContainer.value.removeChild(renderer.domElement);
    }
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
.pet-assistant {
  position: fixed;
  z-index: 1000;

  .pet-container {
    position: fixed;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    transition: all 0.3s ease;
    cursor: move;

    &.expanded {
      width: 120px;
      height: 120px;
      border-radius: 16px;
    }

    &.dragging {
      opacity: 0.8;
    }

    .pet-model-container {
      width: 100%;
      height: 100%;
    }

    .pet-controls {
      position: absolute;
      top: 0;
      right: 0;
      display: flex;
      flex-direction: column;
      opacity: 0;
      transition: opacity 0.2s ease;

      .control-button {
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(0, 0, 0, 0.5);
        border: none;
        color: white;
        font-size: 10px;
        cursor: pointer;

        &:hover {
          background: rgba(0, 0, 0, 0.7);
        }
      }
    }

    &:hover .pet-controls {
      opacity: 1;
    }

    .emotion-bubble {
      position: absolute;
      top: -30px;
      right: -10px;
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      padding: 8px;
      border-radius: 50%;
      animation: float 3s ease-in-out infinite;
    }

    .thought-bubble {
      position: absolute;
      top: -40px;
      left: -20px;
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      padding: 8px;
      border-radius: 12px;
      max-width: 150px;
      animation: fadeIn 0.5s ease-out;

      p {
        margin: 0;
        font-size: 12px;
        color: white;
      }

      &::before {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 15px;
        width: 0;
        height: 0;
        border-left: 8px solid transparent;
        border-right: 8px solid transparent;
        border-top: 8px solid rgba(255, 255, 255, 0.1);
      }
    }
  }

  .chat-window {
    position: fixed;
    width: 300px;
    height: 400px;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);

    .chat-header {
      padding: 12px 16px;
      background: rgba(255, 255, 255, 0.05);
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);

      .avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        overflow: hidden;
        margin-right: 10px;

        img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }
      }

      h3 {
        margin: 0;
        font-size: 16px;
        color: white;
      }

      .close-button {
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255, 255, 255, 0.1);
        border: none;
        border-radius: 50%;
        color: white;
        cursor: pointer;

        &:hover {
          background: rgba(255, 255, 255, 0.2);
        }
      }
    }

    .chat-messages {
      flex: 1;
      padding: 16px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 12px;

      &::-webkit-scrollbar {
        width: 4px;
      }

      &::-webkit-scrollbar-track {
        background: transparent;
      }

      &::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 2px;
      }

      .message {
        max-width: 80%;

        &.user {
          align-self: flex-end;

          .message-content {
            background: rgba(6, 182, 212, 0.3);
            border-radius: 16px 16px 4px 16px;
          }
        }

        &.ai {
          align-self: flex-start;

          .message-content {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 16px 16px 16px 4px;
          }
        }

        .message-content {
          padding: 10px 12px;

          p {
            margin: 0;
            color: white;
            font-size: 14px;
            line-height: 1.4;
            word-break: break-word;
          }

          .timestamp {
            display: block;
            font-size: 10px;
            margin-top: 4px;
            color: rgba(255, 255, 255, 0.5);
            text-align: right;
          }

          .typing-indicator {
            display: flex;
            align-items: center;
            gap: 4px;

            span {
              display: block;
              width: 8px;
              height: 8px;
              border-radius: 50%;
              background: rgba(255, 255, 255, 0.5);
              animation: typing 1.5s infinite ease-in-out;

              &:nth-child(1) {
                animation-delay: 0s;
              }

              &:nth-child(2) {
                animation-delay: 0.2s;
              }

              &:nth-child(3) {
                animation-delay: 0.4s;
              }
            }
          }
        }
      }
    }

    .chat-input {
      padding: 12px 16px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      gap: 8px;

      input {
        flex: 1;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 8px 16px;
        color: white;
        outline: none;

        &:focus {
          border-color: rgba(6, 182, 212, 0.5);
        }

        &::placeholder {
          color: rgba(255, 255, 255, 0.5);
        }
      }

      .send-button {
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(6, 182, 212, 0.7);
        border: none;
        border-radius: 50%;
        color: white;
        cursor: pointer;

        &:hover {
          background: rgba(6, 182, 212, 0.9);
        }

        &:disabled {
          background: rgba(255, 255, 255, 0.1);
          color: rgba(255, 255, 255, 0.3);
          cursor: not-allowed;
        }
      }
    }
  }

  .pet-toggle {
    position: fixed;
    right: 20px;
    bottom: 20px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: rgba(6, 182, 212, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: all 0.3s ease;

    &:hover {
      transform: scale(1.1);
      background: rgba(6, 182, 212, 0.9);
    }
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-4px);
  }
}
</style>
