// 元宇宙功能模块导出

// 组合式函数 (Composables)
export { default as useMetaverse } from './composables/useMetaverse'
export { default as useAvatar } from './composables/useAvatar'
export { default as useSpaces } from './composables/useSpaces'
export { default as useEvents } from './composables/useEvents'
export { default as useItems } from './composables/useItems'

// 工具函数
export * from './utils'

// 类型定义（如果有）
export * from './types'

// 导出 API 服务
export { default as metaverseService } from './api/metaverseService'
