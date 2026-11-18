# 核验计划:迪尔茨著作 / 语录

> 当前环境**无外网**,无法实时核验。本文件是"离线准备的核验清单",
> 联网后按步骤执行即可把 `01-bibliography.md` / `03-quotes.md` 的 ⚠️ 条目转为 ✅。

## 一、权威核验来源(按可信度)
1. **迪尔茨官网**:https://www.nlpuniversity.com 、 https://diltsstrategies.com (书目最权威)
2. **Wikipedia**: https://en.wikipedia.org/wiki/Robert_Dilts (概览 + 书单)
3. **Open Library**: https://openlibrary.org (ISBN / 初版年份)
4. **WorldCat**: https://www.worldcat.org (馆藏初版信息)
5. **Google Books / Goodreads**: 中文译名与封面
6. **豆瓣**: https://book.douban.com (中文译本译名 / 出版社)

## 二、逐本核验清单(状态: ☐ 未核)
- [ ] Neuro-Linguistic Programming Volume I (1980, with Bandler/Grinder/DeLozier)
- [ ] Applications of Neuro-Linguistic Programming (1983)
- [ ] Roots of Neuro-Linguistic Programming (1987, with Grinder)
- [ ] Changing Belief Systems with NLP (1990) — 中文译名《改变信念系统》?
- [ ] Beliefs: Pathways to Health and Well-Being (1990, with Hallbom/Smith) — 中文《信念》?
- [ ] Tools for Dreamers (1991, with Epstein) — 含迪士尼策略
- [ ] Strategies of Genius Vol. 1 (1994)
- [ ] Strategies of Genius Vol. 2 (1994)
- [ ] Strategies of Genius Vol. 3 (1995)
- [ ] Visionary Leadership Skills (1996)
- [ ] Modeling with NLP (1998)
- [ ] Sleight of Mouth (1999) — 中文《语言的魔术》/《口语戏法》?
- [ ] The Encyclopedia of Systemic NLP (2000, with DeLozier)
- [ ] From Coach to Awakener (2003) — 中文《从教练到唤醒者》?
- [ ] The Hero's Journey (2003, with Gilligan) — 中文《英雄之旅》?
- [ ] Coaching: The NLP Approach (2003, with McDermott) — 中文《NLP 教练》?
- [ ] Alpha to Omega (2007)
- [ ] NLP II: The Next Generation (2010, with DeLozier/Epstein)
- [ ] The Ultimate Introduction to NLP (2014, with DeLozier/Passion)

> 每本核三项:**初版年份**、**原始书名拼写**、**中文译名/出版社**(若有)。

## 三、语录核验清单(状态: ☐ 未核)
- [ ] "If you always do what you've always done…" 是否确归 Dilts(查其著作索引)
- [ ] "沟通的意义在于回应" 是否 Dilts 表述,还是 NLP 前提假设
- [ ] ❓ 三类误传条目:确认 Korzybski / Anaïs Nin / Epictetus 原文归属(用于固化"避坑"规则)

## 四、联网后可执行的核查脚本(示例)
```bash
# 用 Open Library 按书名查初版年份(需联网)
for t in "Sleight of Mouth" "From Coach to Awakener" "Strategies of Genius"; do
  curl -sS "https://openlibrary.org/search.json?title=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$t")" \
    | python3 -c "import sys,json;d=json.load(sys.stdin);[print(b.get('title'),b.get('first_publish_year')) for b in d.get('docs',[])[:3]]"
done
```

## 五、完成判据
- 书目 19 本年份/译名全部 ✅
- ⚠️ 语录每条标注"已核 / 改归 / 删除"
- 更新 `README.md` 状态为 🟢 已核验
