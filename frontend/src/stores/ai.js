import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/modules/http'

export const useAIStore = defineStore('ai', () => {
  // 状态
  const currentPet = ref(null)
  const chatHistory = ref([])
  const isTyping = ref(false)
  const isSpeaking = ref(false)
  const voiceSettings = ref({
    voice: 'zh-CN-XiaoxiaoNeural',
    speed: 1.0,
    pitch: 1.0,
    volume: 0.8,
    enabled: true
  })
  const petSettings = ref({
    personality: 'friendly', // friendly, playful, serious, cute
    mood: 'happy', // happy, sad, excited, calm, sleepy
    energy: 100,
    intimacy: 0,
    appearance: {
      model: 'cat',
      color: '#06b6d4',
      accessories: []
    }
  })
  const aiModels = ref([
    { id: 'gpt-3.5', name: 'GPT-3.5', description: '快速响应，适合日常对话' },
    { id: 'gpt-4', name: 'GPT-4', description: '更智能，更深度的对话体验' },
    { id: 'claude', name: 'Claude', description: '安全可靠，擅长分析推理' }
  ])
  const selectedModel = ref('gpt-3.5')
  const loading = ref(false)

  // 计算属性
  const petName = computed(() => currentPet.value?.name || '小助手')
  const petLevel = computed(() => currentPet.value?.level || 1)
  const petExp = computed(() => currentPet.value?.experience || 0)
  const chatCount = computed(() => chatHistory.value.length)
  const lastMessage = computed(() => chatHistory.value[chatHistory.value.length - 1])

  // 初始化AI助手
  const initializePet = async () => {
    try {
      const savedPet = localStorage.getItem('ai_pet_data')
      if (savedPet) {
        currentPet.value = JSON.parse(savedPet)
      } else {
        // 创建默认宠物
        currentPet.value = {
          id: 'default',
          name: '小星',
          level: 1,
          experience: 0,
          createdAt: new Date().toISOString()
        }
        savePetData()
      }
    } catch (error) {
      console.error('初始化AI助手失败:', error)
    }
  }

  // 保存宠物数据
  const savePetData = () => {
    if (currentPet.value) {
      localStorage.setItem('ai_pet_data', JSON.stringify(currentPet.value))
    }
  }

  // 发送消息
  const sendMessage = async (message, options = {}) => {
    if (!message.trim()) return

    // 添加用户消息到历史记录
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: message,
      timestamp: new Date().toISOString()
    }
    chatHistory.value.push(userMessage)

    // 显示AI正在输入
    isTyping.value = true
    loading.value = true

    try {
      const response = await api.ai.chat({
        message,
        model: selectedModel.value,
        history: chatHistory.value.slice(-10), // 发送最近10条消息作为上下文
        petSettings: petSettings.value,
        ...options
      })

      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: response.data.message,
        timestamp: new Date().toISOString(),
        emotion: response.data.emotion || 'neutral'
      }

      chatHistory.value.push(aiMessage)

      // 更新宠物状态
      if (response.data.petUpdate) {
        updatePetStats(response.data.petUpdate)
      }

      // 语音播放
      if (voiceSettings.value.enabled) {
        await speakMessage(aiMessage.content)
      }

      return { success: true, data: { message: aiMessage.content } }
    } catch (error) {
      console.error('发送消息失败:', error)
      const errorMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: '抱歉，我现在无法回复您，请稍后再试。',
        timestamp: new Date().toISOString(),
        emotion: 'sad'
      }
      chatHistory.value.push(errorMessage)

      return { success: false, error: error.message }
    } finally {
      isTyping.value = false
      loading.value = false
    }
  }

  // 语音播放
  const speakMessage = async (text) => {
    if (!voiceSettings.value.enabled || !text) return

    isSpeaking.value = true

    try {
      // 使用Web Speech API
      if ('speechSynthesis' in window) {
        return new Promise((resolve, reject) => {
          const utterance = new SpeechSynthesisUtterance(text)
          utterance.lang = 'zh-CN'
          utterance.rate = voiceSettings.value.speed
          utterance.pitch = voiceSettings.value.pitch
          utterance.volume = voiceSettings.value.volume

          utterance.onend = () => {
            isSpeaking.value = false
            resolve()
          }

          utterance.onerror = (error) => {
            isSpeaking.value = false
            console.error('语音播放失败:', error)
            reject(error)
          }

          speechSynthesis.speak(utterance)
        })
      } else {
        // 使用后端TTS服务
        const response = await api.ai.textToSpeech({
          text,
          voice: voiceSettings.value.voice,
          speed: voiceSettings.value.speed,
          pitch: voiceSettings.value.pitch
        })

        if (response.data.audioUrl) {
          const audio = new Audio(response.data.audioUrl)
          audio.volume = voiceSettings.value.volume

          return new Promise((resolve, reject) => {
            audio.onended = () => {
              isSpeaking.value = false
              resolve()
            }

            audio.onerror = (error) => {
              isSpeaking.value = false
              reject(error)
            }

            audio.play()
          })
        }
      }
    } catch (error) {
      console.error('语音播放失败:', error)
      isSpeaking.value = false
    }
  }

  // 停止语音播放
  const stopSpeaking = () => {
    if ('speechSynthesis' in window) {
      speechSynthesis.cancel()
    }
    isSpeaking.value = false
  }

  // 更新宠物状态
  const updatePetStats = (updates) => {
    if (currentPet.value) {
      Object.assign(currentPet.value, updates)
      savePetData()
    }
  }

  // 更新宠物名称
  const updatePetName = (name) => {
    if (currentPet.value && name) {
      currentPet.value.name = name;
      savePetData();
    }
  }

  // 更新语音设置
  const updateVoiceSettings = (settings) => {
    Object.assign(voiceSettings.value, settings)
    localStorage.setItem('voice_settings', JSON.stringify(voiceSettings.value))
  }

  // 更新宠物设置
  const updatePetSettings = (settings) => {
    Object.assign(petSettings.value, settings)
    localStorage.setItem('pet_settings', JSON.stringify(petSettings.value))
  }

  // 切换AI模型
  const switchModel = (modelId) => {
    selectedModel.value = modelId
    localStorage.setItem('selected_ai_model', modelId)
  }

  // 清空聊天历史
  const clearChatHistory = () => {
    chatHistory.value = []
    localStorage.removeItem('chat_history')
  }

  // 加载设置
  const loadSettings = () => {
    try {
      const savedVoiceSettings = localStorage.getItem('voice_settings')
      if (savedVoiceSettings) {
        Object.assign(voiceSettings.value, JSON.parse(savedVoiceSettings))
      }

      const savedPetSettings = localStorage.getItem('pet_settings')
      if (savedPetSettings) {
        Object.assign(petSettings.value, JSON.parse(savedPetSettings))
      }

      const savedModel = localStorage.getItem('selected_ai_model')
      if (savedModel) {
        selectedModel.value = savedModel
      }

      const savedChatHistory = localStorage.getItem('chat_history')
      if (savedChatHistory) {
        chatHistory.value = JSON.parse(savedChatHistory)
      }
    } catch (error) {
      console.error('加载设置失败:', error)
    }
  }

  // 保存聊天历史
  const saveChatHistory = () => {
    localStorage.setItem('chat_history', JSON.stringify(chatHistory.value))
  }

  // 文本转语音
  const textToSpeech = async (options) => {
    try {
      loading.value = true;
      const response = await api.ai.textToSpeech({
        text: options.text,
        voice: options.voice || voiceSettings.value.voice,
        speed: options.speed || voiceSettings.value.speed,
        pitch: options.pitch || voiceSettings.value.pitch
      });

      return {
        success: true,
        data: {
          audioUrl: response.data.audioUrl
        }
      };
    } catch (error) {
      console.error('文本转语音失败:', error);
      return {
        success: false,
        error: error.message
      };
    } finally {
      loading.value = false;
    }
  }

  // 语音转文本
  const speechToText = async (options) => {
    try {
      loading.value = true;

      // 创建FormData对象
      const formData = new FormData();
      formData.append('audio', options.audio);

      const response = await api.ai.speechToText(formData);

      return {
        success: true,
        data: {
          text: response.data.text
        }
      };
    } catch (error) {
      console.error('语音转文本失败:', error);
      return {
        success: false,
        error: error.message
      };
    } finally {
      loading.value = false;
    }
  }

  return {
    // 状态
    currentPet,
    chatHistory,
    isTyping,
    isSpeaking,
    voiceSettings,
    petSettings,
    aiModels,
    selectedModel,
    loading,

    // 计算属性
    petName,
    petLevel,
    petExp,
    chatCount,
    lastMessage,

    // 方法
    initializePet,
    sendMessage,
    speakMessage,
    stopSpeaking,
    updatePetStats,
    updatePetName,
    updateVoiceSettings,
    updatePetSettings,
    switchModel,
    clearChatHistory,
    loadSettings,
    saveChatHistory,
    textToSpeech,
    speechToText
  }
})
