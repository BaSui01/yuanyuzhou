<template>
  <div class="voice-lab-view p-4 md:p-6">
    <div class="max-w-7xl mx-auto">
      <div class="header mb-6">
        <h1 class="text-2xl md:text-3xl font-bold text-white">语音实验室</h1>
        <p class="text-gray-400 mt-2">探索AI语音合成与识别的魔力</p>
      </div>

      <!-- 功能卡片区域 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- 语音合成 -->
        <div class="tts-section glass rounded-xl p-6">
          <div class="section-header mb-4">
            <h2 class="text-xl font-bold text-white flex items-center">
              <i class="pi pi-volume-up mr-2 text-cyan-400"></i>
              语音合成
            </h2>
            <p class="text-gray-400 text-sm mt-1">将文本转换为自然流畅的语音</p>
          </div>

          <div class="space-y-4">
            <!-- 文本输入 -->
            <div class="form-group">
              <label class="block text-sm font-medium text-gray-300 mb-2">输入文本</label>
              <Textarea
                v-model="ttsText"
                rows="4"
                class="w-full"
                placeholder="请输入要转换为语音的文本..."
              />
            </div>

            <!-- 语音设置 -->
            <div class="form-group">
              <label class="block text-sm font-medium text-gray-300 mb-2">语音选择</label>
              <Dropdown
                v-model="selectedVoice"
                :options="availableVoices"
                option-label="name"
                option-value="id"
                placeholder="选择语音"
                class="w-full"
              />
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div class="form-group">
                <label class="block text-sm font-medium text-gray-300 mb-2">语速</label>
                <Slider v-model="voiceSpeed" :min="0.5" :max="2" :step="0.1" />
                <div class="flex justify-between text-xs text-gray-500 mt-1">
                  <span>慢</span>
                  <span>正常</span>
                  <span>快</span>
                </div>
              </div>

              <div class="form-group">
                <label class="block text-sm font-medium text-gray-300 mb-2">音调</label>
                <Slider v-model="voicePitch" :min="0.5" :max="2" :step="0.1" />
                <div class="flex justify-between text-xs text-gray-500 mt-1">
                  <span>低</span>
                  <span>正常</span>
                  <span>高</span>
                </div>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="flex space-x-2">
              <Button
                label="生成语音"
                icon="pi pi-play"
                @click="generateSpeech"
                :loading="ttsLoading"
                :disabled="!ttsText.trim()"
              />
              <Button
                label="停止"
                icon="pi pi-stop"
                class="p-button-outlined"
                @click="stopSpeech"
                :disabled="!isSpeaking"
              />
              <Button
                label="下载"
                icon="pi pi-download"
                class="p-button-outlined"
                @click="downloadSpeech"
                :disabled="!audioUrl"
              />
            </div>

            <!-- 音频播放器 -->
            <div v-if="audioUrl" class="audio-player mt-4">
              <audio ref="audioPlayer" controls class="w-full" :src="audioUrl"></audio>
            </div>
          </div>
        </div>

        <!-- 语音识别 -->
        <div class="stt-section glass rounded-xl p-6">
          <div class="section-header mb-4">
            <h2 class="text-xl font-bold text-white flex items-center">
              <i class="pi pi-microphone mr-2 text-purple-400"></i>
              语音识别
            </h2>
            <p class="text-gray-400 text-sm mt-1">将您的语音转换为文本</p>
          </div>

          <div class="space-y-4">
            <!-- 录音控制 -->
            <div class="recording-controls flex flex-col items-center justify-center py-6">
              <div
                class="recording-button w-20 h-20 rounded-full flex items-center justify-center cursor-pointer mb-4"
                :class="{ 'bg-red-500/20 pulse-animation': isRecording, 'bg-purple-500/20': !isRecording }"
                @click="toggleRecording"
              >
                <i
                  :class="isRecording ? 'pi pi-stop text-red-400' : 'pi pi-microphone text-purple-400'"
                  class="text-2xl"
                ></i>
              </div>
              <p class="text-sm text-gray-300">
                {{ isRecording ? '点击停止录音' : '点击开始录音' }}
              </p>
              <p v-if="recordingTime > 0" class="text-xs text-gray-400 mt-1">
                已录制 {{ formatTime(recordingTime) }}
              </p>
            </div>

            <!-- 识别结果 -->
            <div class="recognition-result">
              <label class="block text-sm font-medium text-gray-300 mb-2">识别结果</label>
              <div
                class="result-box bg-gray-800/60 border border-gray-700 rounded-lg p-4 min-h-[100px] max-h-[200px] overflow-y-auto"
                :class="{ 'animate-pulse': sttLoading }"
              >
                <p v-if="sttLoading" class="text-gray-400">正在识别中...</p>
                <p v-else-if="recognizedText" class="text-white whitespace-pre-wrap">{{ recognizedText }}</p>
                <p v-else class="text-gray-500 italic">录音后将在这里显示识别结果</p>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="flex space-x-2">
              <Button
                label="复制文本"
                icon="pi pi-copy"
                @click="copyRecognizedText"
                :disabled="!recognizedText"
              />
              <Button
                label="清除"
                icon="pi pi-trash"
                class="p-button-outlined"
                @click="clearRecognition"
                :disabled="!recognizedText && !isRecording"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- 高级功能区域 -->
      <div class="advanced-features mt-8">
        <h2 class="text-xl font-bold text-white mb-4">高级功能</h2>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- 语音克隆 -->
          <div class="feature-card glass rounded-xl p-6">
            <div class="card-icon w-12 h-12 rounded-full bg-pink-500/20 flex items-center justify-center mb-4">
              <i class="pi pi-user-plus text-pink-400"></i>
            </div>
            <h3 class="text-lg font-bold text-white mb-2">语音克隆</h3>
            <p class="text-gray-400 text-sm mb-4">上传您的语音样本，创建个性化的AI声音</p>
            <Button label="即将推出" icon="pi pi-clock" class="p-button-outlined p-button-secondary" disabled />
          </div>

          <!-- 实时翻译 -->
          <div class="feature-card glass rounded-xl p-6">
            <div class="card-icon w-12 h-12 rounded-full bg-amber-500/20 flex items-center justify-center mb-4">
              <i class="pi pi-globe text-amber-400"></i>
            </div>
            <h3 class="text-lg font-bold text-white mb-2">实时翻译</h3>
            <p class="text-gray-400 text-sm mb-4">语音输入实时翻译成多种语言</p>
            <Button label="即将推出" icon="pi pi-clock" class="p-button-outlined p-button-secondary" disabled />
          </div>

          <!-- 情感分析 -->
          <div class="feature-card glass rounded-xl p-6">
            <div class="card-icon w-12 h-12 rounded-full bg-green-500/20 flex items-center justify-center mb-4">
              <i class="pi pi-heart text-green-400"></i>
            </div>
            <h3 class="text-lg font-bold text-white mb-2">情感分析</h3>
            <p class="text-gray-400 text-sm mb-4">分析语音中的情感和语调</p>
            <Button label="即将推出" icon="pi pi-clock" class="p-button-outlined p-button-secondary" disabled />
          </div>
        </div>
      </div>

      <!-- 使用历史 -->
      <div class="usage-history mt-8 glass rounded-xl p-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-bold text-white">使用历史</h2>
          <Button icon="pi pi-refresh" class="p-button-text p-button-rounded" @click="loadUsageHistory" />
        </div>

        <DataTable :value="usageHistory" stripedRows class="p-datatable-sm">
          <Column field="type" header="类型">
            <template #body="{ data }">
              <span class="flex items-center">
                <i :class="data.type === 'tts' ? 'pi pi-volume-up text-cyan-400' : 'pi pi-microphone text-purple-400'" class="mr-2"></i>
                {{ data.type === 'tts' ? '语音合成' : '语音识别' }}
              </span>
            </template>
          </Column>
          <Column field="content" header="内容">
            <template #body="{ data }">
              <span class="truncate block max-w-[200px]">{{ data.content }}</span>
            </template>
          </Column>
          <Column field="date" header="日期">
            <template #body="{ data }">
              {{ formatDate(data.date) }}
            </template>
          </Column>
          <Column header="操作">
            <template #body="{ data }">
              <Button
                icon="pi pi-replay"
                class="p-button-text p-button-rounded p-button-sm"
                @click="replayHistory(data)"
                tooltip="重新使用"
              />
            </template>
          </Column>
        </DataTable>
      </div>
    </div>

    <!-- 桌宠AI助手 -->
    <PetAssistant />
  </div>
</template>

<script>
import VoiceLabViews from '@/server/view/ai/VoiceLabViews'
</script>

<style lang="scss" scoped>
@use '../../styles/view/ai/voice-lab.scss';
</style>
