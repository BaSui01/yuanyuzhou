<template>
    <div class="floating-ai-assistant" :class="{ 'expanded': isExpanded }">
        <!-- AI助手头像 -->
        <div class="assistant-avatar" @click="toggleExpanded" v-tooltip="isExpanded ? '收起助手' : '展开AI助手'">
            <Avatar :image="assistantAvatar" class="avatar pulse-animation" size="large" shape="circle" />
            <div class="status-indicator">
                <i class="pi pi-circle-fill"></i>
            </div>
            <div class="notification-badge" v-if="unreadMessages > 0">
                {{ unreadMessages }}
            </div>
        </div>

        <!-- 展开的对话面板 -->
        <Transition name="slide-up">
            <div v-if="isExpanded" class="chat-panel">
                <div class="chat-header">
                    <div class="assistant-info">
                        <Avatar :image="assistantAvatar" size="small" />
                        <div class="info">
                            <h4>{{ assistantName }}</h4>
                            <span class="status">{{ assistantStatus }}</span>
                        </div>
                    </div>

                    <div class="header-actions">
                        <Button icon="pi pi-cog" text size="small" @click="openSettings" v-tooltip="'设置'" />
                        <Button icon="pi pi-minus" text size="small" @click="toggleExpanded" v-tooltip="'最小化'" />
                    </div>
                </div>

                <div class="chat-messages" ref="messagesContainer">
                    <div v-for="message in messages" :key="message.id" class="message"
                        :class="{ 'user': message.sender === 'user', 'ai': message.sender === 'ai' }">
                        <div class="message-avatar">
                            <Avatar :image="message.sender === 'user' ? userAvatar : assistantAvatar" size="small" />
                        </div>
                        <div class="message-content">
                            <div class="message-bubble">
                                <p>{{ message.content }}</p>
                                <div class="message-actions" v-if="message.sender === 'ai'">
                                    <Button icon="pi pi-copy" text size="small" @click="copyMessage(message.content)"
                                        v-tooltip="'复制'" />
                                    <Button icon="pi pi-thumbs-up" text size="small" @click="likeMessage(message.id)"
                                        v-tooltip="'点赞'" />
                                </div>
                            </div>
                            <span class="message-time">{{ formatTime(message.timestamp) }}</span>
                        </div>
                    </div>

                    <!-- 打字指示器 -->
                    <div v-if="isTyping" class="message ai">
                        <div class="message-avatar">
                            <Avatar :image="assistantAvatar" size="small" />
                        </div>
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
                    <div class="input-wrapper">
                        <InputText v-model="newMessage" placeholder="输入消息..." @keypress.enter="sendMessage"
                            :disabled="isTyping" class="message-input" />
                        <Button icon="pi pi-microphone" text @click="toggleVoiceInput"
                            :class="{ 'active': isVoiceActive }" v-tooltip="'语音输入'" />
                        <Button icon="pi pi-send" @click="sendMessage" :disabled="!newMessage.trim() || isTyping"
                            v-tooltip="'发送'" />
                    </div>

                    <div class="quick-actions">
                        <Button v-for="action in quickActions" :key="action.id" :label="action.label" size="small"
                            outlined @click="sendQuickMessage(action.message)" class="quick-action-btn" />
                    </div>
                </div>
            </div>
        </Transition>

        <!-- 设置对话框 -->
        <Dialog v-model:visible="showSettings" header="AI助手设置" modal class="settings-dialog">
            <div class="settings-content">
                <div class="setting-group">
                    <label>助手名称</label>
                    <InputText v-model="tempSettings.name" />
                </div>

                <div class="setting-group">
                    <label>助手个性</label>
                    <Dropdown v-model="tempSettings.personality" :options="personalityOptions" optionLabel="label"
                        optionValue="value" />
                </div>

                <div class="setting-group">
                    <label>语音设置</label>
                    <div class="voice-settings">
                        <div class="setting-item">
                            <label>语音速度</label>
                            <Slider v-model="tempSettings.voiceSpeed" :min="0.5" :max="2" :step="0.1" />
                        </div>
                        <div class="setting-item">
                            <label>语音音调</label>
                            <Slider v-model="tempSettings.voicePitch" :min="0.5" :max="2" :step="0.1" />
                        </div>
                    </div>
                </div>

                <div class="setting-group">
                    <label>通知设置</label>
                    <div class="notification-settings">
                        <div class="setting-item">
                            <Checkbox v-model="tempSettings.enableNotifications" inputId="notifications" />
                            <label for="notifications">启用通知</label>
                        </div>
                        <div class="setting-item">
                            <Checkbox v-model="tempSettings.enableSounds" inputId="sounds" />
                            <label for="sounds">启用声音</label>
                        </div>
                    </div>
                </div>
            </div>

            <template #footer>
                <Button label="取消" icon="pi pi-times" text @click="showSettings = false" />
                <Button label="保存" icon="pi pi-check" @click="saveSettings" />
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, watch } from 'vue'
import { useAIStore } from '@/stores/ai'
import { useAuthStore } from '@/stores/auth'

