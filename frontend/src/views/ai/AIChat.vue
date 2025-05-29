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
        <Avatar :icon="message.role === 'user' ? 'pi pi-user' : 'pi pi-android'"
                :style="{ 'background-color': message.role === 'user' ? '#4CAF50' : '#3B82F6', color: '#ffffff' }"
                shape="circle"
                class="message-avatar" />
        <div class="message-content">
          <div class="message-text" v-html="formatMessage(message.content)"></div>
          <div class="message-time">{{ formatTime(message.timestamp) }}</div>
        </div>
      </div>

      <div v-if="loading" class="message ai">
        <Avatar icon="pi pi-android"
                style="background-color: #3B82F6; color: #ffffff;"
                shape="circle"
                class="message-avatar" />
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
      <InputText v-model="userInput" placeholder="输入消息..." class="w-full" @keyup.enter="sendMessage"
        :disabled="loading" />
      <Button icon="pi pi-send" @click="sendMessage" :disabled="loading || !userInput.trim()" />
    </div>

    <Sidebar v-model:visible="showSettings" position="right" class="settings-sidebar">
      <h3>聊天设置</h3>

      <div class="setting-group">
        <label>AI角色</label>
        <Dropdown v-model="settings.aiRole" :options="aiRoles" optionLabel="name" class="w-full"
          @change="applySettings" />
      </div>

      <div class="setting-group">
        <label>回复风格</label>
        <Dropdown v-model="settings.responseStyle" :options="responseStyles" optionLabel="name" class="w-full"
          @change="applySettings" />
      </div>

      <div class="setting-group">
        <label>回复长度</label>
        <Slider v-model="settings.responseLength" :min="1" :max="5" :step="1" class="w-full" @change="applySettings" />
        <div class="slider-labels">
          <span>简短</span>
          <span>详细</span>
        </div>
      </div>

      <div class="setting-group">
        <label>创造力</label>
        <Slider v-model="settings.creativity" :min="0" :max="1" :step="0.1" class="w-full" @change="applySettings" />
        <div class="slider-labels">
          <span>精确</span>
          <span>创意</span>
        </div>
      </div>
    </Sidebar>
  </div>
</template>

<script setup>
import { ai } from '@/modules'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Avatar from 'primevue/avatar'
import Sidebar from 'primevue/sidebar'
import Dropdown from 'primevue/dropdown'
import Slider from 'primevue/slider'

const {
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
  sendMessage,
  resetConversation,
  applySettings,
  formatMessage,
  formatTime
} = ai.useAIChat()
</script>

<style lang="scss">
@use '@styles/view/ai/chat.scss';
</style>
