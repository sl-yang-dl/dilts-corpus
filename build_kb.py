# -*- coding: utf-8 -*-
"""从既有语料生成 grill-me 检索单元:JSONL(向量化)+ Markdown(人工审阅)。
所有内容均源自本目录 01~04 文件,出处以 source 字段保留,便于追溯。"""
import json, os

RECORDS = [
    # ---------- 模型 / 方法论 ----------
    dict(id="m-logical-levels", category="model", topic="逻辑层次",
         question="罗伯特·迪尔茨的\"逻辑层次/理解层次\"是什么?",
         answer="六层由下至上:环境→行为→能力→信念与价值观→身份→精神/系统。越上层对越下层具有更强的组织与影响力;冲突常源于跨层错位;问题卡在哪一层,就优先在哪一层工作。",
         source="02-models.md#1", confidence="high"),
    dict(id="m-disney", category="model", topic="迪士尼策略",
         question="迪尔茨的\"迪士尼策略\"怎么用?",
         answer="三种角色分时扮演:梦想家(发散创意)、实干家(落地计划)、批评家(查漏补缺)。不在同一时刻混用,以免过早批判扼杀创意或只有创意没有执行。",
         source="02-models.md#2", confidence="high"),
    dict(id="m-hero", category="model", topic="英雄之旅",
         question="迪尔茨与吉利根的\"英雄之旅\"框架是什么?",
         answer="基于 Joseph Campbell 神话结构发展为个人蜕变/教练框架。核心原则:①灵魂正在苏醒;②灵魂通过人类神经系统苏醒;③每个生命都是一段英雄之旅。衍生:生生不息的大我(Generative Self);三个心智(身体/认知/场域);意识三层(原始/自我/生生不息);整合\"阴影\"。(来源《英雄之旅》,与 Stephen Gilligan 合著)",
         source="02-models.md#3;04-sourced-excerpts.md#2", confidence="high"),
    dict(id="m-sleight", category="model", topic="语言魔术/Sleight of Mouth",
         question="迪尔茨的\"语言魔术/Sleight of Mouth\"是什么?",
         answer="一套用于松动与重构限制性信念的语言模式,系统整理于《语言的魔力》(1999)。含:意图—重新定义、换框(情境/意义/批评者)、归类(向上/向下/横向找比喻)、价值观与准则链接、后果法、用\"就像\"框架等。(来源《语言的魔力》目录)",
         source="02-models.md#4;04-sourced-excerpts.md#1", confidence="high"),
    dict(id="m-belief", category="model", topic="信念系统",
         question="迪尔茨怎么看\"信念\"?",
         answer="信念是关于自我、他人与世界的\"前提与假设\",可被识别与改变;限制性信念可用信念改变循环等处理。(来源《改变信念系统》《信念:通往健康与幸福之路》)",
         source="02-models.md#5", confidence="high"),
    dict(id="m-spelling", category="model", topic="拼写策略",
         question="迪尔茨的\"拼写策略\"是什么?",
         answer="对优秀拼写者的策略建模(视觉/听觉/触觉组合),用于改善学习困难。",
         source="02-models.md#6;02-models.md#9", confidence="high"),
    dict(id="m-perceptual", category="model", topic="感知位置",
         question="迪尔茨的\"感知位置\"怎么用?",
         answer="一/二/三位置:自己、对方、观察者(可扩展至时间/系统位置),用于理解关系、冲突整合与换位思考。",
         source="02-models.md#7", confidence="high"),
    dict(id="m-vision", category="model", topic="愿景领导力",
         question="迪尔茨的\"愿景领导力\"是什么?",
         answer="愿景是组织中最具凝聚力与驱动力的力量;领导力需在逻辑层次上对齐愿景与身份。(来源《归属感》= Visionary Leadership Skills 中译本)",
         source="02-models.md#8", confidence="high"),
    dict(id="m-techniques", category="model", topic="迪尔茨开发的技法清单",
         question="迪尔茨本人开发了哪些 NLP 技法?",
         answer="重塑印记、冲突信念整合法、魔术语言模式、拼写策略、脱敏技术、理解层次、信念改变循环。(来源《NLP模仿卓越的艺术》作者简介)",
         source="02-models.md#9;04-sourced-excerpts.md#3", confidence="high"),
    dict(id="m-nlp-principles", category="model", topic="NLP 原则(非迪尔茨原创)",
         question="\"地图不是疆域\"是迪尔茨说的吗?",
         answer="不是。它是 NLP 体系共有前提之一(亦见《NLP模仿卓越的艺术》列为\"NLP 的原则\"),源自 Alfred Korzybski(1933),并非迪尔茨原创。同理\"身心同一系统\"\"弹性法则\"也是 NLP 前提。",
         source="02-models.md#10;03-quotes.md#misattrib", confidence="high"),

    # ---------- 高置信语录(观点表述) ----------
    dict(id="q-high-1", category="quote", topic="逻辑层次影响力",
         question="迪尔茨关于逻辑层次说过什么?",
         answer="逻辑层次中,越往上的层次对越往下的层次具有越强的组织与影响力;改变要发生在最恰当的层次:若问题根植于身份层,仅在行为层干预往往无效。",
         source="03-quotes.md#high", confidence="high"),
    dict(id="q-high-2", category="quote", topic="愿景",
         question="迪尔茨怎么定义愿景?",
         answer="愿景不是目标,而是人们愿意归属的世界。(Visionary Leadership 思想)",
         source="03-quotes.md#high", confidence="high"),
    dict(id="q-high-3", category="quote", topic="创意与执行",
         question="迪尔茨关于创意与执行的看法?",
         answer="创意需要梦想家,落地需要实干家,稳健需要批评家——三者缺一不可,但要分时扮演。(迪士尼策略)",
         source="03-quotes.md#high", confidence="high"),
    dict(id="q-high-4", category="quote", topic="信念可改写",
         question="迪尔茨关于信念的看法?",
         answer="信念是我们关于自我、他人与世界的前提假设,它可以被重新书写。",
         source="03-quotes.md#high", confidence="high"),

    # ---------- 待核验语录 ----------
    dict(id="q-warn-1", category="quote_pending", topic="If you always do...",
         question="\"如果你总是做你一直在做的事,你就会得到你一直得到的结果\"是迪尔茨说的吗?",
         answer="常见于 NLP/教练圈并常归于迪尔茨,但源头存疑(类似表述见于 1980 年代多位作者)。引用时须注明\"流传版本,出处待核\"。",
         source="03-quotes.md#warn", confidence="pending"),
    dict(id="q-warn-2", category="quote_pending", topic="沟通的意义",
         question="\"沟通的意义在于你所得到的回应\"是迪尔茨说的吗?",
         answer="实为 NLP 前提假设(Bandler & Grinder 体系),非迪尔茨独创,常被一并引用。",
         source="03-quotes.md#warn", confidence="pending"),

    # ---------- 误传(避坑,勿引用) ----------
    dict(id="q-avoid-map", category="avoid", topic="地图不是疆域",
         question="用户问\"迪尔茨说过'地图不是疆域'吗\"?",
         answer="不归迪尔茨。出自 Korzybski(1933)《Science and Sanity》,由 NLP 采用,是 NLP 共有前提。详见 03-quotes.md ❓。",
         source="03-quotes.md#misattrib", confidence="high"),
    dict(id="q-avoid-anais", category="avoid", topic="我们不是看事物本来的样子",
         question="\"我们不是看事物本来的样子,而是看我们自己以为的样子\"是迪尔茨说的吗?",
         answer="出自 Anaïs Nin(安娜伊斯·宁),非迪尔茨。",
         source="03-quotes.md#misattrib", confidence="high"),
    dict(id="q-avoid-epictetus", category="avoid", topic="困扰我们的不是事情本身",
         question="\"让我们困扰的不是事情本身,而是我们对事情的看法\"是迪尔茨说的吗?",
         answer="思想源头为爱比克泰德(Epictetus)等斯多葛学派,非迪尔茨。",
         source="03-quotes.md#misattrib", confidence="high"),

    # ---------- 著作 / 内容 ----------
    dict(id="b-sleight", category="book", topic="《语言的魔力》",
         question="迪尔茨《语言的魔力》讲什么?",
         answer="原名 Sleight of Mouth(1999)。系统讲\"回应术\"语言模式,通过改变语言框架来转变信念。结构:语言与经验→框架和换框→归类→价值观与准则→信念和预期。(来源《语言的魔力》豆瓣页)",
         source="04-sourced-excerpts.md#1", confidence="high"),
    dict(id="b-hero", category="book", topic="《英雄之旅》",
         question="迪尔茨《英雄之旅》讲什么?",
         answer="与 Stephen Gilligan 合著,基于四天工作坊记录,引导读者展开自我发现的英雄之旅,对接灵性深处的部分。(来源《英雄之旅》豆瓣页)",
         source="04-sourced-excerpts.md#2", confidence="high"),
    dict(id="b-modeling", category="book", topic="《NLP模仿卓越的艺术》",
         question="迪尔茨《NLP模仿卓越的艺术》讲什么?",
         answer="原名 Modeling with NLP(1998)。系统讲解 NLP\"模型仿效\",提炼卓越人士的思想/行为模式并\"复制安装\"给他人;列出 NLP 原则与 T.O.T.E. 模型、模仿的三种感知位置。(来源《NLP模仿卓越的艺术》豆瓣页)",
         source="04-sourced-excerpts.md#3", confidence="high"),
    dict(id="b-list", category="book", topic="代表著作清单",
         question="迪尔茨写过哪些书?",
         answer="总著作量超 32 部。代表英文:Neuro-Linguistic Programming Vol.I(1980)、Changing Belief Systems with NLP(1990)、Beliefs:Pathways to Health and Well-Being(1990)、Tools for Dreamers(1991)、Strategies of Genius 1-3(1994-95)、Visionary Leadership Skills(1996)、Modeling with NLP(1998)、Sleight of Mouth(1999)、The Encyclopedia of Systemic NLP(2000)、Alpha Leadership(2002)、From Coach to Awakener(2003)、The Hero's Journey(2009)、NLP II(2010)、Next Generation Entrepreneurs(2015)、Generative Coaching(与 Gilligan)。中译本含《语言的魔力》《从教练到唤醒者》《英雄之旅》《归属感》《卓越元素》《NLP模仿卓越的艺术》《集体智慧》《信念的魔力》等。(来源 01-bibliography.md,百度百科核验)",
         source="01-bibliography.md", confidence="high"),
    dict(id="b-falsematch", category="book", topic="易混淆书目警示",
         question="哪些书容易和迪尔茨搞混?",
         answer="豆瓣检索会张冠李戴:搜\"归属感 迪尔茨\"会命中 Alastair L. Day 的金融书;搜\"从教练到唤醒者\"会命中罗比·斯坦豪斯《教练的唤醒力》。引用前务必核对作者为 Robert Dilts。",
         source="01-bibliography.md#五;04-sourced-excerpts.md#误匹配", confidence="high"),

    # ---------- 书籍原话摘录(源自已抓取的 3 本书,非网络名言) ----------
    dict(id="x-sleight-worldview", category="excerpt", topic="回应术与世界观",
         question="迪尔茨在《语言的魔力》里怎么描述'回应术'的作用?",
         answer="回应术能在不知不觉间转变我们的信念,教会我们一种全新的世界观——这就是回应术的神奇之处;它让我们拥有一个积极的人生态度、一种快乐健康的心理状态。",
         source="04-sourced-excerpts.md#1", confidence="high"),
    dict(id="x-hero-meaning", category="excerpt", topic="英雄之旅的核心问题",
         question="迪尔茨/吉利根在《英雄之旅》中提出的核心问题是什么?",
         answer="英雄之旅的核心是:你怎样让生命活得有意义?灵性召唤你去体验的深刻的生命是什么样子?本书由斯蒂芬·吉利根和罗伯特·迪尔茨主持的四天工作坊记录整理而成。",
         source="04-sourced-excerpts.md#2", confidence="high"),
    dict(id="x-modeling-core", category="excerpt", topic="模型仿效的核心价值",
         question="迪尔茨怎么看 NLP 的'模型仿效/modeling'?",
         answer="模型仿效(modeling)是 NLP 最核心的学问之一:可提炼卓越人士的思想模式与行为模式,转化为'思想程序',从而'复制安装'给其他人,让更多人迈向卓越。",
         source="04-sourced-excerpts.md#3", confidence="high"),
    dict(id="x-systemic-nlp", category="excerpt", topic="系统派NLP",
         question="什么是'系统派 NLP(Systemic NLP)'?",
         answer="迪尔茨在策略与信念系统的 NLP 技术方面做了大量开创性工作,他对 NLP 的发展被称为'系统派 NLP(Systemic NLP)'。",
         source="04-sourced-excerpts.md#3", confidence="high"),
    dict(id="x-nlp-university", category="excerpt", topic="NLP大学",
         question="迪尔茨与 NLP 大学的关系?",
         answer="迪尔茨从 1975 年起成为 NLP 的开发者、作者、培训师与顾问,参与创立位于加州圣克鲁兹的 NLP 大学(NLP University),并开创性将 NLP 应用于健康、领导力、创新及教育。",
         source="04-sourced-excerpts.md#2", confidence="high"),
]

