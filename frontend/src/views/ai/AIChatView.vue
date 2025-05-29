<template>
  <div class="ai-chat-container">
    <div class="chat-header">
      <h1>AI助手对话</h1>
      <div class="chat-actions">
        <Button icon="pi pi-refresh" class="p-button-rounded p-button-text" @click="resetConversation" />
        <Button icon="pi pi-cog" class="p-button-rounded p-button-text" @click="showSettings = true" />
      </div>
    </div>

    <div class="chat-messages" ref="messagesContainer">
      <div v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
        <Avatar
          :image="message.role === 'user' ? userAvatar : aiAvatar"
          shape="circle"
          class="message-avatar"
        />
        <div class="message-content">
          <div class="message-text" v-html="formatMessage(message.content)"></div>
          <div class="message-time">{{ formatTime(message.timestamp) }}</div>
        </div>
      </div>

      <div v-if="loading" class="message ai">
        <Avatar :image="aiAvatar" shape="circle" class="message-avatar" />
        <div class="message-content">
          <div class="message-typing">
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
          </div>
        </div>
      </div>
    </div>

    <div class="chat-input">
      <InputText
        v-model="userInput"
        placeholder="输入消息..."
        class="w-full"
        @keyup.enter="sendMessage"
        :disabled="loading"
      />
      <Button
        icon="pi pi-send"
        @click="sendMessage"
        :disabled="loading || !userInput.trim()"
      />
    </div>

    <Sidebar v-model:visible="showSettings" position="right" class="settings-sidebar">
      <h3>聊天设置</h3>

      <div class="setting-group">
        <label>AI角色</label>
        <Dropdown
          v-model="settings.aiRole"
          :options="aiRoles"
          optionLabel="name"
          class="w-full"
          @change="applySettings"
        />
      </div>

      <div class="setting-group">
        <label>回复风格</label>
        <Dropdown
          v-model="settings.responseStyle"
          :options="responseStyles"
          optionLabel="name"
          class="w-full"
          @change="applySettings"
        />
      </div>

      <div class="setting-group">
        <label>回复长度</label>
        <Slider
          v-model="settings.responseLength"
          :min="1"
          :max="5"
          :step="1"
          class="w-full"
          @change="applySettings"
        />
        <div class="slider-labels">
          <span>简短</span>
          <span>详细</span>
        </div>
      </div>

      <div class="setting-group">
        <label>创造力</label>
        <Slider
          v-model="settings.creativity"
          :min="0"
          :max="1"
          :step="0.1"
          class="w-full"
          @change="applySettings"
        />
        <div class="slider-labels">
          <span>精确</span>
          <span>创意</span>
        </div>
      </div>
    </Sidebar>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import { useAIStore } from '@/stores/ai';
import DOMPurify from 'dompurify';
import marked from 'marked';

const aiStore = useAIStore();

// 聊天状态
const messages = ref([
  {
    role: 'ai',
    content: '你好！我是你的AI助手。有什么我可以帮助你的吗？',
    timestamp: Date.now()
  }
]);
const userInput = ref('');
const loading = ref(false);
const messagesContainer = ref(null);
const showSettings = ref(false);

// 头像
const userAvatar = ref('/avatars/user.png');
const aiAvatar = ref('/avatars/ai-assistant.png');

// 设置选项
const settings = ref({
  aiRole: { name: '通用助手', value: 'general' },
  responseStyle: { name: '友好', value: 'friendly' },
  responseLength: 3,
  creativity: 0.7
});

const aiRoles = [
  { name: '通用助手', value: 'general' },
  { name: '技术专家', value: 'tech' },
  { name: '创意伙伴', value: 'creative' },
  { name: '生活顾问', value: 'life' }
];

const responseStyles = [
  { name: '友好', value: 'friendly' },
  { name: '专业', value: 'professional' },
  { name: '幽默', value: 'humorous' },
  { name: '简洁', value: 'concise' }
];

// 发送消息
const sendMessage = async () => {
  if (!userInput.value.trim() || loading.value) return;

  const userMessage = {
    role: 'user',
    content: userInput.value,
    timestamp: Date.now()
  };

  messages.value.push(userMessage);
  userInput.value = '';
  loading.value = true;

  scrollToBottom();

  try {
    // 调用AI Store中的方法获取AI回复
    const response = await aiStore.sendMessage({
      message: userMessage.content,
      settings: {
        role: settings.value.aiRole.value,
        style: settings.value.responseStyle.value,
        length: settings.value.responseLength,
        creativity: settings.value.creativity
      }
    });

    messages.value.push({
      role: 'ai',
      content: response.content || '抱歉，我现在无法回答这个问题。',
      timestamp: Date.now()
    });
  } catch (error) {
    console.error('获取AI回复失败:', error);
    messages.value.push({
      role: 'ai',
      content: '抱歉，发生了错误。请稍后再试。',
      timestamp: Date.now()
    });
  } finally {
    loading.value = false;
    scrollToBottom();
  }
};

// 重置对话
const resetConversation = () => {
  messages.value = [
    {
      role: 'ai',
      content: '你好！我是你的AI助手。有什么我可以帮助你的吗？',
      timestamp: Date.now()
    }
  ];
};

// 应用设置
const applySettings = () => {
  // 这里可以添加应用设置的逻辑
  console.log('应用设置:', settings.value);
};

// 格式化消息，支持Markdown
const formatMessage = (content) => {
  const html = marked(content);
  return DOMPurify.sanitize(html);
};

// 格式化时间
const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
};

// 监听消息变化，自动滚动到底部
watch(() => messages.value.length, scrollToBottom);

onMounted(() => {
  scrollToBottom();

  // 加载用户设置
  const savedSettings = aiStore.getSettings();
  if (savedSettings) {
    settings.value = savedSettings;
  }
});
</script>

<style lang="scss">
@import '@/assets/styles/view/ai/chat.scss';
</style>
