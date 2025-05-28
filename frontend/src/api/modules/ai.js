import axios from '../axios';

/**
 * AI相关API
 */
export const aiAPI = {
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

  // 创建AI宠物
  createPet: (petData) => {
    return axios.post('/ai/pet', {
      name: petData.name,
      personality: petData.personality,
      appearance: petData.appearance,
      voice_settings: petData.voiceSettings,
      description: petData.description
    });
  },

  // 更新AI宠物信息
  updatePet: (petId, petData) => {
    return axios.put(`/ai/pet/${petId}`, {
      name: petData.name,
      personality: petData.personality,
      appearance: petData.appearance,
      voice_settings: petData.voiceSettings,
      description: petData.description,
      mood: petData.mood,
      energy: petData.energy,
      intimacy: petData.intimacy
    });
  },

  // 获取AI宠物信息
  getPet: (petId) => {
    return axios.get(`/ai/pet/${petId}`);
  },

  // 获取用户的所有AI宠物
  getUserPets: () => {
    return axios.get('/ai/pets');
  },

  // 删除AI宠物
  deletePet: (petId) => {
    return axios.delete(`/ai/pet/${petId}`);
  },

  // 训练AI宠物
  trainPet: (petId, trainingData) => {
    return axios.post(`/ai/pet/${petId}/train`, {
      training_text: trainingData.trainingText,
      personality_traits: trainingData.personalityTraits,
      knowledge_base: trainingData.knowledgeBase
    });
  },

  // 获取聊天历史
  getChatHistory: (petId, params = {}) => {
    return axios.get(`/ai/pet/${petId}/chat-history`, {
      params: {
        page: params.page || 1,
        per_page: params.perPage || 20,
        start_date: params.startDate,
        end_date: params.endDate
      }
    });
  },

  // 清空聊天历史
  clearChatHistory: (petId) => {
    return axios.delete(`/ai/pet/${petId}/chat-history`);
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
  },

  // AI代码生成
  generateCode: (data) => {
    return axios.post('/ai/code/generate', {
      description: data.description,
      language: data.language,
      framework: data.framework,
      style: data.style || 'clean'
    });
  },

  // AI代码解释
  explainCode: (code, language) => {
    return axios.post('/ai/code/explain', {
      code: code,
      language: language
    });
  },

  // 获取AI使用统计
  getUsageStats: (period = '30d') => {
    return axios.get('/ai/stats', {
      params: { period }
    });
  },

  // 获取AI配置
  getAIConfig: () => {
    return axios.get('/ai/config');
  },

  // 更新AI配置
  updateAIConfig: (config) => {
    return axios.put('/ai/config', config);
  },

  // AI学习反馈
  provideFeedback: (chatId, feedback) => {
    return axios.post(`/ai/feedback/${chatId}`, {
      rating: feedback.rating,
      comment: feedback.comment,
      helpful: feedback.helpful,
      tags: feedback.tags
    });
  },

  // 获取推荐的提示词
  getPromptSuggestions: (category) => {
    return axios.get('/ai/prompts/suggestions', {
      params: { category }
    });
  },

  // 保存自定义提示词
  saveCustomPrompt: (prompt) => {
    return axios.post('/ai/prompts/custom', {
      title: prompt.title,
      content: prompt.content,
      category: prompt.category,
      tags: prompt.tags,
      is_public: prompt.isPublic || false
    });
  },

  // 获取用户的自定义提示词
  getCustomPrompts: () => {
    return axios.get('/ai/prompts/custom');
  },

  // AI角色扮演
  rolePlay: (data) => {
    return axios.post('/ai/roleplay', {
      character: data.character,
      scenario: data.scenario,
      message: data.message,
      context: data.context
    });
  },

  // 获取可用的AI角色
  getCharacters: () => {
    return axios.get('/ai/characters');
  },

  // 创建自定义AI角色
  createCharacter: (character) => {
    return axios.post('/ai/characters', {
      name: character.name,
      description: character.description,
      personality: character.personality,
      background: character.background,
      avatar: character.avatar,
      voice_settings: character.voiceSettings
    });
  }
};