// PrimeVue 组件
import Avatar from 'primevue/avatar'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Dialog from 'primevue/dialog'
import Dropdown from 'primevue/dropdown'
import Slider from 'primevue/slider'
import Checkbox from 'primevue/checkbox'

// Stores
const aiStore = useAIStore()
const authStore = useAuthStore()

// 响应式数据
const isExpanded = ref(false)
const isTyping = ref(false)
const isVoiceActive = ref(false)
const newMessage = ref('')
const unreadMessages = ref(0)
const showSettings = ref(false)
const messagesContainer = ref(null)

// AI助手信息
const assistantName = computed(() => aiStore.petName || 'AI助手')
const assistantAvatar = computed(() => '/img/ai-assistant.svg')
const assistantStatus = computed(() => '在线')
const userAvatar = computed(() => authStore.userAvatar || '/avatars/default-user.svg')

// 消息列表
const messages = ref([
    {
        id: 1,
        sender: 'ai',
        content: '你好！我是您的AI助手，有什么可以帮助您的吗？',
        timestamp: new Date(Date.now() - 60000)
    }
])

// 快捷操作
const quickActions = ref([
    { id: 1, label: '今日安排', message: '我今天有什么安排？' },
    { id: 2, label: '天气查询', message: '今天天气怎么样？' },
    { id: 3, label: '新闻摘要', message: '给我总结一下今日新闻' },
    { id: 4, label: '帮助', message: '你能做什么？' }
])

// 设置相关
const tempSettings = ref({
    name: '小助手',
    personality: 'friendly',
    voiceSpeed: 1.0,
    voicePitch: 1.0,
    enableNotifications: true,
    enableSounds: true
})

const personalityOptions = ref([
    { label: '友好型', value: 'friendly' },
    { label: '专业型', value: 'professional' },
    { label: '幽默型', value: 'humorous' },
    { label: '简洁型', value: 'concise' }
])

// 方法
const toggleExpanded = () => {
    isExpanded.value = !isExpanded.value
    if (isExpanded.value) {
        unreadMessages.value = 0
        nextTick(() => {
            scrollToBottom()
        })
    }
}

const sendMessage = async () => {
    if (!newMessage.value.trim() || isTyping.value) return

    const userMessage = {
        id: Date.now(),
        sender: 'user',
        content: newMessage.value,
        timestamp: new Date()
    }

    messages.value.push(userMessage)
    const messageText = newMessage.value
    newMessage.value = ''

    await nextTick()
    scrollToBottom()

    // 模拟AI回复
    await simulateAIResponse(messageText)
}

const sendQuickMessage = async (message) => {
    newMessage.value = message
    await sendMessage()
}

const simulateAIResponse = async (userMessage) => {
    isTyping.value = true

    // 模拟思考时间
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000))

    const aiResponse = {
        id: Date.now(),
        sender: 'ai',
        content: generateAIResponse(userMessage),
        timestamp: new Date()
    }

    messages.value.push(aiResponse)
    isTyping.value = false

    if (!isExpanded.value) {
        unreadMessages.value++
    }

    await nextTick()
    scrollToBottom()
}

