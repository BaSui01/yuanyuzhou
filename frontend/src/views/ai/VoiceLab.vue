<template>
  <div class="voice-lab-container">
    <div class="voice-lab-header">
      <h1>语音实验室</h1>
      <p>定制您的AI助手的声音和语言模式</p>
    </div>

    <div class="voice-lab-content">
      <div class="voice-settings-card">
        <h2>声音设置</h2>

        <div class="setting-group">
          <label>声音类型</label>
          <Dropdown v-model="voiceSettings.voiceType" :options="voiceTypes" optionLabel="name" class="w-full"
            @change="updateVoicePreview" />
        </div>

        <div class="setting-group">
          <label>语言</label>
          <Dropdown v-model="voiceSettings.language" :options="languages" optionLabel="name" class="w-full"
            @change="updateVoicePreview" />
        </div>

        <div class="setting-group">
          <label>语速 ({{ voiceSettings.speed }})</label>
          <Slider v-model="voiceSettings.speed" :min="0.5" :max="2" :step="0.1" class="w-full"
            @change="updateVoicePreview" />
          <div class="slider-labels">
            <span>慢</span>
            <span>快</span>
          </div>
        </div>

        <div class="setting-group">
          <label>音调 ({{ voiceSettings.pitch }})</label>
          <Slider v-model="voiceSettings.pitch" :min="0.5" :max="2" :step="0.1" class="w-full"
            @change="updateVoicePreview" />
          <div class="slider-labels">
            <span>低</span>
            <span>高</span>
          </div>
        </div>
      </div>

      <div class="voice-preview-card">
        <h2>声音预览</h2>

        <div class="preview-text-area">
          <Textarea v-model="previewText" rows="4" class="w-full" placeholder="输入要预览的文本..." />
        </div>

        <div class="preview-controls">
          <Button label="播放预览" icon="pi pi-play" @click="playPreview" :disabled="isPlaying || !previewText.trim()"
            class="mr-2" />
          <Button label="停止" icon="pi pi-stop" @click="stopPreview" :disabled="!isPlaying" class="p-button-secondary" />
        </div>

        <div class="voice-visualization" ref="visualizationContainer">
          <!-- 声音可视化将在这里渲染 -->
        </div>
      </div>
    </div>

    <div class="voice-lab-actions">
      <Button label="保存设置" icon="pi pi-save" @click="saveSettings" class="mr-2" />
      <Button label="重置" icon="pi pi-refresh" @click="resetSettings" class="p-button-secondary" />
    </div>
  </div>
</template>

<script setup>
import { useVoiceLab } from '@/modules/features/ai/composables/useVoiceLab'
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'
import Slider from 'primevue/slider'
import Textarea from 'primevue/textarea'

const {
  isPlaying,
  previewText,
  visualizationContainer,
  voiceSettings,
  voiceTypes,
  languages,
  playPreview,
  stopPreview,
  updateVoicePreview,
  saveSettings,
  resetSettings
} = useVoiceLab()
</script>

<style lang="scss">
@use'@styles/view/ai/voice-lab.scss';
</style>
