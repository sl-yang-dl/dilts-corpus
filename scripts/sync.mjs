// 把仓库根目录由 build_kb.py 生成的语录/术语 markdown 同步进 VitePress 站点。
// 在 site/ 下执行 `npm run sync`(即 node ../scripts/sync.mjs)时,路径以本文件位置为基准。
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const root = path.resolve(__dirname, '..') // 仓库根
const site = path.join(root, 'site')

const jobs = [
  ['语录集.md', 'quotes.md'],
  ['术语集.md', 'terms.md'],
  ['README.md', 'about.md']
]

for (const [src, dst] of jobs) {
  const from = path.join(root, src)
  const to = path.join(site, dst)
  if (!fs.existsSync(from)) {
    console.warn(`[sync] 跳过(源不存在): ${src}`)
    continue
  }
  fs.copyFileSync(from, to)
  console.log(`[sync] ${src} -> site/${dst}`)
}
