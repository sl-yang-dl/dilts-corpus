// scripts/sync.mjs
// 把 data/*.csv 同步进 VitePress 站点:
//   1) 解析为结构化数据 -> site/quotes.ts / terms.ts / books.ts(供组件渲染)
//   2) 生成承载组件的极简页面:index/quotes/terms/books/about(.md)
//   3) about 页内容来自 content/bio.md(迪尔茨生平),而非项目 README
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const ROOT = path.resolve(__dirname, '..')
const SITE = path.join(ROOT, 'site')

// 极简 CSV 解析:支持引号包裹与字段内逗号
function parseCSV(text) {
  const rows = []
  let row = [], field = '', inQ = false
  for (let i = 0; i < text.length; i++) {
    const c = text[i]
    if (inQ) {
      if (c === '"' && text[i + 1] === '"') { field += '"'; i++ }
      else if (c === '"') inQ = false
      else field += c
    } else {
      if (c === '"') inQ = true
      else if (c === ',') { row.push(field); field = '' }
      else if (c === '\n') { row.push(field); rows.push(row); row = []; field = '' }
      else if (c === '\r') { /* skip */ }
      else field += c
    }
  }
  if (field.length || row.length) { row.push(field); rows.push(row) }
  const head = rows.shift().map((h) => h.trim())
  return rows.filter((r) => r.length > 1 || r[0].trim()).map((r) => {
    const o = {}
    head.forEach((h, i) => { o[h] = (r[i] ?? '').trim() })
    return o
  })
}

function toTSArray(name, arr) {
  return `export const ${name} = ${JSON.stringify(arr, null, 2)}\n`
}

function writeFile(rel, content) {
  const p = path.join(SITE, rel)
  fs.mkdirSync(path.dirname(p), { recursive: true })
  fs.writeFileSync(p, content, 'utf-8')
}

function readCSV(name) {
  return parseCSV(fs.readFileSync(path.join(ROOT, 'data', name), 'utf-8'))
}

// ---- 1. 结构化数据 ----
const quotes = readCSV('quotes.csv')
const terms = readCSV('terms.csv')
const books = readCSV('books.csv')
writeFile('quotes.ts', toTSArray('quotes', quotes))
writeFile('terms.ts', toTSArray('terms', terms))
writeFile('books.ts', toTSArray('books', books))
console.log(`[sync] quotes.ts (${quotes.length}) + terms.ts (${terms.length}) + books.ts (${books.length})`)

// ---- 2. 页面 ----
writeFile('index.md', `---\nlayout: page\n---\n\n<HomeQuote />\n`)
writeFile('quotes.md', `---\nlayout: page\n---\n\n<QuoteList />\n`)
writeFile('terms.md', `---\nlayout: page\n---\n\n<TermList />\n`)
writeFile('books.md', `---\nlayout: page\n---\n\n<BookList />\n`)

// about 页 = 生平时间线,由 site/bio.ts 驱动 <BioPage /> 渲染
writeFile('about.md', `---\nlayout: page\ntitle: 关于罗伯特·迪尔茨\n---\n\n<BioPage />\n`)

console.log('[sync] index/quotes/terms/books/about 页已生成')