HERE = os.path.dirname(os.path.abspath(__file__))

# 1) JSONL —— 向量化友好
with open(os.path.join(HERE, "05-knowledge.jsonl"), "w", encoding="utf-8") as f:
    for r in RECORDS:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

# 2) Markdown 问答对 —— 人工审阅
groups = {
    "model": "一、模型 / 方法论",
    "quote": "二、高置信语录(观点表述)",
    "quote_pending": "三、待核验语录(引用须注明出处待核)",
    "avoid": "四、常见误传(避坑,勿引用)",
    "book": "五、著作与内容",
    "excerpt": "六、书籍原话摘录(源自已抓取的 3 本书)",
}
md = ["# grill-me 检索问答对(结构化)\n",
      "> 由 `build_kb.py` 从 01~04 语料自动生成。每条含检索问句 + 答案 + 出处 + 置信度。\n",
      f"> 共 {len(RECORDS)} 条。置信度:high=可安全引用 / pending=待核 / avoid=误传勿引。\n"]
for cat, title in groups.items():
    items = [r for r in RECORDS if r["category"] == cat]
    if not items:
        continue
    md.append(f"\n## {title}\n")
    for r in items:
        md.append(f"**Q: {r['question']}**  _(id={r['id']}, 置信={r['confidence']}, 出处={r['source']})_\n")
        md.append(f"> A: {r['answer']}\n")

with open(os.path.join(HERE, "05-structured.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"生成完成: {len(RECORDS)} 条 -> 05-knowledge.jsonl + 05-structured.md")
