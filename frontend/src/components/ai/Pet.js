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
const petAvatar = computed(() => `/img/pet-${aiStore.petSettings?.appearance?.color?.replace('#', '') || '06b6d4'}.png`);

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
