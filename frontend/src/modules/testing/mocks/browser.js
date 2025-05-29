import { setupWorker } from 'msw'
import { handlers } from './handlers'

// 创建模拟服务工作器
export const worker = setupWorker(...handlers)
