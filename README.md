# 罗伯特·迪尔茨语录集(语录 + 术语 + 作品)

> 收录罗伯特·迪尔茨(Robert Dilts)在 NLP 与教练体系中的**观点、金句、术语与作品**,按主题归类,每条标注出处与置信度。
> 目标:既能让人慢慢收集、阅读,也能让 **grill-me** 基于它准确回答,**不杜撰、不误传出处**。

- 🌐 在线站点(GitHub Pages):**https://sl-yang-dl.github.io/dilts-corpus/**
- 📦 仓库已**公开**;push 到 `main` 即自动构建并部署网站。

## 状态
- 🟢 语录 / 术语已结构化,单一数据源驱动网站 + 检索单元
- ⏸️ 演讲·访谈逐字稿:因无可用链接 + 搜索引擎反爬,**暂缺**,待用户提供链接后续补
- 本机可访问国内站点(Baidu/Baike/Douban),境外站点(Google/Wikipedia/YouTube)不通

## 文件结构
| 路径 | 内容 | 说明 |
|------|------|------|
| `data/quotes.csv` | **语录单一数据源** | 追加行即可;含 `date`/`occasion`/`added` 元信息列(可留空) |
| `data/terms.csv` | **术语单一数据源** | 解释 NLP / 迪尔茨专有概念 |
| `data/books.csv` | **作品单一数据源** | 他所有作品一览 + 简介 |
| `site/bio.ts` | **迪尔茨生平(结构化)** | 网站「关于」页时间线数据,驱动 `BioPage.vue` |
| `build_kb.py` | 生成器 | 读三个 CSV → 生成下方产物 |
| `语录集.md` | 按主题归类的可读语录 | 网站「语录集」页来源 |
| `术语集.md` | 专有名词表(中英对照) | 网站「术语集」页来源 |
| `05-knowledge.jsonl` | 结构化检索单元 | grill-me 检索 / 嵌入 |
| `05-structured.md` | 同上的人类可读问答对 | 人工审阅 |
| `retriever.py` | 零依赖(numpy)检索原型 | 本地验证检索效果 |
| `site/` | VitePress 站点 | 由 Vue 组件渲染(语录/术语/作品/关于) |
| `scripts/sync.mjs` | 同步脚本 | 把 CSV → `site/*.ts` 与页面(关于页由 `site/bio.ts` 驱动) |
| `.github/workflows/deploy.yml` | 自动部署 | push 即上线 GitHub Pages |

## 置信度标记约定
- ✅ **高置信(high)**:可安全归于迪尔茨的观点 / 模型表述
- ⚠️ **待核验(pending)**:广泛流传但原文或出处需核对
- ❓ **疑似误传(avoid)**:常被归于迪尔茨,实则出自他人(用于"避坑",勿引用)

## 如何添加一条语录 / 术语(日常收集)
只动两个 CSV,其余自动生成。

**加一条语录** → 在 `data/quotes.csv` 末尾追加一行:
```csv
new-id,quote,逻辑层次,逻辑层次中越上层对越下层组织力越强。,02-models.md#1,high,逻辑层次,,
```
字段:`id, category, theme, zh, source, confidence, topic, date, occasion, added`
- `category`:`quote` / `quote_pending` / `avoid` / `model` / `excerpt`(著作已独立到 `books.csv`,此处勿用 `book`)
- `theme`:所属主题(决定在语录集里的章节,如 `逻辑层次` `迪士尼策略`)
- `zh`:语录中文;`source`:出处;`confidence`:上述三档之一;`topic`:短标签
- `date` / `occasion`:**可选元信息**(如 `1990`、`某工作坊`)——需要时填,留空则不显示
- `added`:**追加日期**(你把它收进语录集的日期,如 `2026-11-23`)——用于追溯收录时间,可与 `date`(语录内容所属年代)区分;旧的批量导入条目已用 git 首次提交日期回填,新条目建议你手动填入

**加一条术语** → 在 `data/terms.csv` 末尾追加一行:
```csv
new-term,Sleight of Mouth,语言魔术,一套松动与重构限制性信念的语言模式。,换框、信念改变循环,02-models.md#4,high
```
字段:`id, zh, en, definition, related, source, confidence`

**加一部作品** → 在 `data/books.csv` 末尾追加一行:
```csv
new-book,《书名》,Book Title(英文/原名),2024,著/译/合著,一句话简介,01-bibliography.md#一,high
```
字段:`id, title, title_en, year, role, intro, source, confidence`

**生成全部产物**(语录集.md / 术语集.md / jsonl / 网站):
```bash
python3 build_kb.py
```
**发布**:`git add -A && git commit && git push` → 网站自动部署;jsonl 同步更新供 grill-me 使用。

## 本地预览网站
```bash
cd site
npm install        # 首次
npm run dev         # 本地预览 http://localhost:5173
npm run build       # 产出 site/.vitepress/dist
```
`npm run dev/build` 会先跑 `scripts/sync.mjs`,把最新的 `语录集.md`/`术语集.md` 注入站点。

## 网站部署(GitHub Pages)
- 架构参照 `book-to-skill`:VitePress + `scripts/sync.mjs` 自动同步 + `.github/workflows/deploy.yml`,push 到 `main` 即 `npm run build` → 部署 Pages。
- 基路径由 CI 注入 `VP_BASE=/dilts-corpus/`(仓库改名时需同步改)。
- 站内支持主题导航、全文搜索(中文友好)、置信度标记。

## 给 grill-me 的接入约定
1. 引用语录时优先使用 ✅ 条目;⚠️ 条目需注明"流传版本,出处待核"。
2. 遇到 ❓ 类名言,主动纠正归因,不要顺着误传回答。
3. 无法确认的内容,明确说"资料中未收录 / 待核验",而非编造。

### 最小原型 `retriever.py`(已包含,零依赖仅 numpy)
本地即可验证检索效果,无需联网/装包:
```bash
python3 retriever.py                        # 内置 3 条 demo
python3 retriever.py "迪尔茨的逻辑层次是什么"   # 单条查询
python3 retriever.py --json "地图不是疆域 是谁说的"  # JSON 返回
```
在 Python 中调用:
```python
from retriever import build_prompt
p = build_prompt("迪尔茨的逻辑层次是什么", k=3)
p['system'], p['context'], p['user']   # 直接作为 LLM 的 system/context/用户问题
```
> 升级真实句向量:把 `retriever.py` 里的 `embed()` 换成 sentence-transformers / OpenAI 等,其余逻辑无需改动。

## 待办
- [x] 联网核验著作年份与中文译名(百度百科)
- [x] 抓取 3 本代表作带出处摘录(豆瓣,见 `04-sourced-excerpts.md`)
- [x] 语录 / 术语拆为 `data/*.csv` 单一数据源,`build_kb.py` 自动生成语录集.md / 术语集.md / jsonl
- [x] 新增**作品集**页(`data/books.csv` + `BookList.vue`):所有作品一览 + 简介
- [x] **关于**页改为迪尔茨生平时间线(`site/bio.ts` + `BioPage.vue`),与项目 README 分离
- [x] 语录支持 `date` / `occasion` 元信息列(可留空)
- [x] VitePress 站点 + GitHub Pages 自动部署(仓库已公开)
- [⏸️] 补充演讲 / 访谈语录:**阻塞**(无链接 + 搜索引擎反爬),待用户提供链接后续补
