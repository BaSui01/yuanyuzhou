<template>
  <div class="ai-chat-view p-4 md:p-6">
    <div class="max-w-7xl mx-auto">
      <!-- 聊天界面 -->
      <div class="chat-container flex flex-col lg:flex-row gap-6">
        <!-- 聊天主界面 -->
        <div class="chat-main flex-1 glass rounded-xl overflow-hidden flex flex-col h-[calc(100vh-160px)]">
          <!-- 聊天头部 -->
          <div class="chat-header p-4 border-b border-white/10 flex justify-between items-center">
            <div class="flex items-center space-x-3">
              <Avatar :image="petAvatar" class="h-10 w-10" />
              <div>
                <h2 class="text-lg font-bold text-white">{{ petName }}</h2>
                <div class="flex items-center text-xs text-cyan-400">
                  <span v-if="isTyping" class="flex items-center">
                    <i class="pi pi-spin pi-spinner mr-1"></i>
                    正在输入...
                  </span>
                  <span v-else-if="isSpeaking" class="flex items-center">
                    <i class="pi pi-volume-up mr-1"></i>
                    正在说话...
                  </span>
                  <span v-else class="flex items-center">
                    <i class="pi pi-check-circle mr-1"></i>
                    在线
                  </span>
                </div>
              </div>
            </div>

            <div class="flex items-center space-x-2">
              <Button
                :icon="voiceEnabled ? 'pi pi-volume-up' : 'pi pi-volume-off'"
                class="p-button-text p-button-rounded p-button-sm"
                :class="{ 'text-cyan-400': voiceEnabled }"
                @click="toggleVoice"
                tooltip="语音朗读"
              />
              <Button
                icon="pi pi-trash"
                class="p-button-text p-button-rounded p-button-sm"
                @click="confirmClearChat"
                tooltip="清空对话"
              />
              <Button
                icon="pi pi-cog"
                class="p-button-text p-button-rounded p-button-sm"
                @click="showSettings = true"
                tooltip="设置"
              />
            </div>
          </div>

          <!-- 聊天消息区域 -->
          <div ref="messagesContainer" class="chat-messages flex-1 p-4 overflow-y-auto">
            <div v-if="chatHistory.length === 0" class="h-full flex flex-col items-center justify-center text-center">
              <div class="w-20 h-20 rounded-full bg-cyan-500/20 flex items-center justify-center mb-4">
                <i class="pi pi-comments text-2xl text-cyan-400"></i>
              </div>
              <h3 class="text-xl font-bold text-white mb-2">开始与AI助手对话</h3>
              <p class="text-gray-400 max-w-md">您可以询问任何问题，AI助手将尽力为您解答</p>
            </div>

            <div v-else class="space-y-6">
              <div
                v-for="message in chatHistory"
                :key="message.id"
                class="message"
                :class="{ 'user-message': message.type === 'user', 'ai-message': message.type === 'ai' }"
              >
                <div class="flex items-start gap-3" :class="{ 'flex-row-reverse': message.type === 'user' }">
                  <Avatar
                    :image="message.type === 'user' ? userAvatar : petAvatar"
                    class="h-8 w-8 mt-1"
                  />

                  <div
                    class="message-bubble p-4 rounded-lg max-w-[80%]"
                    :class="{
                      'bg-cyan-600/30 text-white': message.type === 'user',
                      'bg-gray-800/60 text-white': message.type === 'ai'
                    }"
                  >
                    <div class="message-content">
                      <p class="whitespace-pre-wrap">{{ message.content }}</p>

                      <div class="message-footer flex items-center justify-between mt-2 text-xs text-gray-400">
                        <span>{{ formatTime(message.timestamp) }}</span>

                        <div v-if="message.type === 'ai'" class="flex items-center space-x-2">
                          <Button
                            icon="pi pi-volume-up"
                            class="p-button-text p-button-rounded p-button-sm p-0 w-6 h-6"
                            @click="speakMessage(message.content)"
                          />
                          <Button
                            icon="pi pi-copy"
                            class="p-button-text p-button-rounded p-button-sm p-0 w-6 h-6"
                            @click="copyToClipboard(message.content)"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- AI正在输入指示器 -->
              <div v-if="isTyping" class="message ai-message">
                <div class="flex items-start gap-3">
                  <Avatar :image="petAvatar" class="h-8 w-8 mt-1" />

                  <div class="message-bubble p-4 rounded-lg max-w-[80%] bg-gray-800/60">
                    <div class="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 输入区域 -->
          <div class="chat-input p-4 border-t border-white/10">
            <div class="flex items-end gap-2">
              <div class="flex-1 relative">
                <textarea
                  v-model="currentMessage"
                  class="w-full rounded-lg bg-gray-800/60 border border-white/10 text-white p-3 pr-10 resize-none"
                  placeholder="输入消息..."
                  rows="2"
                  @keydown.enter.prevent="handleEnterKey"
                  :disabled="isTyping"
                ></textarea>

                <Button
                  v-if="currentMessage.trim()"
                  icon="pi pi-times"
                  class="absolute right-2 top-2 p-button-text p-button-rounded p-button-sm"
                  @click="currentMessage = ''"
                />
              </div>

              <div class="flex items-center gap-2">
                <Button
                  :icon="isRecording ? 'pi pi-stop' : 'pi pi-microphone'"
                  :class="{ 'p-button-danger': isRecording }"
                  class="p-button-rounded"
                  @click="toggleRecording"
                  tooltip="语音输入"
                />

                <Button
                  icon="pi pi-send"
                  class="p-button-rounded"
                  :disabled="!currentMessage.trim() || isTyping"
                  @click="sendMessage"
                />
              </div>
            </div>

            <!-- 快捷回复 -->
            <div v-if="quickReplies.length > 0" class="quick-replies mt-3 flex flex-wrap gap-2">
              <Button
                v-for="reply in quickReplies"
                :key="reply"
                :label="reply"
                class="p-button-text p-button-sm"
                @click="useQuickReply(reply)"
              />
            </div>
          </div>
        </div>

        <!-- 侧边栏 -->
        <div class="chat-sidebar w-full lg:w-80 glass rounded-xl overflow-hidden flex flex-col">
          <!-- AI模型选择 -->
          <div class="p-4 border-b border-white/10">
            <h3 class="text-lg font-bold text-white mb-3">AI模型</h3>
            <div class="space-y-2">
              <div
                v-for="model in aiModels"
                :key="model.id"
                class="model-option p-3 rounded-lg cursor-pointer transition-colors"
                :class="{ 'bg-cyan-600/30 border-cyan-500': selectedModel === model.id, 'bg-gray-800/60 border-transparent': selectedModel !== model.id }"
                @click="switchModel(model.id)"
              >
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <div class="w-2 h-2 rounded-full mr-2" :class="{ 'bg-cyan-400': selectedModel === model.id, 'bg-gray-500': selectedModel !== model.id }"></div>
                    <span class="font-medium text-white">{{ model.name }}</span>
                  </div>
                  <span v-if="selectedModel === model.id" class="text-xs text-cyan-400">已选择</span>
                </div>
                <p class="text-xs text-gray-400 mt-1">{{ model.description }}</p>
              </div>
            </div>
          </div>

          <!-- 对话历史 -->
          <div class="flex-1 p-4 overflow-y-auto">
            <div class="flex justify-between items-center mb-3">
              <h3 class="text-lg font-bold text-white">对话历史</h3>
              <Button icon="pi pi-plus" class="p-button-text p-button-rounded p-button-sm" tooltip="新建对话" @click="startNewChat" />
            </div>

            <div class="space-y-2">
              <div
                v-for="(chat, index) in chatSessions"
                :key="chat.id"
                class="chat-session p-3 rounded-lg cursor-pointer transition-colors"
                :class="{ 'bg-cyan-600/30': index === 0, 'bg-gray-800/60 hover:bg-gray-700/60': index !== 0 }"
                @click="loadChatSession(chat.id)"
              >
                <div class="flex items-center justify-between">
                  <span class="font-medium text-white truncate">{{ chat.title }}</span>
                  <span class="text-xs text-gray-400">{{ formatDate(chat.date) }}</span>
                </div>
                <p class="text-xs text-gray-400 mt-1 truncate">{{ chat.preview }}</p>
              </div>
            </div>
          </div>

          <!-- 提示词库 -->
          <div class="p-4 border-t border-white/10">
            <div class="flex justify-between items-center mb-3">
              <h3 class="text-lg font-bold text-white">提示词库</h3>
              <Button icon="pi pi-list" class="p-button-text p-button-rounded p-button-sm" tooltip="查看全部" />
            </div>

            <div class="space-y-2">
              <div
                v-for="prompt in promptSuggestions"
                :key="prompt.id"
                class="prompt p-3 rounded-lg bg-gray-800/60 hover:bg-gray-700/60 cursor-pointer transition-colors"
                @click="usePrompt(prompt.content)"
              >
                <div class="font-medium text-white">{{ prompt.title }}</div>
                <p class="text-xs text-gray-400 mt-1 truncate">{{ prompt.content }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 设置对话框 -->
    <Dialog v-model:visible="showSettings" header="AI助手设置" :style="{width: '90%', maxWidth: '500px'}" modal>
      <div class="space-y-6">
        <!-- 语音设置 -->
        <div class="voice-settings">
          <h3 class="text-lg font-bold text-white mb-3">语音设置</h3>

          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <label for="voiceEnabled" class="text-gray-300">启用语音朗读</label>
              <Checkbox v-model="voiceEnabled" :binary="true" inputId="voiceEnabled" />
            </div>

            <div>
              <label class="block text-gray-300 mb-2">语音音量</label>
              <Slider v-model="voiceVolume" :min="0" :max="100" class="w-full" />
              <div class="flex justify-between text-xs text-gray-500 mt-1">
                <span>0</span>
                <span>50</span>
                <span>100</span>
              </div>
            </div>

            <div>
              <label class="block text-gray-300 mb-2">语音速度</label>
              <Slider v-model="voiceSpeed" :min="0.5" :max="2" :step="0.1" class="w-full" />
              <div class="flex justify-between text-xs text-gray-500 mt-1">
                <span>慢</span>
                <span>正常</span>
                <span>快</span>
              </div>
            </div>

            <div>
              <label class="block text-gray-300 mb-2">语音选择</label>
              <Dropdown
                v-model="selectedVoice"
                :options="availableVoices"
                option-label="name"
                option-value="id"
                placeholder="选择语音"
                class="w-full"
              />
            </div>
          </div>
        </div>

        <!-- AI设置 -->
        <div class="ai-settings">
          <h3 class="text-lg font-bold text-white mb-3">AI设置</h3>

          <div class="space-y-4">
            <div>
              <label class="block text-gray-300 mb-2">回复温度 (创造性)</label>
              <Slider v-model="temperature" :min="0" :max="1" :step="0.1" class="w-full" />
              <div class="flex justify-between text-xs text-gray-500 mt-1">
                <span>精确</span>
                <span>平衡</span>
                <span>创造性</span>
              </div>
            </div>

            <div>
              <label class="block text-gray-300 mb-2">回复长度</label>
              <Dropdown
                v-model="maxTokens"
                :options="[
                  { name: '简短', value: 500 },
                  { name: '中等', value: 1000 },
                  { name: '详细', value: 2000 }
                ]"
                option-label="name"
                option-value="value"
                placeholder="选择长度"
                class="w-full"
              />
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <Button label="取消" class="p-button-text" @click="showSettings = false" />
        <Button label="保存设置" @click="saveSettings" />
      </template>
    </Dialog>

    <!-- 确认对话框 -->
    <ConfirmDialog></ConfirmDialog>
  </div>
</template>

<script>
import AIChatViews from '@/server/view/ai/AIChatViews'
</script>

<style lang="scss" scoped>
@use '../../styles/view/ai/AIChatView.scss'
</style>
</script>
