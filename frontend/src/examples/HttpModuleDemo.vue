<template>
  <div class="http-module-demo">
    <div class="container mx-auto p-6">
      <h1 class="text-3xl font-bold mb-8 text-center">HTTP模块加密通信演示</h1>

      <!-- 加密配置面板 -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 class="text-xl font-semibold mb-4">加密配置</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium mb-2">加密级别</label>
            <select v-model="encryptLevel" @change="updateEncryptLevel" class="w-full p-2 border rounded">
              <option :value="0">0级 - 不加密</option>
              <option :value="1">1级 - 单层加密</option>
              <option :value="2">2级 - 双层加密</option>
              <option :value="3">3级 - 三层加密</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium mb-2">加密状态</label>
            <button
              @click="toggleEncryption"
              :class="encryptionEnabled ? 'bg-green-500' : 'bg-red-500'"
              class="w-full p-2 text-white rounded hover:opacity-80"
            >
              {{ encryptionEnabled ? '已启用' : '已禁用' }}
            </button>
          </div>
          <div>
            <label class="block text-sm font-medium mb-2">当前状态</label>
            <div class="p-2 bg-gray-100 rounded text-center">
              <span :class="encryptionEnabled ? 'text-green-600' : 'text-red-600'">
                {{ encryptionEnabled ? `${encryptLevel}级加密` : '无加密' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- API测试面板 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">

        <!-- 认证API测试 -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h3 class="text-lg font-semibold mb-4 text-blue-600">认证API测试 (自动高级加密)</h3>

          <!-- 登录测试 -->
          <div class="mb-6">
            <h4 class="font-medium mb-2">用户登录</h4>
            <div class="space-y-2">
              <input v-model="loginData.email" placeholder="邮箱" class="w-full p-2 border rounded">
              <input v-model="loginData.password" type="password" placeholder="密码 (自动3级加密)" class="w-full p-2 border rounded">
              <button @click="testLogin" :disabled="loading" class="w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50">
                {{ loading ? '请求中...' : '测试登录' }}
              </button>
            </div>
          </div>

          <!-- 修改密码测试 -->
          <div class="mb-4">
            <h4 class="font-medium mb-2">修改密码 (整个请求3级加密)</h4>
            <div class="space-y-2">
              <input v-model="passwordData.current" type="password" placeholder="当前密码" class="w-full p-2 border rounded">
              <input v-model="passwordData.new" type="password" placeholder="新密码" class="w-full p-2 border rounded">
              <button @click="testChangePassword" :disabled="loading" class="w-full p-2 bg-orange-500 text-white rounded hover:bg-orange-600 disabled:opacity-50">
                {{ loading ? '请求中...' : '测试修改密码' }}
              </button>
            </div>
          </div>
        </div>

        <!-- AI API测试 -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h3 class="text-lg font-semibold mb-4 text-purple-600">AI API测试 (标准加密)</h3>

          <!-- AI聊天测试 -->
          <div class="mb-6">
            <h4 class="font-medium mb-2">AI聊天</h4>
            <div class="space-y-2">
              <textarea v-model="chatData.message" placeholder="输入消息" class="w-full p-2 border rounded h-20 resize-none"></textarea>
              <select v-model="chatData.model" class="w-full p-2 border rounded">
                <option value="gpt-3.5">GPT-3.5</option>
                <option value="gpt-4">GPT-4</option>
                <option value="claude">Claude</option>
              </select>
              <button @click="testChat" :disabled="loading" class="w-full p-2 bg-purple-500 text-white rounded hover:bg-purple-600 disabled:opacity-50">
                {{ loading ? '请求中...' : '发送聊天' }}
              </button>
            </div>
          </div>

          <!-- 文本转语音测试 -->
          <div class="mb-4">
            <h4 class="font-medium mb-2">文本转语音</h4>
            <div class="space-y-2">
              <input v-model="ttsData.text" placeholder="要转换的文本" class="w-full p-2 border rounded">
              <button @click="testTTS" :disabled="loading" class="w-full p-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:opacity-50">
                {{ loading ? '请求中...' : '转换语音' }}
              </button>
            </div>
          </div>
        </div>

        <!-- 手动加密测试 -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h3 class="text-lg font-semibold mb-4 text-indigo-600">手动加密/解密测试</h3>

          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">原始数据 (JSON格式)</label>
              <textarea v-model="manualData.original" placeholder='{"key": "value"}' class="w-full p-2 border rounded h-20 resize-none"></textarea>
            </div>

            <div class="flex gap-2">
              <button @click="manualEncrypt" class="flex-1 p-2 bg-indigo-500 text-white rounded hover:bg-indigo-600">
                加密数据
              </button>
              <button @click="manualDecrypt" class="flex-1 p-2 bg-teal-500 text-white rounded hover:bg-teal-600">
                解密数据
              </button>
            </div>

            <div>
              <label class="block text-sm font-medium mb-2">加密结果</label>
              <textarea v-model="manualData.encrypted" readonly class="w-full p-2 border rounded h-20 resize-none bg-gray-50"></textarea>
            </div>

            <div>
              <label class="block text-sm font-medium mb-2">解密结果</label>
              <textarea v-model="manualData.decrypted" readonly class="w-full p-2 border rounded h-20 resize-none bg-gray-50"></textarea>
            </div>
          </div>
        </div>

        <!-- 请求日志 -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <h3 class="text-lg font-semibold mb-4 text-gray-600">请求日志</h3>
          <div class="space-y-2 max-h-80 overflow-y-auto">
            <div v-for="(log, index) in requestLogs" :key="index" class="text-sm p-2 rounded" :class="getLogClass(log.type)">
              <div class="font-medium">{{ log.timestamp }} - {{ log.type }}</div>
              <div>{{ log.message }}</div>
              <div v-if="log.details" class="text-xs mt-1 opacity-75">{{ log.details }}</div>
            </div>
            <div v-if="requestLogs.length === 0" class="text-gray-500 text-center py-4">
              暂无请求日志
            </div>
          </div>
          <button @click="clearLogs" class="mt-4 w-full p-2 bg-gray-500 text-white rounded hover:bg-gray-600">
            清空日志
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { request } from '@/modules/http'
import api from '@/modules/http/api'

export default {
  name: 'HttpModuleDemo',
  setup() {
    // 响应式数据
    const encryptLevel = ref(2)
    const encryptionEnabled = ref(true)
    const loading = ref(false)

    const loginData = reactive({
      email: 'demo@example.com',
      password: 'password123'
    })

    const passwordData = reactive({
      current: 'oldpassword',
      new: 'newpassword123'
    })

    const chatData = reactive({
      message: '你好，今天天气怎么样？',
      model: 'gpt-3.5'
    })

    const ttsData = reactive({
      text: '这是一段测试文本，用于演示文本转语音功能。'
    })

    const manualData = reactive({
      original: '{"username": "testuser", "email": "test@example.com"}',
      encrypted: '',
      decrypted: ''
    })

    const requestLogs = ref([])

    // 方法
    const addLog = (type, message, details = null) => {
      requestLogs.value.unshift({
        type,
        message,
        details,
        timestamp: new Date().toLocaleTimeString()
      })

      // 限制日志数量
      if (requestLogs.value.length > 50) {
        requestLogs.value = requestLogs.value.slice(0, 50)
      }
    }

    const getLogClass = (type) => {
      const classes = {
        'SUCCESS': 'bg-green-100 text-green-800',
        'ERROR': 'bg-red-100 text-red-800',
        'INFO': 'bg-blue-100 text-blue-800',
        'WARNING': 'bg-yellow-100 text-yellow-800'
      }
      return classes[type] || 'bg-gray-100 text-gray-800'
    }

    const updateEncryptLevel = () => {
      request.setEncryptLevel(encryptLevel.value)
      addLog('INFO', `设置加密级别为: ${encryptLevel.value}`)
    }

    const toggleEncryption = () => {
      encryptionEnabled.value = !encryptionEnabled.value
      request.setEncryption(encryptionEnabled.value)
      addLog('INFO', `${encryptionEnabled.value ? '启用' : '禁用'}加密`)
    }

    const testLogin = async () => {
      loading.value = true
      try {
        addLog('INFO', '发送登录请求', `邮箱: ${loginData.email}`)

        const result = await api.auth.login({
          email: loginData.email,
          password: loginData.password,
          remember: false
        })

        addLog('SUCCESS', '登录请求成功', JSON.stringify(result, null, 2))
      } catch (error) {
        addLog('ERROR', '登录请求失败', error.message || JSON.stringify(error))
      } finally {
        loading.value = false
      }
    }

    const testChangePassword = async () => {
      loading.value = true
      try {
        addLog('INFO', '发送修改密码请求', '使用3级加密')

        const result = await api.auth.changePassword({
          current_password: passwordData.current,
          password: passwordData.new,
          password_confirmation: passwordData.new
        })

        addLog('SUCCESS', '修改密码请求成功', JSON.stringify(result, null, 2))
      } catch (error) {
        addLog('ERROR', '修改密码请求失败', error.message || JSON.stringify(error))
      } finally {
        loading.value = false
      }
    }

    const testChat = async () => {
      loading.value = true
      try {
        addLog('INFO', '发送AI聊天请求', `模型: ${chatData.model}, 消息: ${chatData.message}`)

        const result = await api.ai.chat({
          message: chatData.message,
          model: chatData.model,
          temperature: 0.8
        })

        addLog('SUCCESS', 'AI聊天请求成功', JSON.stringify(result, null, 2))
      } catch (error) {
        addLog('ERROR', 'AI聊天请求失败', error.message || JSON.stringify(error))
      } finally {
        loading.value = false
      }
    }

    const testTTS = async () => {
      loading.value = true
      try {
        addLog('INFO', '发送文本转语音请求', `文本: ${ttsData.text}`)

        const result = await api.ai.textToSpeech({
          text: ttsData.text,
          voice: 'zh-CN-XiaoxiaoNeural',
          speed: 1.0
        })

        addLog('SUCCESS', '文本转语音请求成功', JSON.stringify(result, null, 2))
      } catch (error) {
        addLog('ERROR', '文本转语音请求失败', error.message || JSON.stringify(error))
      } finally {
        loading.value = false
      }
    }

    const manualEncrypt = () => {
      try {
        const data = JSON.parse(manualData.original)
        const encrypted = request.encrypt(data, encryptLevel.value)
        manualData.encrypted = encrypted
        addLog('SUCCESS', `手动加密成功 (${encryptLevel.value}级)`, `原始长度: ${manualData.original.length}, 加密后长度: ${encrypted.length}`)
      } catch (error) {
        addLog('ERROR', '手动加密失败', error.message)
        manualData.encrypted = ''
      }
    }

    const manualDecrypt = () => {
      try {
        if (!manualData.encrypted) {
          throw new Error('请先加密数据')
        }

        const decrypted = request.decrypt(manualData.encrypted, encryptLevel.value)
        manualData.decrypted = JSON.stringify(decrypted, null, 2)
        addLog('SUCCESS', `手动解密成功 (${encryptLevel.value}级)`)
      } catch (error) {
        addLog('ERROR', '手动解密失败', error.message)
        manualData.decrypted = ''
      }
    }

    const clearLogs = () => {
      requestLogs.value = []
      addLog('INFO', '已清空请求日志')
    }

    // 初始化
    onMounted(() => {
      addLog('INFO', 'HTTP模块演示页面已加载')
      addLog('INFO', `当前加密配置: ${encryptionEnabled.value ? encryptLevel.value + '级加密' : '无加密'}`)
    })

    return {
      // 响应式数据
      encryptLevel,
      encryptionEnabled,
      loading,
      loginData,
      passwordData,
      chatData,
      ttsData,
      manualData,
      requestLogs,

      // 方法
      updateEncryptLevel,
      toggleEncryption,
      testLogin,
      testChangePassword,
      testChat,
      testTTS,
      manualEncrypt,
      manualDecrypt,
      clearLogs,
      getLogClass
    }
  }
}
</script>

<style scoped>
.http-module-demo {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.container {
  max-width: 1200px;
}

/* 滚动条样式 */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 按钮hover效果 */
button:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

/* 输入框焦点效果 */
input:focus, textarea:focus, select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}
</style>
