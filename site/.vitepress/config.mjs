import { defineConfig } from 'vitepress'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// 本地开发 base 为 '/';GitHub Pages 项目页需设为 '/<仓库名>/'
// 由 CI 通过环境变量 VP_BASE 注入(见 .github/workflows/deploy.yml)。
const base = process.env.VP_BASE || '/'

const head = [
  ['link', { rel: 'icon', type: 'image/svg+xml', href: `${base}favicon.svg` }],
]

// 语录/术语页用 layout:page 全宽承载组件,无需侧边栏;顶部导航即可。
export default defineConfig({
  base,
  head,
  title: '罗伯特·迪尔茨语录集',
  description: '迪尔茨在 NLP 与教练体系中的观点、金句与术语,按主题归类,标注出处与置信度。',
  lang: 'zh-CN',
  lastUpdated: true,
  // 关掉 cleanUrls:GitHub Pages 静态托管不支持无扩展名路径,
  // 必须用 /quotes.html 这种带扩展名的链接(否则导航 404)。
  cleanUrls: false,
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '语录集', link: '/quotes' },
      { text: '术语集', link: '/terms' },
      { text: '作品集', link: '/books' },
      { text: '关于', link: '/about' }
    ],
    search: {
      provider: 'local',
      options: {
        detail: true,
        miniSearch: {
          // 中文按字/词更友好:前缀 + 轻度模糊
          searchOptions: { prefix: true, fuzzy: 0.2 }
        }
      }
    },
    outline: { level: [2, 3] },
    docFooter: { prev: false, next: false },
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '菜单',
    darkModeSwitchLabel: '主题',
    lastUpdatedText: '最后更新'
  }
})
