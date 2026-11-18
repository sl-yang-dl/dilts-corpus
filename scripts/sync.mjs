// 把仓库根目录的数据,同步进 VitePress 站点:
//   1) data/quotes.csv, data/terms.csv -> site/quotes.ts, site/terms.ts(结构化数据,供 Vue 组件渲染)
//   2) 生成组件宿主页 site/{index,quotes,terms}.md(用 layout:page 承载自定义组件)
//   3) README.md -> site/about.md
// 在 site/ 下执行 `npm run sync`(即 node ../scripts/sync.mjs)时,路径以本文件位置为基准。
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const root = path.resolve(__dirname, '..') // 仓库根
const site = path.join(root, 'site')

// ---- 极简 CSV 解析(支持引号包裹、字段内逗号)----
function parseCSV(text) {
  const rows = []
  let row = [], field = '', inQ = false
  for (let i = 0; i < text.length; i++) {
    const c = text[i]
    if (inQ) {
      if (c === '"') {
        if (text[i + 1] === '"') { field += '"'; i++ } else inQ = false
      } else field += c
    } else if (c === '"') inQ = true
    else if (c === ',') { row.push(field); field = '' }
    else if (c === '\n' || c === '\r') {
      if (c === '\r' && text[i + 1] === '\n') i++
      row.push(field); rows.push(row); row = []; field = ''
    } else field += c
  }
  if (field.length || row.length) { row.push(field); rows.push(row) }
  const header = rows.shift() || []
  return rows
    .filter((r) => r.length > 1 || (r.length === 1 && r[0] !== ''))
    .map((r) => {
      const o = {}
      header.forEach((h, j) => (o[h.trim()] = (r[j] ?? '').trim()))
      return o
    })
}

const quotes = parseCSV(fs.readFileSync(path.join(root, 'data', 'quotes.csv'), 'utf8'))
const terms = parseCSV(fs.readFileSync(path.join(root, 'data', 'terms.csv'), 'utf8'))

fs.writeFileSync(
  path.join(site, 'quotes.ts'),
  `// 由 scripts/sync.mjs 从 data/quotes.csv 自动生成,勿手改\nexport const quotes = ${JSON.stringify(quotes, null, 2)};\n`
)
fs.writeFileSync(
  path.join(site, 'terms.ts'),
  `// 由 scripts/sync.mjs 从 data/terms.csv 自动生成,勿手改\nexport const terms = ${JSON.stringify(terms, null, 2)};\n`
)
console.log(`[sync] quotes.ts (${quotes.length}) + terms.ts (${terms.length})`)

// 组件宿主页(layout: page 全宽承载自定义组件)
fs.writeFileSync(
  path.join(site, 'index.md'),
  `---\nlayout: page\ntitle: 罗伯特·迪尔茨语录集\n---\n\n<HomeQuote />\n`
)
fs.writeFileSync(
  path.join(site, 'quotes.md'),
  `---\nlayout: page\ntitle: 语录集\n---\n\n<QuoteList />\n`
)
fs.writeFileSync(
  path.join(site, 'terms.md'),
  `---\nlayout: page\ntitle: 术语集\n---\n\n<TermList />\n`
)

// 关于页(来自 README)
fs.copyFileSync(path.join(root, 'README.md'), path.join(site, 'about.md'))
console.log('[sync] index/quotes/terms/about 页已生成')
