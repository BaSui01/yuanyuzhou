<template>
  <div class="ai-companion-view p-4 md:p-6">
    <div class="max-w-7xl mx-auto">
      <div class="header mb-6">
        <h1 class="text-2xl md:text-3xl font-bold text-white">AI伴侣</h1>
        <p class="text-gray-400 mt-2">与您的专属AI桌宠助手互动</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- 左侧：桌宠信息 -->
        <div class="pet-info-section glass rounded-xl p-6 col-span-1">
          <div class="pet-profile text-center mb-6">
            <div class="pet-avatar relative mx-auto mb-4">
              <div class="w-32 h-32 rounded-full bg-gradient-to-r from-cyan-500 to-purple-500 mx-auto flex items-center justify-center">
                <img :src="petAvatar" alt="AI伴侣" class="w-28 h-28 rounded-full object-cover" />
              </div>
              <div class="status-badge absolute bottom-0 right-0 w-6 h-6 rounded-full bg-green-500 border-2 border-gray-800"></div>
            </div>

            <h2 class="text-xl font-bold text-white">{{ petName }}</h2>
            <p class="text-gray-400 text-sm">{{ petPersonalityDesc }}</p>
          </div>

          <div class="pet-stats space-y-4">
            <div class="stat-item">
              <div class="flex justify-between mb-1">
                <span class="text-sm text-gray-300">等级</span>
                <span class="text-sm text-cyan-400">{{ petLevel }}</span>
              </div>
              <div class="h-2 bg-gray-700 rounded-full overflow-hidden">
                <div class="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full" :style="{ width: `${petExpPercentage}%` }"></div>
              </div>
            </div>

            <div class="stat-item">
              <div class="flex justify-between mb-1">
                <span class="text-sm text-gray-300">心情</span>
                <span class="text-sm" :class="moodColor">{{ petMood }}</span>
              </div>
              <div class="h-2 bg-gray-700 rounded-full overflow-hidden">
                <div class="h-full rounded-full" :class="moodBarColor" :style="{ width: `${moodPercentage}%` }"></div>
              </div>
            </div>

            <div class="stat-item">
              <div class="flex justify-between mb-1">
                <span class="text-sm text-gray-300">能量</span>
                <span class="text-sm" :class="energyColor">{{ petEnergy }}%</span>
              </div>
              <div class="h-2 bg-gray-700 rounded-full overflow-hidden">
                <div class="h-full rounded-full" :class="energyBarColor" :style="{ width: `${petEnergy}%` }"></div>
              </div>
            </div>

            <div class="stat-item">
              <div class="flex justify-between mb-1">
                <span class="text-sm text-gray-300">亲密度</span>
                <span class="text-sm text-pink-400">{{ intimacyLevel }}</span>
              </div>
              <div class="h-2 bg-gray-700 rounded-full overflow-hidden">
                <div class="h-full bg-gradient-to-r from-pink-500 to-purple-500 rounded-full" :style="{ width: `${intimacyPercentage}%` }"></div>
              </div>
            </div>
          </div>

          <div class="pet-actions mt-6">
            <h3 class="text-lg font-semibold text-white mb-3">互动</h3>
            <div class="grid grid-cols-2 gap-2">
              <Button label="喂食" icon="pi pi-heart" class="p-button-outlined" @click="feedPet" />
              <Button label="抚摸" icon="pi pi-thumbs-up" class="p-button-outlined" @click="petPet" />
              <Button label="玩耍" icon="pi pi-star" class="p-button-outlined" @click="playWithPet" />
              <Button label="休息" icon="pi pi-moon" class="p-button-outlined" @click="restPet" />
            </div>
          </div>
        </div>

        <!-- 中间：互动区域 -->
        <div class="pet-interaction glass rounded-xl p-6 col-span-1 md:col-span-2">
          <div class="interaction-container h-[500px] flex flex-col">
            <div class="interaction-area flex-1 flex items-center justify-center relative">
              <!-- 3D模型容器 -->
              <div ref="modelContainer" class="model-container w-full h-full"></div>

              <!-- 表情气泡 -->
              <div v-if="showEmotionBubble" class="emotion-bubble absolute top-4 right-4 bg-white/10 backdrop-blur-md p-3 rounded-full">
                <i :class="emotionIcon" class="text-2xl" :style="{ color: emotionColor }"></i>
              </div>

              <!-- 思考气泡 -->
              <div v-if="showThoughtBubble" class="thought-bubble absolute top-4 left-4 bg-white/10 backdrop-blur-md p-4 rounded-xl max-w-[200px]">
                <p class="text-sm text-white">{{ currentThought }}</p>
              </div>
            </div>

            <div class="interaction-controls mt-4 bg-gray-800/50 rounded-lg p-4">
              <div class="flex items-center space-x-2">
                <InputText v-model="userPrompt" placeholder="与AI伴侣对话..." class="flex-1" @keyup.enter="sendPrompt" />
                <Button icon="pi pi-send" @click="sendPrompt" :disabled="!userPrompt.trim()" />
              </div>

              <div v-if="quickPrompts.length > 0" class="quick-prompts mt-3 flex flex-wrap gap-2">
                <Button
                  v-for="prompt in quickPrompts"
                  :key="prompt"
                  :label="prompt"
                  class="p-button-text p-button-sm text-xs"
                  @click="selectQuickPrompt(prompt)"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部：自定义和设置 -->
      <div class="customization-section glass rounded-xl p-6 mt-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-bold text-white">个性化设置</h2>
          <Button icon="pi pi-save" label="保存设置" @click="saveSettings" />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- 外观设置 -->
          <div class="appearance-settings">
            <h3 class="text-lg font-semibold text-white mb-3">外观</h3>

            <div class="form-group mb-4">
              <label class="block text-sm font-medium text-gray-300 mb-2">模型</label>
              <Dropdown
                v-model="selectedModel"
                :options="availableModels"
                option-label="name"
                option-value="id"
                placeholder="选择模型"
                class="w-full"
              />
            </div>

            <div class="form-group">
              <label class="block text-sm font-medium text-gray-300 mb-2">颜色</label>
              <div class="color-picker flex space-x-2">
                <div
                  v-for="color in colorOptions"
                  :key="color"
                  class="w-8 h-8 rounded-full cursor-pointer border-2 transition-all duration-200"
                  :class="{ 'border-white': selectedColor === color, 'border-transparent': selectedColor !== color }"
                  :style="{ backgroundColor: color }"
                  @click="selectedColor = color"
                ></div>
              </div>
            </div>
          </div>

          <!-- 性格设置 -->
          <div class="personality-settings">
            <h3 class="text-lg font-semibold text-white mb-3">性格</h3>

            <div class="form-group mb-4">
              <label class="block text-sm font-medium text-gray-300 mb-2">性格类型</label>
              <Dropdown
                v-model="selectedPersonality"
                :options="personalityOptions"
                option-label="label"
                option-value="value"
                placeholder="选择性格"
                class="w-full"
              />
            </div>

            <div class="form-group">
              <label class="block text-sm font-medium text-gray-300 mb-2">名称</label>
              <InputText v-model="customPetName" placeholder="给AI伴侣起个名字" class="w-full" />
            </div>
          </div>

          <!-- 语音设置 -->
          <div class="voice-settings">
            <h3 class="text-lg font-semibold text-white mb-3">语音</h3>

            <div class="form-group mb-4">
              <div class="flex items-center justify-between">
                <label class="text-sm font-medium text-gray-300">启用语音</label>
                <InputSwitch v-model="voiceEnabled" />
              </div>
            </div>

            <div class="form-group mb-4">
              <label class="block text-sm font-medium text-gray-300 mb-2">语音类型</label>
              <Dropdown
                v-model="selectedVoice"
                :options="availableVoices"
                option-label="name"
                option-value="id"
                placeholder="选择语音"
                class="w-full"
                :disabled="!voiceEnabled"
              />
            </div>

            <div class="form-group">
              <label class="block text-sm font-medium text-gray-300 mb-2">语速</label>
              <Slider v-model="voiceSpeed" :min="0.5" :max="2" :step="0.1" :disabled="!voiceEnabled" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AICompanionViews from '@/server/view/ai/AICompanionViews'
</script>

<style lang="scss" scoped>
@use '../../styles/view/ai/companion.scss';
</style>
