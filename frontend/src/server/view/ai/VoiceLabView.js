import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useAIStore } from '@/stores/ai';
import PetAssistant from '@/components/ai/PetAssistant.vue';

const aiStore = useAIStore();

// 语音合成相关
const ttsText = ref('');
const selectedVoice = ref('zh-CN-XiaoxiaoNeural');
const voiceSpeed = ref(1.0);
const voicePitch = ref(1.0);
const audioUrl = ref('');
const ttsLoading = ref(false);
const isSpeaking = ref(false);
const audioPlayer = ref(null);

// 语音识别相关
const isRecording = ref(false);
const recordingTime = ref(0);
const recognizedText = ref('');
const sttLoading = ref(false);
let recordingInterval = null;
let mediaRecorder = null;
let audioChunks = [];

// 可用语音列表
const availableVoices = ref([
  { id: 'zh-CN-XiaoxiaoNeural', name: '晓晓 (女声)' },
  { id: 'zh-CN-YunxiNeural', name: '云希 (男声)' },
  { id: 'zh-CN-YunyangNeural', name: '云扬 (男声)' },
  { id: 'zh-CN-XiaohanNeural', name: '晓涵 (女声)' },
  { id: 'zh-CN-XiaomoNeural', name: '晓墨 (女声)' }
]);

// 使用历史
const usageHistory = ref([
  { id: 1, type: 'tts', content: '欢迎使用语音实验室，这里可以体验AI语音合成与识别功能。', date: new Date(Date.now() - 3600000) },
  { id: 2, type: 'stt', content: '语音识别测试，这段文字是通过语音转换得到的。', date: new Date(Date.now() - 7200000) }
]);

// 生成语音
const generateSpeech = async () => {
  if (!ttsText.value.trim()) return;

  ttsLoading.value = true;
  isSpeaking.value = true;

  try {
    // 调用API生成语音
    const response = await aiStore.textToSpeech({
      text: ttsText.value,
      voice: selectedVoice.value,
      speed: voiceSpeed.value,
      pitch: voicePitch.value
    });

    if (response.success) {
      audioUrl.value = response.data.audioUrl;

      // 播放音频
      if (audioPlayer.value) {
        audioPlayer.value.onended = () => {
          isSpeaking.value = false;
        };
        audioPlayer.value.play();
      }

      // 添加到使用历史
      addToHistory('tts', ttsText.value);
    } else {
      console.error('生成语音失败:', response.message);
    }
  } catch (error) {
    console.error('生成语音出错:', error);
  } finally {
    ttsLoading.value = false;
  }
};

// 停止语音播放
const stopSpeech = () => {
  if (audioPlayer.value) {
    audioPlayer.value.pause();
    audioPlayer.value.currentTime = 0;
  }
  isSpeaking.value = false;
};

// 下载语音文件
const downloadSpeech = () => {
  if (!audioUrl.value) return;

  const link = document.createElement('a');
  link.href = audioUrl.value;
  link.download = `tts-${Date.now()}.mp3`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

// 切换录音状态
const toggleRecording = async () => {
  if (isRecording.value) {
    stopRecording();
  } else {
    startRecording();
  }
};

// 开始录音
const startRecording = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
      // 处理录音数据
      sttLoading.value = true;

      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });

      try {
        // 调用API进行语音识别
        const response = await aiStore.speechToText({
          audio: audioBlob
        });

        if (response.success) {
          recognizedText.value = response.data.text;

          // 添加到使用历史
          if (recognizedText.value) {
            addToHistory('stt', recognizedText.value);
          }
        } else {
          console.error('语音识别失败:', response.message);
        }
      } catch (error) {
        console.error('语音识别出错:', error);
      } finally {
        sttLoading.value = false;
      }
    };

    // 开始录音
    mediaRecorder.start();
    isRecording.value = true;
    recordingTime.value = 0;

    // 开始计时
    recordingInterval = setInterval(() => {
      recordingTime.value += 1;
    }, 1000);

  } catch (error) {
    console.error('无法访问麦克风:', error);
  }
};

// 停止录音
const stopRecording = () => {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop();

    // 停止所有音轨
    mediaRecorder.stream.getTracks().forEach(track => track.stop());
  }

  isRecording.value = false;

  // 清除计时器
  if (recordingInterval) {
    clearInterval(recordingInterval);
    recordingInterval = null;
  }
};

// 复制识别文本
const copyRecognizedText = async () => {
  if (!recognizedText.value) return;

  try {
    await navigator.clipboard.writeText(recognizedText.value);
    // 显示复制成功提示
    window.app.addNotification({
      type: 'success',
      title: '复制成功',
      message: '文本已复制到剪贴板',
      duration: 2000
    });
  } catch (error) {
    console.error('复制失败:', error);
  }
};

// 清除识别结果
const clearRecognition = () => {
  recognizedText.value = '';

  if (isRecording.value) {
    stopRecording();
  }
};

// 加载使用历史
const loadUsageHistory = async () => {
  try {
    // 实际项目中应该从API加载历史数据
    console.log('加载使用历史');
  } catch (error) {
    console.error('加载使用历史失败:', error);
  }
};

// 重新使用历史记录
const replayHistory = (item) => {
  if (item.type === 'tts') {
    ttsText.value = item.content;
    generateSpeech();
  } else {
    recognizedText.value = item.content;
  }
};

// 添加到使用历史
const addToHistory = (type, content) => {
  usageHistory.value.unshift({
    id: Date.now(),
    type,
    content,
    date: new Date()
  });

  // 限制历史记录数量
  if (usageHistory.value.length > 10) {
    usageHistory.value = usageHistory.value.slice(0, 10);
  }
};

// 格式化时间
const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
};

// 格式化日期
const formatDate = (date) => {
  return new Date(date).toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// 生命周期钩子
onMounted(() => {
  // 初始化
});

onBeforeUnmount(() => {
  // 清理资源
  if (isRecording.value) {
    stopRecording();
  }

  if (isSpeaking.value) {
    stopSpeech();
  }
});
