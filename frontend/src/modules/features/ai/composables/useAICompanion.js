import { ref, reactive, onMounted, nextTick } from 'vue'
import { useToast } from 'primevue/usetoast'
import * as THREE from 'three'

export function useAICompanion() {
  const toast = useToast()

  // 响应式状态
  const canvasContainer = ref(null)
  const loading = ref(false)
  const scene = ref(null)
  const renderer = ref(null)
  const camera = ref(null)
  const companionModel = ref(null)

  // AI伙伴设置
  const companionSettings = reactive({
    name: '小助手',
    userNickname: '主人',
    model: 'female_01',
    color: 'blue',
    accessories: [],
    personality: {
      type: { code: 'friendly', name: '友善' },
      friendliness: 7,
      energy: 5,
      humor: 6
    },
    behavior: {
      interactionFrequency: { code: 'normal', name: '正常' },
      interactionModes: ['voice', 'text'],
      reminders: {
        schedule: true,
        health: false,
        tasks: true
      }
    },
    relationship: { code: 'assistant', name: '助手' }
  })

  // 模型选项
  const modelOptions = ref([
    {
      value: 'female_01',
      name: '女性助手',
      thumbnail: '/img/models/female_01_thumb.jpg'
    },
    {
      value: 'male_01',
      name: '男性助手',
      thumbnail: '/img/models/male_01_thumb.jpg'
    },
    {
      value: 'robot_01',
      name: '机器人',
      thumbnail: '/img/models/robot_01_thumb.jpg'
    },
    {
      value: 'animal_01',
      name: '动物伙伴',
      thumbnail: '/img/models/animal_01_thumb.jpg'
    }
  ])

  // 颜色选项
  const colorOptions = ref([
    { value: 'blue', hex: '#4287f5', name: '蓝色' },
    { value: 'pink', hex: '#f542d1', name: '粉色' },
    { value: 'green', hex: '#42f554', name: '绿色' },
    { value: 'purple', hex: '#8542f5', name: '紫色' },
    { value: 'orange', hex: '#f5a442', name: '橙色' },
    { value: 'red', hex: '#f54242', name: '红色' }
  ])

  // 附件选项
  const accessoryOptions = ref([
    {
      value: 'glasses',
      name: '眼镜',
      thumbnail: '/img/accessories/glasses_thumb.jpg'
    },
    {
      value: 'hat',
      name: '帽子',
      thumbnail: '/img/accessories/hat_thumb.jpg'
    },
    {
      value: 'bow_tie',
      name: '领结',
      thumbnail: '/img/accessories/bow_tie_thumb.jpg'
    },
    {
      value: 'necklace',
      name: '项链',
      thumbnail: '/img/accessories/necklace_thumb.jpg'
    }
  ])

  // 性格类型
  const personalityTypes = ref([
    { code: 'friendly', name: '友善' },
    { code: 'professional', name: '专业' },
    { code: 'casual', name: '随和' },
    { code: 'energetic', name: '活力' },
    { code: 'calm', name: '沉稳' },
    { code: 'humorous', name: '幽默' }
  ])

  // 互动频率
  const interactionFrequencies = ref([
    { code: 'low', name: '较少' },
    { code: 'normal', name: '正常' },
    { code: 'high', name: '频繁' }
  ])

  // 互动方式
  const interactionModes = ref([
    { value: 'voice', name: '语音', icon: 'pi pi-volume-up' },
    { value: 'text', name: '文字', icon: 'pi pi-comment' },
    { value: 'gesture', name: '手势', icon: 'pi pi-hand' },
    { value: 'expression', name: '表情', icon: 'pi pi-heart' }
  ])

  // 关系类型
  const relationshipTypes = ref([
    { code: 'assistant', name: '助手' },
    { code: 'friend', name: '朋友' },
    { code: 'companion', name: '伙伴' },
    { code: 'teacher', name: '导师' },
    { code: 'pet', name: '宠物' }
  ])

  // 初始化3D场景
  const initThreeJS = async () => {
    if (!canvasContainer.value) return

    try {
      // 创建场景
      scene.value = new THREE.Scene()
      scene.value.background = new THREE.Color(0xf0f0f0)

      // 创建相机
      const aspect = canvasContainer.value.clientWidth / canvasContainer.value.clientHeight
      camera.value = new THREE.PerspectiveCamera(75, aspect, 0.1, 1000)
      camera.value.position.set(0, 1.6, 3)

      // 创建渲染器
      renderer.value = new THREE.WebGLRenderer({ antialias: true })
      renderer.value.setSize(canvasContainer.value.clientWidth, canvasContainer.value.clientHeight)
      renderer.value.shadowMap.enabled = true
      renderer.value.shadowMap.type = THREE.PCFSoftShadowMap
      canvasContainer.value.appendChild(renderer.value.domElement)

      // 添加光源
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
      scene.value.add(ambientLight)

      const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
      directionalLight.position.set(10, 10, 5)
      directionalLight.castShadow = true
      scene.value.add(directionalLight)

      // 加载默认模型
      await loadCompanionModel()

      // 开始渲染循环
      animate()

    } catch (error) {
      console.error('初始化3D场景失败:', error)
      toast.add({
        severity: 'error',
        summary: '错误',
        detail: '无法初始化3D预览',
        life: 3000
      })
    }
  }

  // 加载AI伙伴模型
  const loadCompanionModel = async () => {
    try {
      // 这里应该加载实际的3D模型
      // 目前创建一个简单的占位符
      const geometry = new THREE.CapsuleGeometry(0.5, 1.5, 4, 8)
      const material = new THREE.MeshLambertMaterial({
        color: colorOptions.value.find(c => c.value === companionSettings.color)?.hex || '#4287f5'
      })

      if (companionModel.value) {
        scene.value.remove(companionModel.value)
      }

      companionModel.value = new THREE.Mesh(geometry, material)
      companionModel.value.position.y = 0.75
      companionModel.value.castShadow = true
      scene.value.add(companionModel.value)

      // 添加地面
      const groundGeometry = new THREE.PlaneGeometry(10, 10)
      const groundMaterial = new THREE.MeshLambertMaterial({ color: 0xffffff })
      const ground = new THREE.Mesh(groundGeometry, groundMaterial)
      ground.rotation.x = -Math.PI / 2
      ground.receiveShadow = true
      scene.value.add(ground)

    } catch (error) {
      console.error('加载模型失败:', error)
    }
  }

  // 动画循环
  const animate = () => {
    requestAnimationFrame(animate)

    if (companionModel.value) {
      companionModel.value.rotation.y += 0.005
    }

    if (renderer.value && scene.value && camera.value) {
      renderer.value.render(scene.value, camera.value)
    }
  }

  // 旋转模型
  const rotateModel = () => {
    if (companionModel.value) {
      companionModel.value.rotation.y += Math.PI / 4
    }
  }

  // 放大
  const zoomIn = () => {
    if (camera.value) {
      camera.value.position.z = Math.max(camera.value.position.z - 0.5, 1)
    }
  }

  // 缩小
  const zoomOut = () => {
    if (camera.value) {
      camera.value.position.z = Math.min(camera.value.position.z + 0.5, 10)
    }
  }

  // 选择模型
  const selectModel = (modelValue) => {
    companionSettings.model = modelValue
    loadCompanionModel()
    updateCompanion()
  }

  // 选择颜色
  const selectColor = (colorValue) => {
    companionSettings.color = colorValue
    updateModelColor()
    updateCompanion()
  }

  // 更新模型颜色
  const updateModelColor = () => {
    if (companionModel.value) {
      const color = colorOptions.value.find(c => c.value === companionSettings.color)
      if (color) {
        companionModel.value.material.color.setHex(color.hex.replace('#', '0x'))
      }
    }
  }

  // 切换附件
  const toggleAccessory = (accessoryValue) => {
    const index = companionSettings.accessories.indexOf(accessoryValue)
    if (index > -1) {
      companionSettings.accessories.splice(index, 1)
    } else {
      companionSettings.accessories.push(accessoryValue)
    }
    updateCompanion()
  }

  // 切换互动方式
  const toggleInteractionMode = (modeValue) => {
    const index = companionSettings.behavior.interactionModes.indexOf(modeValue)
    if (index > -1) {
      companionSettings.behavior.interactionModes.splice(index, 1)
    } else {
      companionSettings.behavior.interactionModes.push(modeValue)
    }
    updateCompanion()
  }

  // 更新伙伴设置
  const updateCompanion = () => {
    // 这里可以添加实时更新逻辑
    console.log('伙伴设置已更新:', companionSettings)
  }

  // 保存设置
  const saveSettings = async () => {
    loading.value = true

    try {
      // 保存到本地存储
      localStorage.setItem('ai_companion_settings', JSON.stringify(companionSettings))

      // 这里可以添加保存到服务器的逻辑
      // await apiService.post('/ai/companion/settings', companionSettings)

      toast.add({
        severity: 'success',
        summary: '成功',
        detail: 'AI伙伴设置已保存',
        life: 3000
      })
    } catch (error) {
      console.error('保存设置失败:', error)
      toast.add({
        severity: 'error',
        summary: '错误',
        detail: '保存设置失败，请重试',
        life: 3000
      })
    } finally {
      loading.value = false
    }
  }

  // 重置设置
  const resetSettings = () => {
    Object.assign(companionSettings, {
      name: '小助手',
      userNickname: '主人',
      model: 'female_01',
      color: 'blue',
      accessories: [],
      personality: {
        type: { code: 'friendly', name: '友善' },
        friendliness: 7,
        energy: 5,
        humor: 6
      },
      behavior: {
        interactionFrequency: { code: 'normal', name: '正常' },
        interactionModes: ['voice', 'text'],
        reminders: {
          schedule: true,
          health: false,
          tasks: true
        }
      },
      relationship: { code: 'assistant', name: '助手' }
    })

    loadCompanionModel()

    toast.add({
      severity: 'info',
      summary: '已重置',
      detail: '设置已恢复为默认值',
      life: 3000
    })
  }

  // 加载保存的设置
  const loadSettings = () => {
    try {
      const savedSettings = localStorage.getItem('ai_companion_settings')
      if (savedSettings) {
        const parsed = JSON.parse(savedSettings)
        Object.assign(companionSettings, parsed)
      }
    } catch (error) {
      console.error('加载设置失败:', error)
    }
  }

  // 处理窗口大小变化
  const handleResize = () => {
    if (camera.value && renderer.value && canvasContainer.value) {
      const aspect = canvasContainer.value.clientWidth / canvasContainer.value.clientHeight
      camera.value.aspect = aspect
      camera.value.updateProjectionMatrix()
      renderer.value.setSize(canvasContainer.value.clientWidth, canvasContainer.value.clientHeight)
    }
  }

  // 组件挂载时执行
  onMounted(async () => {
    loadSettings()

    await nextTick()
    await initThreeJS()

    window.addEventListener('resize', handleResize)
  })

  // 组件卸载时清理
  const cleanup = () => {
    window.removeEventListener('resize', handleResize)

    if (renderer.value) {
      renderer.value.dispose()
    }
  }

  return {
    // 状态
    canvasContainer,
    loading,
    companionSettings,
    modelOptions,
    colorOptions,
    accessoryOptions,
    personalityTypes,
    interactionFrequencies,
    interactionModes,
    relationshipTypes,

    // 3D控制方法
    rotateModel,
    zoomIn,
    zoomOut,

    // 设置方法
    selectModel,
    selectColor,
    toggleAccessory,
    toggleInteractionMode,
    updateCompanion,
    saveSettings,
    resetSettings,

    // 清理方法
    cleanup
  }
}