const generateAIResponse = (userMessage) => {
    const responses = [
        '我理解了您的问题，让我为您查找相关信息...',
        '这是一个很有趣的问题！根据我的分析...',
        '我很乐意帮助您解决这个问题。',
        '基于您提供的信息，我建议...',
        '让我为您提供一些有用的建议。'
    ]

    return responses[Math.floor(Math.random() * responses.length)]
}

const copyMessage = async (content) => {
    try {
        await navigator.clipboard.writeText(content)
        // 可以添加一个提示
    } catch (err) {
        console.error('复制失败:', err)
    }
}

const likeMessage = (messageId) => {
    // 实现点赞逻辑
    console.log('点赞消息:', messageId)
}

const toggleVoiceInput = () => {
    isVoiceActive.value = !isVoiceActive.value

    if (isVoiceActive.value) {
        startVoiceRecognition()
    } else {
        stopVoiceRecognition()
    }
}

const startVoiceRecognition = () => {
    // 实现语音识别
    console.log('开始语音识别')
}

const stopVoiceRecognition = () => {
    // 停止语音识别
    console.log('停止语音识别')
}

const openSettings = () => {
    showSettings.value = true
}

const saveSettings = () => {
    // 保存设置到 store
    aiStore.updateAssistantSettings(tempSettings.value)
    showSettings.value = false
}

const scrollToBottom = () => {
    if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
}

const formatTime = (timestamp) => {
    const now = new Date()
    const diff = now - timestamp
    const minutes = Math.floor(diff / 60000)

    if (minutes < 1) return '刚刚'
    if (minutes < 60) return `${minutes}分钟前`

    const hours = Math.floor(minutes / 60)
    if (hours < 24) return `${hours}小时前`

    return timestamp.toLocaleDateString()
}

// 监听窗口大小变化
watch(isExpanded, (expanded) => {
    if (expanded) {
        nextTick(() => {
            scrollToBottom()
        })
    }
})

onMounted(() => {
    // 初始化设置
    tempSettings.value = { ...aiStore.assistantSettings }
})
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables' as vars;
@use '@/assets/styles/mixins' as mixins;

