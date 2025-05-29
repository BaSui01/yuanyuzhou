<template>
  <div class="pet-assistant">
    <!-- 浮动桌宠 -->
    <div
      v-if="showPet"
      class="pet-container"
      :class="{ 'expanded': expanded, 'dragging': isDragging }"
      :style="petPosition"
      @mousedown="startDrag"
    >
      <!-- 3D模型容器 -->
      <div ref="petModelContainer" class="pet-model-container"></div>

      <!-- 表情气泡 -->
      <div v-if="showEmotionBubble" class="emotion-bubble">
        <i :class="emotionIcon" class="text-2xl" :style="{ color: emotionColor }"></i>
      </div>

      <!-- 思考气泡 -->
      <div v-if="showThoughtBubble" class="thought-bubble">
        <p>{{ currentThought }}</p>
      </div>

      <!-- 控制按钮 -->
      <div class="pet-controls">
        <button class="control-button" @click.stop="toggleChat">
          <i class="pi pi-comments"></i>
        </button>
        <button class="control-button" @click.stop="toggleExpand">
          <i :class="expanded ? 'pi pi-minus' : 'pi pi-plus'"></i>
        </button>
        <button class="control-button" @click.stop="togglePet">
          <i class="pi pi-times"></i>
        </button>
      </div>
    </div>

    <!-- 聊天窗口 -->
    <div v-if="showChat" class="chat-window" :style="chatPosition">
      <div class="chat-header">
        <div class="flex items-center">
          <div class="avatar">
            <img :src="petAvatar" alt="AI助手" />
          </div>
          <h3>{{ petName }}</h3>
        </div>
        <button class="close-button" @click="toggleChat">
          <i class="pi pi-times"></i>
        </button>
      </div>

      <div ref="chatMessages" class="chat-messages">
        <div
          v-for="(msg, index) in chatHistory"
          :key="index"
          class="message"
          :class="msg.sender === 'ai' ? 'ai' : 'user'"
        >
          <div class="message-content">
            <p>{{ msg.text }}</p>
            <span class="timestamp">{{ formatTime(msg.timestamp) }}</span>
          </div>
        </div>

        <div v-if="isTyping" class="message ai">
          <div class="message-content">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>

      <div class="chat-input">
        <input
          v-model="userInput"
          type="text"
          placeholder="输入消息..."
          @keyup.enter="sendMessage"
        />
        <button class="send-button" @click="sendMessage" :disabled="!userInput.trim()">
          <i class="pi pi-send"></i>
        </button>
      </div>
    </div>

    <!-- 浮动按钮 -->
    <div v-if="!showPet" class="pet-toggle" @click="togglePet">
      <i class="pi pi-comments"></i>
    </div>
  </div>
</template>

<script setup>
import Pet from './Pet.js';
</script>

<style lang="scss">
@use './Pet.scss';
</style>
