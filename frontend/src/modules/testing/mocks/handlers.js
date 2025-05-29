import { rest } from 'msw'
import { authHandlers } from './modules/auth'
import { userHandlers } from './modules/user'
import { aiHandlers } from './modules/ai'
import { metaverseHandlers } from './modules/metaverse'

// 合并所有处理程序
export const handlers = [
  ...authHandlers,
  ...userHandlers,
  ...aiHandlers,
  ...metaverseHandlers
]
