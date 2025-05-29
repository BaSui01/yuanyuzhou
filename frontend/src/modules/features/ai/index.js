// AI 功能模块导出

// 组合式函数 (Composables)
export { useChatView } from './composables/useChatView'
export { useImageAnalysis } from './composables/useImageAnalysis'
export { useAIChat } from './composables/useAIChat'
export { default as useAICompanion } from './composables/useAICompanion'
export { default as useVoiceLab } from './composables/useVoiceLab'

// 工具函数
export * from './utils'

// 类型定义（如果有）
export * from './types'

// 导出 AI API 服务
export { default as aiService } from './api/aiService'

// 导出 AI 组件（如果有的话）
// export { default as AIChat } from './components/AIChat.vue'
// export { default as AICompanion } from './components/AICompanion.vue'
