import { ref, reactive, computed, nextTick, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import aiService from '../api/aiService'

export function useAIChat() {
  const toast = useToast()

  // 响应式状态
  const messages = ref([])
  const userInput = ref('')
  const loading = ref(false)
  const showSettings = ref(false)
  const messagesContainer = ref(null)

  // 用户和AI头像
  const userAvatar = ref('/avatars/default-user.svg')
  const aiAvatar = ref('/img/ai-avatar.svg')

  // AI聊天设置
  const settings = reactive({
    aiRole: { code: 'assistant', name: '智能助手' },
    responseStyle: { code: 'balanced', name: '平衡' },
    responseLength: 3,
    creativity: 0.7
  })

  // AI角色选项
  const aiRoles = ref([
    { code: 'assistant', name: '智能助手' },
    { code: 'teacher', name: '导师' },
    { code: 'friend', name: '朋友' },
    { code: 'expert', name: '专家' },
    { code: 'creative', name: '创意伙伴' }
  ])

  // 回复风格选项
  const responseStyles = ref([
    { code: 'formal', name: '正式' },
    { code: 'casual', name: '轻松' },
    { code: 'balanced', name: '平衡' },
    { code: 'creative', name: '创意' },
    { code: 'technical', name: '技术' }
  ])

  // 发送消息
  const sendMessage = async () => {
    if (!userInput.value.trim() || loading.value) return

    const userMessage = {
      role: 'user',
      content: userInput.value.trim(),
      timestamp: new Date()
    }

    messages.value.push(userMessage)
    const userInputText = userInput.value
    userInput.value = ''
    loading.value = true

    // 滚动到底部
    await nextTick()
    scrollToBottom()

    try {
      // 使用 aiService 调用 API
      const response = await aiService.chat({
        message: userInputText,
        history: messages.value.map(msg => ({
          role: msg.role === 'user' ? 'user' : 'assistant',
          content: msg.content
        })),
        model: 'gpt-3.5',
        temperature: settings.creativity,
        maxTokens: settings.responseLength * 200
      })

      const aiMessage = {
        role: 'assistant',
        content: response.message || `您好！我收到了您的消息："${userInputText}"。`,
        timestamp: new Date()
      }

      messages.value.push(aiMessage)

      // 保存对话历史
      saveConversationHistory()

    } catch (error) {
      console.error('发送消息失败:', error)
      toast.add({
        severity: 'error',
        summary: '错误',
        detail: '发送消息失败，请重试',
        life: 3000
      })

      // 移除用户消息（因为发送失败）
      messages.value.pop()
    } finally {
      loading.value = false
      await nextTick()
      scrollToBottom()
    }
  }

  // 重置对话
  const resetConversation = () => {
    messages.value = []
    clearConversationHistory()
    toast.add({
      severity: 'success',
      summary: '成功',
      detail: '对话已重置',
      life: 2000
    })
  }

  // 应用设置
  const applySettings = () => {
    saveSettings()
    toast.add({
      severity: 'success',
      summary: '设置已保存',
      detail: '新设置将在下次对话中生效',
      life: 2000
    })
  }

  // 格式化消息内容
  const formatMessage = (content) => {
    // 基础的markdown格式化
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code>$1</code>')
      .replace(/\n/g, '<br>')
  }

  // 格式化时间
  const formatTime = (timestamp) => {
    const now = new Date()
    const messageTime = new Date(timestamp)
    const diff = now - messageTime

    if (diff < 60000) {
      return '刚刚'
    } else if (diff < 3600000) {
      return `${Math.floor(diff / 60000)}分钟前`
    } else if (diff < 86400000) {
      return `${Math.floor(diff / 3600000)}小时前`
    } else {
      return messageTime.toLocaleDateString()
    }
  }

  // 滚动到底部
  const scrollToBottom = () => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  }

  // 获取当前对话ID
  const getCurrentConversationId = () => {
    return localStorage.getItem('current_conversation_id') || generateConversationId()
  }

  // 生成对话ID
  const generateConversationId = () => {
    const id = 'conv_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
    localStorage.setItem('current_conversation_id', id)
    return id
  }

  // 保存对话历史
  const saveConversationHistory = () => {
    try {
      const conversationId = getCurrentConversationId()
      localStorage.setItem(`conversation_${conversationId}`, JSON.stringify(messages.value))

      // 保存对话列表
      const conversations = JSON.parse(localStorage.getItem('conversation_list') || '[]')
      const existingIndex = conversations.findIndex(conv => conv.id === conversationId)

      const conversationItem = {
        id: conversationId,
        title: messages.value.length > 0 ? messages.value[0].content.substring(0, 30) + '...' : '新对话',
        lastMessage: messages.value.length > 0 ? messages.value[messages.value.length - 1].content : '',
        timestamp: new Date(),
        messageCount: messages.value.length
      }

      if (existingIndex >= 0) {
        conversations[existingIndex] = conversationItem
      } else {
        conversations.unshift(conversationItem)
      }

      localStorage.setItem('conversation_list', JSON.stringify(conversations.slice(0, 50))) // 只保留最近50个对话
    } catch (error) {
      console.error('保存对话历史失败:', error)
    }
  }

  // 清除对话历史
  const clearConversationHistory = () => {
    const conversationId = getCurrentConversationId()
    localStorage.removeItem(`conversation_${conversationId}`)
    localStorage.removeItem('current_conversation_id')
  }

  // 加载对话历史
  const loadConversationHistory = () => {
    try {
      const conversationId = getCurrentConversationId()
      const savedConversation = localStorage.getItem(`conversation_${conversationId}`)
      if (savedConversation) {
        messages.value = JSON.parse(savedConversation)
      }
    } catch (error) {
      console.error('加载对话历史失败:', error)
    }
  }

  // 保存设置
  const saveSettings = () => {
    try {
      localStorage.setItem('ai_chat_settings', JSON.stringify(settings))
    } catch (error) {
      console.error('保存设置失败:', error)
    }
  }

  // 加载设置
  const loadSettings = () => {
    try {
      const savedSettings = localStorage.getItem('ai_chat_settings')
      if (savedSettings) {
        Object.assign(settings, JSON.parse(savedSettings))
      }
    } catch (error) {
      console.error('加载设置失败:', error)
    }
  }

  // 组件挂载时执行
  onMounted(() => {
    loadSettings()
    loadConversationHistory()

    // 如果没有消息，显示欢迎消息
    if (messages.value.length === 0) {
      messages.value.push({
        role: 'assistant',
        content: '你好！我是你的AI助手，有什么可以帮助你的吗？',
        timestamp: new Date()
      })
    }

    nextTick(() => {
      scrollToBottom()
    })
  })

  return {
    // 状态
    messages,
    userInput,
    loading,
    showSettings,
    messagesContainer,
    userAvatar,
    aiAvatar,
    settings,
    aiRoles,
    responseStyles,

    // 方法
    sendMessage,
    resetConversation,
    applySettings,
    formatMessage,
    formatTime,
    scrollToBottom
  }
}
