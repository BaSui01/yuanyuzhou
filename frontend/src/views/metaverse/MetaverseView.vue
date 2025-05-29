<template>
  <div class="metaverse-container">
    <div class="metaverse-canvas" ref="canvasContainer"></div>

    <div class="metaverse-ui">
      <div class="controls-panel">
        <Button icon="pi pi-home" @click="goToDashboard" class="p-button-rounded p-button-secondary" />
        <Button icon="pi pi-cog" @click="showSettings = true" class="p-button-rounded p-button-secondary" />
        <Button icon="pi pi-comments" @click="showChat = true" class="p-button-rounded p-button-secondary" />
      </div>

      <Sidebar v-model:visible="showSettings" position="right" class="settings-sidebar">
        <h3>空间设置</h3>
        <div class="setting-group">
          <label>环境主题</label>
          <Dropdown v-model="settings.theme" :options="themeOptions" optionLabel="name" class="w-full" />
        </div>

        <div class="setting-group">
          <label>光照强度</label>
          <Slider v-model="settings.lightIntensity" :min="0" :max="2" :step="0.1" class="w-full" />
        </div>

        <div class="setting-group">
          <label>粒子数量</label>
          <Slider v-model="settings.particleCount" :min="100" :max="10000" :step="100" class="w-full" />
        </div>

        <div class="setting-group">
          <Button label="应用设置" class="w-full" @click="applySettings" />
        </div>
      </Sidebar>

      <Sidebar v-model:visible="showChat" position="right" class="chat-sidebar">
        <h3>社交聊天</h3>
        <div class="chat-messages" ref="chatMessages">
          <div v-for="(msg, index) in chatMessages" :key="index" :class="['chat-message', msg.sender === 'me' ? 'my-message' : 'other-message']">
            <div class="message-avatar">
              <Avatar :image="msg.avatar" shape="circle" />
            </div>
            <div class="message-content">
              <div class="message-sender">{{ msg.senderName }}</div>
              <div class="message-text">{{ msg.text }}</div>
              <div class="message-time">{{ msg.time }}</div>
            </div>
          </div>
        </div>

        <div class="chat-input">
          <InputText v-model="newMessage" placeholder="输入消息..." class="w-full" @keyup.enter="sendMessage" />
          <Button icon="pi pi-send" @click="sendMessage" />
        </div>
      </Sidebar>
    </div>
  </div>
</template>

<script>
import MetaverseViews from '@/server/view/metaverse/MetaverseViews'
</script>

<style lang="scss">
@use'@styles/view/metaverse.scss';
</style>