.floating-ai-assistant {
    position: fixed;
    bottom: vars.spacing(xl);
    right: vars.spacing(xl);
    z-index: vars.z-index(modal);

    @include vars.responsive(sm) {
        bottom: vars.spacing(lg);
        right: vars.spacing(lg);
    }

    .assistant-avatar {
        position: relative;
        cursor: pointer;
        transition: vars.transition(all);

        &:hover {
            @include mixins.hover-lift(5px);
        }

        .avatar {
            @include mixins.glow-effect(vars.color(primary), 15px, 0.4);
            border: 3px solid rgba(vars.color(primary), 0.3);
        }

        .status-indicator {
            position: absolute;
            bottom: 2px;
            right: 2px;
            color: vars.color(success);
            animation: pulse-glow 2s ease-in-out infinite;
        }

        .notification-badge {
            position: absolute;
            top: -5px;
            right: -5px;
            background: vars.color(error);
            color: white;
            border-radius: vars.border-radius(full);
            min-width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: vars.font-size(xs);
            font-weight: vars.font-weight(bold);
        }
    }

    .chat-panel {
        position: absolute;
        bottom: 60px;
        right: 0;
        width: 350px;
        height: 500px;
        @include mixins.glass-effect(0.95);
        border: 1px solid vars.color(border-primary);
        border-radius: vars.border-radius(xl);
        box-shadow: vars.shadow(2xl);
        display: flex;
        flex-direction: column;
        overflow: hidden;

        @include vars.responsive(sm) {
            width: 300px;
            height: 400px;
        }

        .chat-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: vars.spacing(md);
            border-bottom: 1px solid vars.color(border-primary);

            .assistant-info {
                display: flex;
                align-items: center;
                gap: vars.spacing(sm);

                .info {
                    h4 {
                        margin: 0;
                        font-size: vars.font-size(sm);
                        font-weight: vars.font-weight(semibold);
                    }

                    .status {
                        font-size: vars.font-size(xs);
                        color: vars.color(success);
                    }
                }
            }

            .header-actions {
                display: flex;
                gap: vars.spacing(xs);
            }
        }

        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: vars.spacing(md);
            display: flex;
            flex-direction: column;
            gap: vars.spacing(md);

            .message {
                display: flex;
                gap: vars.spacing(sm);

                &.user {
                    flex-direction: row-reverse;

                    .message-content {
                        align-items: flex-end;

                        .message-bubble {
                            background: linear-gradient(135deg, vars.color(primary), vars.color(secondary));
                            color: white;
                        }
                    }
                }

                &.ai {
                    .message-bubble {
                        background: rgba(255, 255, 255, 0.1);
                        color: vars.color(text-primary);
                    }
                }

                .message-avatar {
                    flex-shrink: 0;
                }

                .message-content {
                    display: flex;
                    flex-direction: column;
                    max-width: 70%;

                    .message-bubble {
                        padding: vars.spacing(sm) vars.spacing(md);
                        border-radius: vars.border-radius(lg);
                        position: relative;

                        p {
                            margin: 0;
                            font-size: vars.font-size(sm);
                            line-height: 1.4;
                        }

                        .message-actions {
                            display: flex;
                            gap: vars.spacing(xs);
                            margin-top: vars.spacing(xs);
                            opacity: 0;
                            transition: vars.transition(opacity);
                        }

                        &:hover .message-actions {
                            opacity: 1;
                        }
                    }

                    .message-time {
                        font-size: vars.font-size(xs);
                        color: vars.color(text-muted);
                        margin-top: vars.spacing(xs);
                    }
                }
            }

            .typing-indicator {
                display: flex;
                align-items: center;
                gap: vars.spacing(xs);
                padding: vars.spacing(sm) vars.spacing(md);
                background: rgba(255, 255, 255, 0.1);
                border-radius: vars.border-radius(lg);

                span {
                    width: 6px;
                    height: 6px;
                    background: vars.color(text-secondary);
                    border-radius: vars.border-radius(full);
                    animation: typing 1.4s ease-in-out infinite;

                    &:nth-child(2) {
                        animation-delay: 0.2s;
                    }

                    &:nth-child(3) {
                        animation-delay: 0.4s;
                    }
                }
            }
        }

        .chat-input {
            padding: vars.spacing(md);
            border-top: 1px solid vars.color(border-primary);

            .input-wrapper {
                display: flex;
                gap: vars.spacing(sm);
                margin-bottom: vars.spacing(sm);

                .message-input {
                    flex: 1;
                }

                .active {
                    color: vars.color(error);
                    animation: pulse-glow 1s ease-in-out infinite;
                }
            }

            .quick-actions {
                display: flex;
                flex-wrap: wrap;
                gap: vars.spacing(xs);

                .quick-action-btn {
                    font-size: vars.font-size(xs);
                    padding: vars.spacing(xs) vars.spacing(sm);
                }
            }
        }
    }

    &.expanded {
        .assistant-avatar {
            .avatar {
                @include mixins.glow-effect(vars.color(secondary), 20px, 0.6);
            }
        }
    }
}

.settings-dialog {
    .settings-content {
        display: flex;
        flex-direction: column;
        gap: vars.spacing(lg);
        min-width: 400px;

        .setting-group {
            display: flex;
            flex-direction: column;
            gap: vars.spacing(sm);

            label {
                font-weight: vars.font-weight(semibold);
                color: vars.color(text-primary);
            }

            .voice-settings,
            .notification-settings {
                display: flex;
                flex-direction: column;
                gap: vars.spacing(md);
                padding-left: vars.spacing(md);

                .setting-item {
                    display: flex;
                    align-items: center;
                    gap: vars.spacing(sm);

                    label {
                        font-weight: vars.font-weight(normal);
                        font-size: vars.font-size(sm);
                    }
                }
            }
        }
    }
}

// 动画
.slide-up-enter-active,
.slide-up-leave-active {
    transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
    opacity: 0;
    transform: translateY(20px);
}

@keyframes typing {

    0%,
    60%,
    100% {
        transform: translateY(0);
    }

    30% {
        transform: translateY(-10px);
    }
}

@keyframes pulse-glow {

    0%,
    100% {
        opacity: 1;
    }

    50% {
        opacity: 0.5;
    }
}
</style>
