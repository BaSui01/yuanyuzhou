const fs = require('fs')
const path = require('path')

// 需要替换的导入路径映射
const replacements = [
  // API 相关
  [/from\s+['"]@\/api['"]/, "from '@/modules/http'"],
  [/from\s+['"]@\/api\/index['"]/, "from '@/modules/http'"],
  [/from\s+['"]@\/api\/([^'"]+)['"]/, "from '@/modules/http'"],

  // Router 相关
  [/from\s+['"]@\/modules\/router['"]/, "from '@/modules/navigation'"],
  [/from\s+['"]@\/router['"]/, "from '@/modules/navigation'"],

  // Services 相关
  [/from\s+['"]@\/modules\/services['"]/, "from '@/modules/setup'"],
  [/from\s+['"]@\/services['"]/, "from '@/modules/setup'"],

  // Mocks 相关
  [/from\s+['"]@\/modules\/mocks\/([^'"]+)['"]/, "from '@/modules/testing/mocks/$1'"],
  [/from\s+['"]@\/mocks\/([^'"]+)['"]/, "from '@/modules/testing/mocks/$1'"],

  // API 对象引用
  [/\baiAPI\b/g, 'api.ai'],
  [/\bauthAPI\b/g, 'api.auth'],
  [/\buserAPI\b/g, 'api.user'],
  [/\bmetaverseAPI\b/g, 'api.metaverse'],
]

// 需要添加 API 导入的文件
const needsApiImport = []

function updateFile(filePath) {
  try {
    let content = fs.readFileSync(filePath, 'utf8')
    let changed = false

    // 应用替换规则
    replacements.forEach(([pattern, replacement]) => {
      const newContent = content.replace(pattern, replacement)
      if (newContent !== content) {
        content = newContent
        changed = true
      }
    })

    // 检查是否使用了 API 但没有导入
    if (content.includes('api.') && !content.includes("from '@/modules/http'")) {
      // 查找 script setup 标签
      const scriptSetupMatch = content.match(/<script setup>/i)
      if (scriptSetupMatch) {
        const insertPos = scriptSetupMatch.index + scriptSetupMatch[0].length
        const importStatement = "\nimport { api } from '@/modules/http'\n"
        content = content.slice(0, insertPos) + importStatement + content.slice(insertPos)
        changed = true
        needsApiImport.push(filePath)
      }
    }

    if (changed) {
      fs.writeFileSync(filePath, content)
      console.log(`✅ 已更新: ${filePath}`)
      return true
    }

    return false
  } catch (error) {
    console.error(`❌ 更新失败 ${filePath}:`, error.message)
    return false
  }
}

function processDirectory(dir, extensions = ['.vue', '.js']) {
  let processedCount = 0
  let updatedCount = 0

  function walkDir(currentDir) {
    const files = fs.readdirSync(currentDir)

    files.forEach(file => {
      const filePath = path.join(currentDir, file)
      const stat = fs.statSync(filePath)

      if (stat.isDirectory()) {
        walkDir(filePath)
      } else if (extensions.some(ext => file.endsWith(ext))) {
        processedCount++
        if (updateFile(filePath)) {
          updatedCount++
        }
      }
    })
  }

  walkDir(dir)
  return { processedCount, updatedCount }
}

// 处理 views 目录
console.log('🚀 开始更新 views 目录...')
const viewsResult = processDirectory('./frontend/src/views')

// 处理 stores 目录
console.log('\n🚀 开始更新 stores 目录...')
const storesResult = processDirectory('./frontend/src/stores')

console.log('\n📊 更新统计:')
console.log(`Views: ${viewsResult.updatedCount}/${viewsResult.processedCount} 个文件已更新`)
console.log(`Stores: ${storesResult.updatedCount}/${storesResult.processedCount} 个文件已更新`)

if (needsApiImport.length > 0) {
  console.log('\n🔧 以下文件已自动添加 API 导入:')
  needsApiImport.forEach(file => console.log(`  - ${file}`))
}

console.log('\n✅ 导入路径更新完成！')
