import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useAIStore } from '@/stores/ai';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

const aiStore = useAIStore();

// 3D模型相关
const modelContainer = ref(null);
let scene, camera, renderer, controls, mixer, clock;
let petModel = null;

// 桌宠基本信息
const petName = computed(() => customPetName.value || aiStore.petName);
const petLevel = computed(() => aiStore.petLevel);
const petExp = computed(() => aiStore.petExp);
const petExpPercentage = computed(() => {
  const nextLevelExp = petLevel.value * 100;
  return (petExp.value / nextLevelExp) * 100;
});

// 桌宠状态
const petEnergy = ref(85);
const petMood = ref('开心');
const moodPercentage = ref(80);
const showEmotionBubble = ref(false);
const showThoughtBubble = ref(false);
const currentThought = ref('');
const emotionIcon = ref('pi pi-heart');
const emotionColor = ref('#ec4899');

// 桌宠设置
const customPetName = ref('');
const selectedModel = ref('cat');
const selectedColor = ref('#06b6d4');
const selectedPersonality = ref('friendly');
const voiceEnabled = ref(true);
const selectedVoice = ref('zh-CN-XiaoxiaoNeural');
const voiceSpeed = ref(1.0);
const userPrompt = ref('');

// 计算属性
const petAvatar = computed(() => `/avatars/pet-${selectedColor.value.replace('#', '')}.png`);

const petPersonalityDesc = computed(() => {
  const descriptions = {
    friendly: '友善、乐于助人',
    playful: '活泼、爱玩耍',
    serious: '严肃、专注',
    cute: '可爱、天真'
  };
  return descriptions[selectedPersonality.value] || '友善、乐于助人';
});

const intimacyLevel = computed(() => {
  const intimacy = aiStore.petSettings.intimacy || 0;
  if (intimacy >= 80) return '挚友';
  if (intimacy >= 60) return '好友';
  if (intimacy >= 40) return '朋友';
  if (intimacy >= 20) return '熟人';
  return '陌生';
});

const intimacyPercentage = computed(() => {
  return aiStore.petSettings.intimacy || 0;
});

const moodColor = computed(() => {
  if (moodPercentage.value >= 80) return 'text-green-400';
  if (moodPercentage.value >= 50) return 'text-yellow-400';
  return 'text-red-400';
});

const moodBarColor = computed(() => {
  if (moodPercentage.value >= 80) return 'bg-gradient-to-r from-green-500 to-emerald-500';
  if (moodPercentage.value >= 50) return 'bg-gradient-to-r from-yellow-500 to-amber-500';
  return 'bg-gradient-to-r from-red-500 to-rose-500';
});

const energyColor = computed(() => {
  if (petEnergy.value >= 70) return 'text-blue-400';
  if (petEnergy.value >= 30) return 'text-yellow-400';
  return 'text-red-400';
});

const energyBarColor = computed(() => {
  if (petEnergy.value >= 70) return 'bg-gradient-to-r from-blue-500 to-cyan-500';
  if (petEnergy.value >= 30) return 'bg-gradient-to-r from-yellow-500 to-amber-500';
  return 'bg-gradient-to-r from-red-500 to-rose-500';
});

// 选项数据
const availableModels = ref([
  { id: 'cat', name: '猫咪' },
  { id: 'dog', name: '小狗' },
  { id: 'robot', name: '机器人' },
  { id: 'slime', name: '史莱姆' }
]);

const personalityOptions = ref([
  { label: '友善型', value: 'friendly' },
  { label: '活泼型', value: 'playful' },
  { label: '严肃型', value: 'serious' },
  { label: '可爱型', value: 'cute' }
]);

const availableVoices = ref([
  { id: 'zh-CN-XiaoxiaoNeural', name: '晓晓 (女声)' },
  { id: 'zh-CN-YunxiNeural', name: '云希 (男声)' },
  { id: 'zh-CN-YunyangNeural', name: '云扬 (男声)' },
  { id: 'zh-CN-XiaohanNeural', name: '晓涵 (女声)' },
  { id: 'zh-CN-XiaomoNeural', name: '晓墨 (女声)' }
]);

const colorOptions = ref([
  '#06b6d4', '#8b5cf6', '#ec4899', '#10b981', '#f59e0b'
]);

const quickPrompts = ref([
  '你好，今天过得怎么样？',
  '给我讲个笑话',
  '你能做什么？',
  '今天天气怎么样？'
]);

