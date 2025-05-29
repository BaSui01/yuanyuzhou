import axios from '@/api/axios';

/**
 * AI功能相关的API服务
 */
export const aiService = {
  // AI聊天对话
  chat: (data) => {
    return axios.post('/ai/chat', {
      message: data.message,
      model: data.model || 'gpt-3.5',
      history: data.history || [],
      pet_settings: data.petSettings,
      context: data.context,
      temperature: data.temperature || 0.8,
      max_tokens: data.maxTokens || 1000
    });
  },

  // 流式聊天对话
  chatStream: (data) => {
    return axios.post('/ai/chat/stream', {
      message: data.message,
      model: data.model || 'gpt-3.5',
      history: data.history || [],
      pet_settings: data.petSettings,
      context: data.context,
      temperature: data.temperature || 0.8,
      max_tokens: data.maxTokens || 1000
    }, {
      responseType: 'stream'
    });
  },

  // 文本转语音
  textToSpeech: (data) => {
    return axios.post('/ai/tts', {
      text: data.text,
      voice: data.voice || 'zh-CN-XiaoxiaoNeural',
      speed: data.speed || 1.0,
      pitch: data.pitch || 1.0,
      emotion: data.emotion || 'neutral',
      format: data.format || 'mp3'
    });
  },

  // 语音转文本
  speechToText: (audioFile) => {
    const formData = new FormData();
    formData.append('audio', audioFile);

    return axios.post('/ai/stt', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // 获取可用的语音列表
  getVoices: () => {
    return axios.get('/ai/voices');
  },

  // 获取AI模型列表
  getModels: () => {
    return axios.get('/ai/models');
  },

  // AI图像生成
  generateImage: (data) => {
    return axios.post('/ai/image/generate', {
      prompt: data.prompt,
      style: data.style || 'realistic',
      size: data.size || '512x512',
      quality: data.quality || 'standard',
      count: data.count || 1
    });
  },

  // AI图像编辑
  editImage: (imageFile, data) => {
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('prompt', data.prompt);
    formData.append('mask', data.mask);

    return axios.post('/ai/image/edit', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // AI情感分析
  analyzeEmotion: (text) => {
    return axios.post('/ai/emotion/analyze', { text });
  },

  // AI文本摘要
  summarizeText: (text, options = {}) => {
    return axios.post('/ai/text/summarize', {
      text: text,
      length: options.length || 'medium',
      style: options.style || 'bullet_points'
    });
  },

  // AI文本翻译
  translateText: (text, targetLang, sourceLang = 'auto') => {
    return axios.post('/ai/text/translate', {
      text: text,
      target_language: targetLang,
      source_language: sourceLang
    });
  }
};

export default aiService;
