<template>
  <div class="ai-companion-container">
    <div class="companion-header">
      <h1>我的AI伙伴</h1>
      <p>定制您的AI伙伴的外观、性格和行为</p>
    </div>

    <div class="companion-content">
      <div class="companion-preview">
        <div class="preview-canvas" ref="canvasContainer"></div>
        <div class="preview-controls">
          <Button icon="pi pi-sync" @click="rotateModel" class="p-button-rounded p-button-text" />
          <Button icon="pi pi-search-plus" @click="zoomIn" class="p-button-rounded p-button-text" />
          <Button icon="pi pi-search-minus" @click="zoomOut" class="p-button-rounded p-button-text" />
        </div>
      </div>

      <div class="companion-settings">
        <TabView>
          <TabPanel header="外观">
            <div class="setting-group">
              <label>角色模型</label>
              <div class="model-selection">
                <div v-for="model in modelOptions" :key="model.value"
                  :class="['model-option', { active: companionSettings.model === model.value }]"
                  @click="selectModel(model.value)">
                  <img :src="model.thumbnail" :alt="model.name" />
                  <span>{{ model.name }}</span>
                </div>
              </div>
            </div>

            <div class="setting-group">
              <label>颜色主题</label>
              <div class="color-selection">
                <div v-for="(color, index) in colorOptions" :key="index"
                  :class="['color-option', { active: companionSettings.color === color.value }]"
                  :style="{ backgroundColor: color.hex }" @click="selectColor(color.value)"></div>
              </div>
            </div>

            <div class="setting-group">
              <label>附件</label>
              <div class="accessory-selection">
                <div v-for="accessory in accessoryOptions" :key="accessory.value"
                  :class="['accessory-option', { active: companionSettings.accessories.includes(accessory.value) }]"
                  @click="toggleAccessory(accessory.value)">
                  <img :src="accessory.thumbnail" :alt="accessory.name" />
                  <span>{{ accessory.name }}</span>
                </div>
              </div>
            </div>
          </TabPanel>

          <TabPanel header="性格">
            <div class="setting-group">
              <label>性格类型</label>
              <Dropdown v-model="companionSettings.personality.type" :options="personalityTypes" optionLabel="name"
                class="w-full" @change="updateCompanion" />
            </div>

            <div class="setting-group">
              <label>友好度 ({{ companionSettings.personality.friendliness }})</label>
              <Slider v-model="companionSettings.personality.friendliness" :min="1" :max="10" :step="1" class="w-full"
                @change="updateCompanion" />
              <div class="slider-labels">
                <span>冷淡</span>
                <span>热情</span>
              </div>
            </div>

            <div class="setting-group">
              <label>活跃度 ({{ companionSettings.personality.energy }})</label>
              <Slider v-model="companionSettings.personality.energy" :min="1" :max="10" :step="1" class="w-full"
                @change="updateCompanion" />
              <div class="slider-labels">
                <span>安静</span>
                <span>活泼</span>
              </div>
            </div>

            <div class="setting-group">
              <label>幽默感 ({{ companionSettings.personality.humor }})</label>
              <Slider v-model="companionSettings.personality.humor" :min="1" :max="10" :step="1" class="w-full"
                @change="updateCompanion" />
              <div class="slider-labels">
                <span>严肃</span>
                <span>诙谐</span>
              </div>
            </div>
          </TabPanel>

          <TabPanel header="行为">
            <div class="setting-group">
              <label>互动频率</label>
              <Dropdown v-model="companionSettings.behavior.interactionFrequency" :options="interactionFrequencies"
                optionLabel="name" class="w-full" @change="updateCompanion" />
            </div>

            <div class="setting-group">
              <label>互动方式</label>
              <div class="interaction-modes">
                <div v-for="mode in interactionModes" :key="mode.value"
                  :class="['interaction-mode', { active: companionSettings.behavior.interactionModes.includes(mode.value) }]"
                  @click="toggleInteractionMode(mode.value)">
                  <i :class="mode.icon"></i>
                  <span>{{ mode.name }}</span>
                </div>
              </div>
            </div>

            <div class="setting-group">
              <label>提醒功能</label>
              <div class="reminder-options">
                <div class="p-field-checkbox">
                  <Checkbox v-model="companionSettings.behavior.reminders.schedule" :binary="true" id="schedule" />
                  <label for="schedule" class="ml-2">日程提醒</label>
                </div>
                <div class="p-field-checkbox">
                  <Checkbox v-model="companionSettings.behavior.reminders.health" :binary="true" id="health" />
                  <label for="health" class="ml-2">健康提醒</label>
                </div>
                <div class="p-field-checkbox">
                  <Checkbox v-model="companionSettings.behavior.reminders.tasks" :binary="true" id="tasks" />
                  <label for="tasks" class="ml-2">任务提醒</label>
                </div>
              </div>
            </div>
          </TabPanel>

          <TabPanel header="名称">
            <div class="setting-group">
              <label>AI伙伴名称</label>
              <InputText v-model="companionSettings.name" class="w-full" placeholder="给您的AI伙伴起个名字..." />
            </div>

            <div class="setting-group">
              <label>您的昵称</label>
              <InputText v-model="companionSettings.userNickname" class="w-full" placeholder="AI伙伴如何称呼您..." />
            </div>

            <div class="setting-group">
              <label>关系类型</label>
              <Dropdown v-model="companionSettings.relationship" :options="relationshipTypes" optionLabel="name"
                class="w-full" />
            </div>
          </TabPanel>
        </TabView>

        <div class="companion-actions">
          <Button label="保存设置" icon="pi pi-save" @click="saveSettings" class="mr-2" />
          <Button label="重置" icon="pi pi-refresh" @click="resetSettings" class="p-button-secondary" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onUnmounted } from 'vue'
import { useAICompanion } from '@/modules/features/ai/composables/useAICompanion'
import Button from 'primevue/button'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import Dropdown from 'primevue/dropdown'
import Slider from 'primevue/slider'
import Checkbox from 'primevue/checkbox'
import InputText from 'primevue/inputtext'

const {
  canvasContainer,
  loading,
  companionSettings,
  modelOptions,
  colorOptions,
  accessoryOptions,
  personalityTypes,
  interactionFrequencies,
  interactionModes,
  relationshipTypes,
  rotateModel,
  zoomIn,
  zoomOut,
  selectModel,
  selectColor,
  toggleAccessory,
  toggleInteractionMode,
  updateCompanion,
  saveSettings,
  resetSettings,
  cleanup
} = useAICompanion()

onUnmounted(() => {
  cleanup()
})
</script>

<style lang="scss">
@use'@styles/view/ai/companion.scss';
</style>
