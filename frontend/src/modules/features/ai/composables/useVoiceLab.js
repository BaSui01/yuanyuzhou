import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useToast } from 'primevue/usetoast'

export function useVoiceLab() {
  const toast = useToast()

  // 响应式状态
  const isPlaying = ref(false)
  const previewText = ref('你好，我是您的AI助手。这是我的声音预览。')
  const visualizationContainer = ref(null)
  const audioContext = ref(null)
  const analyser = ref(null)
  const animationId = ref(null)
  const currentAudio = ref(null)

  // 语音设置
  const voiceSettings = reactive({
    voiceType: { code: 'female_01', name: '女声 - 温柔' },
    language: { code: 'zh-CN', name: '中文（简体）' },
    speed: 1.0,
    pitch: 1.0
  })

  // 声音类型选项
  const voiceTypes = ref([
    { code: 'female_01', name: '女声 - 温柔' },
    { code: 'female_02', name: '女声 - 活泼' },
    { code: 'female_03', name: '女声 - 专业' },
    { code: 'male_01', name: '男声 - 沉稳' },
    { code: 'male_02', name: '男声 - 年轻' },
    { code: 'male_03', name: '男声 - 磁性' },
    { code: 'child_01', name: '童声 - 可爱' },
    { code: 'robot_01', name: '机器音' }
  ])

  // 语言选项
  const languages = ref([
    { code: 'zh-CN', name: '中文（简体）' },
    { code: 'zh-TW', name: '中文（繁体）' },
    { code: 'en-US', name: '英语（美式）' },
    { code: 'en-GB', name: '英语（英式）' },
    { code: 'ja-JP', name: '日语' },
    { code: 'ko-KR', name: '韩语' },
    { code: 'fr-FR', name: '法语' },
    { code: 'de-DE', name: '德语' },
    { code: 'es-ES', name: '西班牙语' }
  ])

  // 初始化音频上下文
  const initAudioContext = () => {
    try {
      audioContext.value = new (window.AudioContext || window.webkitAudioContext)()
      analyser.value = audioContext.value.createAnalyser()
      analyser.value.fftSize = 256
    } catch (error) {
      console.error('初始化音频上下文失败:', error)
    }
  }

  // 播放预览
  const playPreview = async () => {
    if (!previewText.value.trim()) return

    isPlaying.value = true

    try {
      // 停止当前播放的音频
      if (currentAudio.value) {
        currentAudio.value.pause()
        currentAudio.value = null
      }

      // 这里应该调用TTS API生成音频
      // 目前使用Web Speech API作为演示
      if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(previewText.value)

        // 设置语音参数
        utterance.rate = voiceSettings.speed
        utterance.pitch = voiceSettings.pitch
        utterance.lang = voiceSettings.language.code

        // 尝试使用指定的声音
        const voices = speechSynthesis.getVoices()
        const targetVoice = voices.find(voice =>
          voice.lang.includes(voiceSettings.language.code.split('-')[0])
        )
        if (targetVoice) {
          utterance.voice = targetVoice
        }

        utterance.onstart = () => {
          startVisualization()
        }

        utterance.onend = () => {
          isPlaying.value = false
          stopVisualization()
        }

        utterance.onerror = (error) => {
          console.error('语音合成错误:', error)
          isPlaying.value = false
          stopVisualization()
          toast.add({
            severity: 'error',
            summary: '错误',
            detail: '语音播放失败',
            life: 3000
          })
        }

        speechSynthesis.speak(utterance)

      } else {
        // 如果不支持Web Speech API，模拟播放
        await simulateAudioPlayback()
      }

    } catch (error) {
      console.error('播放预览失败:', error)
      isPlaying.value = false
      toast.add({
        severity: 'error',
        summary: '错误',
        detail: '播放预览失败，请重试',
        life: 3000
      })
    }
  }

  // 停止预览
  const stopPreview = () => {
    if ('speechSynthesis' in window) {
      speechSynthesis.cancel()
    }

    if (currentAudio.value) {
      currentAudio.value.pause()
      currentAudio.value = null
    }

    isPlaying.value = false
    stopVisualization()
  }

  // 模拟音频播放（用于不支持Web Speech API的情况）
  const simulateAudioPlayback = () => {
    return new Promise((resolve) => {
      startVisualization()

      // 根据文本长度估算播放时间
      const estimatedDuration = (previewText.value.length / 10) * 1000 / voiceSettings.speed

      setTimeout(() => {
        isPlaying.value = false
        stopVisualization()
        resolve()
      }, estimatedDuration)
    })
  }

  // 开始声音可视化
  const startVisualization = () => {
    if (!visualizationContainer.value) return

    const canvas = document.createElement('canvas')
    canvas.width = visualizationContainer.value.clientWidth
    canvas.height = 100
    canvas.style.width = '100%'
    canvas.style.height = '100px'

    visualizationContainer.value.innerHTML = ''
    visualizationContainer.value.appendChild(canvas)

    const ctx = canvas.getContext('2d')

    const draw = () => {
      if (!isPlaying.value) return

      // 清除画布
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      // 绘制声音波形（模拟）
      ctx.strokeStyle = '#4287f5'
      ctx.lineWidth = 2
      ctx.beginPath()

      const time = Date.now() * 0.01
      const amplitude = 30
      const frequency = 0.1

      for (let x = 0; x < canvas.width; x++) {
        const y = canvas.height / 2 +
          Math.sin((x * frequency) + time) * amplitude *
          (Math.random() * 0.5 + 0.5) // 添加随机性

        if (x === 0) {
          ctx.moveTo(x, y)
        } else {
          ctx.lineTo(x, y)
        }
      }

      ctx.stroke()

      animationId.value = requestAnimationFrame(draw)
    }

    draw()
  }

  // 停止声音可视化
  const stopVisualization = () => {
    if (animationId.value) {
      cancelAnimationFrame(animationId.value)
      animationId.value = null
    }

    if (visualizationContainer.value) {
      visualizationContainer.value.innerHTML = '<p class="no-audio">暂无音频播放</p>'
    }
  }

  // 更新语音预览
  const updateVoicePreview = () => {
    // 如果正在播放，重新开始播放以应用新设置
    if (isPlaying.value) {
      stopPreview()
      setTimeout(() => {
        playPreview()
      }, 100)
    }
  }

  // 保存设置
  const saveSettings = () => {
    try {
      localStorage.setItem('voice_lab_settings', JSON.stringify(voiceSettings))
      toast.add({
        severity: 'success',
        summary: '成功',
        detail: '语音设置已保存',
        life: 3000
      })
    } catch (error) {
      console.error('保存设置失败:', error)
      toast.add({
        severity: 'error',
        summary: '错误',
        detail: '保存设置失败',
        life: 3000
      })
    }
  }

  // 重置设置
  const resetSettings = () => {
    Object.assign(voiceSettings, {
      voiceType: { code: 'female_01', name: '女声 - 温柔' },
      language: { code: 'zh-CN', name: '中文（简体）' },
      speed: 1.0,
      pitch: 1.0
    })

    toast.add({
      severity: 'info',
      summary: '已重置',
      detail: '语音设置已恢复为默认值',
      life: 3000
    })
  }

  // 加载保存的设置
  const loadSettings = () => {
    try {
      const savedSettings = localStorage.getItem('voice_lab_settings')
      if (savedSettings) {
        const parsed = JSON.parse(savedSettings)
        Object.assign(voiceSettings, parsed)
      }
    } catch (error) {
      console.error('加载设置失败:', error)
    }
  }

  // 处理窗口大小变化
  const handleResize = () => {
    if (visualizationContainer.value && isPlaying.value) {
      // 重新创建可视化画布
      stopVisualization()
      startVisualization()
    }
  }

  // 组件挂载时执行
  onMounted(() => {
    loadSettings()
    initAudioContext()
    stopVisualization() // 显示初始状态

    window.addEventListener('resize', handleResize)

    // 确保语音列表已加载（Web Speech API）
    if ('speechSynthesis' in window) {
      speechSynthesis.getVoices()
    }
  })

  // 组件卸载时清理
  onUnmounted(() => {
    stopPreview()
    window.removeEventListener('resize', handleResize)

    if (audioContext.value) {
      audioContext.value.close()
    }
  })

  return {
    // 状态
    isPlaying,
    previewText,
    visualizationContainer,
    voiceSettings,
    voiceTypes,
    languages,

    // 方法
    playPreview,
    stopPreview,
    updateVoicePreview,
    saveSettings,
    resetSettings
  }
}