// 方法
const initScene = () => {
  // 创建场景
  scene = new THREE.Scene();

  // 创建相机
  camera = new THREE.PerspectiveCamera(
    75,
    modelContainer.value.clientWidth / modelContainer.value.clientHeight,
    0.1,
    1000
  );
  camera.position.set(0, 0, 5);

  // 创建渲染器
  renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: true
  });
  renderer.setSize(modelContainer.value.clientWidth, modelContainer.value.clientHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  modelContainer.value.appendChild(renderer.domElement);

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

const loadPetModel = () => {
  const loader = new GLTFLoader();
  const modelPath = `/models/pets/${selectedModel.value}.glb`;

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
      petModel.traverse((node) => {
        if (node.isMesh && node.material) {
          const color = new THREE.Color(selectedColor.value);
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

const animate = () => {
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

const handleResize = () => {
  if (camera && renderer && modelContainer.value) {
    camera.aspect = modelContainer.value.clientWidth / modelContainer.value.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(modelContainer.value.clientWidth, modelContainer.value.clientHeight);
  }
};

const feedPet = () => {
  // 增加能量
  petEnergy.value = Math.min(100, petEnergy.value + 15);

  // 显示情绪
  showEmotion('pi pi-heart', '#ec4899');

  // 显示思考
  showThought('谢谢你的食物，真好吃！');

  // 增加亲密度
  updateIntimacy(5);
};

const petPet = () => {
  // 增加心情
  moodPercentage.value = Math.min(100, moodPercentage.value + 10);

  // 显示情绪
  showEmotion('pi pi-thumbs-up', '#06b6d4');

  // 显示思考
  showThought('好舒服，继续抚摸我吧~');

  // 增加亲密度
  updateIntimacy(3);
};

const playWithPet = () => {
  // 减少能量，增加心情
  petEnergy.value = Math.max(0, petEnergy.value - 10);
  moodPercentage.value = Math.min(100, moodPercentage.value + 15);

  // 显示情绪
  showEmotion('pi pi-star', '#f59e0b');

  // 显示思考
  showThought('好好玩！我们再玩一会吧！');

  // 增加亲密度
  updateIntimacy(8);

  // 播放动画
  if (mixer && petModel) {
    // 在实际项目中，这里应该切换到"玩耍"动画
    console.log('播放玩耍动画');
  }
};

const restPet = () => {
  // 恢复能量，减少心情
  petEnergy.value = Math.min(100, petEnergy.value + 20);
  moodPercentage.value = Math.max(50, moodPercentage.value - 5);

  // 显示情绪
  showEmotion('pi pi-moon', '#8b5cf6');

  // 显示思考
  showThought('呼~休息一下真舒服...');
};

const showEmotion = (icon, color) => {
  emotionIcon.value = icon;
  emotionColor.value = color;
  showEmotionBubble.value = true;

  setTimeout(() => {
    showEmotionBubble.value = false;
  }, 3000);
};

const showThought = (thought) => {
  currentThought.value = thought;
  showThoughtBubble.value = true;

  setTimeout(() => {
    showThoughtBubble.value = false;
  }, 4000);
};

const updateIntimacy = (amount) => {
  const currentIntimacy = aiStore.petSettings.intimacy || 0;
  aiStore.updatePetSettings({
    intimacy: Math.min(100, currentIntimacy + amount)
  });
};

const sendPrompt = async () => {
  if (!userPrompt.value.trim()) return;

  const message = userPrompt.value.trim();
  userPrompt.value = '';

  // 显示思考
  showThought('让我想想...');

  // 调用AI回复
  await aiStore.sendMessage(message);

  // 消耗能量
  petEnergy.value = Math.max(0, petEnergy.value - 5);
};

const selectQuickPrompt = (prompt) => {
  userPrompt.value = prompt;
  sendPrompt();
};

const saveSettings = () => {
  // 保存AI设置
  aiStore.updatePetSettings({
    personality: selectedPersonality.value,
    appearance: {
      model: selectedModel.value,
      color: selectedColor.value
    }
  });

  // 更新语音设置
  aiStore.updateVoiceSettings({
    enabled: voiceEnabled.value,
    voice: selectedVoice.value,
    speed: voiceSpeed.value
  });

  // 更新名称
  if (customPetName.value) {
    aiStore.updatePetName(customPetName.value);
  }

  // 重新加载模型
  loadPetModel();

  // 显示保存成功提示
  showThought('设置已保存！');
};

// 生命周期钩子
onMounted(async () => {
  // 初始化AI助手
  await aiStore.initializePet();
  await aiStore.loadSettings();

  // 加载设置
  selectedPersonality.value = aiStore.petSettings.personality || 'friendly';
  selectedModel.value = aiStore.petSettings.appearance?.model || 'cat';
  selectedColor.value = aiStore.petSettings.appearance?.color || '#06b6d4';
  voiceEnabled.value = aiStore.voiceSettings.enabled;
  selectedVoice.value = aiStore.voiceSettings.voice;
  voiceSpeed.value = aiStore.voiceSettings.speed;

  // 初始化3D场景
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
    if (modelContainer.value) {
      modelContainer.value.removeChild(renderer.domElement);
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
