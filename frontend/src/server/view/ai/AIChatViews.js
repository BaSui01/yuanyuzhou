import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useAIStore } from '@/stores/ai'
import { useConfirm } from 'primevue/useconfirm'

const authStore = useAuthStore()
const aiStore = useAIStore()
const confirm = useConfirm()

// 用户信息
const userAvatar = computed(() => authStore.userAvatar)

// AI助手信息
const petName = computed(() => aiStore.petName)
const petAvatar = computed(() => `/avatars/pet-${aiStore.petSettings.appearance.color.replace('#', '')}.png`)
const isTyping = computed(() => aiStore.isTyping)
const isSpeaking = computed(() => aiStore.isSpeaking)
const chatHistory = computed(() => aiStore.chatHistory)
const aiModels = computed(() => aiStore.aiModels)

// 聊天状态
const currentMessage = ref('')
const messagesContainer = ref(null)
const isRecording = ref(false)
const showSettings = ref(false)

// AI设置
const selectedModel = ref(aiStore.selectedModel)
const temperature = ref(0.8)
const maxTokens = ref(1000)

// 语音设置
const voiceEnabled = ref(aiStore.voiceSettings.enabled)
const voiceVolume = ref(aiStore.voiceSettings.volume * 100)
const voiceSpeed = ref(aiStore.voiceSettings.speed)
const selectedVoice = ref('zh-CN-XiaoxiaoNeural')
const availableVoices = ref([
  { id: 'zh-CN-XiaoxiaoNeural', name: '晓晓 (女声)' },
  { id: 'zh-CN-YunxiNeural', name: '云希 (男声)' },
  { id: 'zh-CN-YunyangNeural', name: '云扬 (男声)' },
  { id: 'zh-CN-XiaohanNeural', name: '晓涵 (女声)' },
  { id: 'zh-CN-XiaomoNeural', name: '晓墨 (女声)' }
])

// 快捷回复
const quickReplies = ref([
  '你好，请问你能做什么？',
  '给我讲个笑话',
  '今天天气怎么样？',
  '推荐一部电影'
])

// 对话历史
const chatSessions = ref([
  { id: 'current', title: '当前对话', date: new Date(), preview: '最近的对话内容...' },
  { id: 'session1', title: '关于AI的讨论', date: new Date(Date.now() - 86400000), preview: '人工智能的发展趋势...' },
  { id: 'session2', title: '电影推荐', date: new Date(Date.now() - 172800000), preview: '根据您的喜好，推荐以下电影...' }
])

// 提示词库
const promptSuggestions = ref([
  { id: 1, title: '创意写作', content: '请帮我写一篇关于未来科技的短文，字数在300字左右。' },
  { id: 2, title: '代码解释', content: '请解释以下代码的功能和工作原理：[粘贴代码]' },
  { id: 3, title: '旅行计划', content: '我计划去[城市]旅行3天，请推荐必去景点和行程安排。' }
])

// 方法
const sendMessage = async () => {
  if (!currentMessage.value.trim() || isTyping.value) return

  const message = currentMessage.value.trim()
  currentMessage.value = ''

  try {
    await aiStore.sendMessage(message, {
      model: selectedModel.value,
      temperature: temperature.value,
      maxTokens: maxTokens.value
    })

    scrollToBottom()
  } catch (error) {
    console.error('发送消息失败:', error)
  }
}

const handleEnterKey = (event) => {
  if (event.shiftKey) return // 允许Shift+Enter换行

  event.preventDefault()
  sendMessage()
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const toggleVoice = () => {
  voiceEnabled.value = !voiceEnabled.value
  aiStore.updateVoiceSettings({ enabled: voiceEnabled.value })
}

const toggleRecording = async () => {
  if (isRecording.value) {
    // 停止录音
    isRecording.value = false
    // 实际项目中应该调用语音识别API
  } else {
    // 开始录音
    try {
      isRecording.value = true

      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        // 实际项目中应该实现录音和语音识别
        console.log('录音已开始', stream)
      }
    } catch (error) {
      console.error('无法访问麦克风:', error)
      isRecording.value = false
    }
  }
}

const speakMessage = (text) => {
  aiStore.speakMessage(text)
}

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    // 显示复制成功提示
    window.app.addNotification({
      type: 'success',
      title: '复制成功',
      message: '文本已复制到剪贴板',
      duration: 2000
    })
  } catch (error) {
    console.error('复制失败:', error)
  }
}

const switchModel = (modelId) => {
  selectedModel.value = modelId
  aiStore.switchModel(modelId)
}

const useQuickReply = (reply) => {
  currentMessage.value = reply
  sendMessage()
}

const usePrompt = (prompt) => {
  currentMessage.value = prompt
}

const startNewChat = () => {
  confirm.require({
    message: '开始新对话将清空当前对话历史，是否继续？',
    header: '确认操作',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: '确认',
    rejectLabel: '取消',
    accept: () => {
      aiStore.clearChatHistory()
    }
  })
}

const loadChatSession = (sessionId) => {
  // 实际项目中应该从API加载历史对话
  console.log('加载对话:', sessionId)
}

const confirmClearChat = () => {
  confirm.require({
    message: '确定要清空所有对话历史吗？',
    header: '确认清空',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: '确认',
    rejectLabel: '取消',
    accept: () => {
      aiStore.clearChatHistory()
    }
  })
}

const saveSettings = () => {
  // 保存语音设置
  aiStore.updateVoiceSettings({
    enabled: voiceEnabled.value,
    volume: voiceVolume.value / 100,
    speed: voiceSpeed.value,
    voice: selectedVoice.value
  })

  // 关闭设置对话框
  showSettings.value = false
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

const formatDate = (date) => {
  const now = new Date()
  const diff = now - date

  if (diff < 86400000) { // 24小时内
    return '今天'
  } else if (diff < 172800000) { // 48小时内
    return '昨天'
  } else {
    return date.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' })
  }
}

// 监听聊天历史变化，自动滚动到底部
watch(() => chatHistory.value.length, () => {
  scrollToBottom()
})

// 生命周期钩子
onMounted(() => {
  scrollToBottom()
})
