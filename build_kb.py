# -*- coding: utf-8 -*-
"""罗伯特·迪尔茨 语录集 · 单一数据源生成器。

日常只维护两个 CSV(手动往里追加行即可):
  - data/quotes.csv  语录(观点 / 金句 / 模型 / 著作 ……),字段见首行
  - data/terms.csv   术语(专有名词),字段见首行

改完跑一次 `python3 build_kb.py`,自动同步产出:
  - 语录集.md          按主题归类的可读语录集(门面)
  - 术语集.md          NLP / 迪尔茨专有名词表
  - 05-knowledge.jsonl 向量化友好检索单元(grill-me / 网站共用)
  - 05-structured.md   同上的人类可读问答对

检索端 retriever.py 读取 05-knowledge.jsonl,无需改动。
"""
import json, os, csv

HERE = os.path.dirname(os.path.abspath(__file__))
QUOTES_CSV = os.path.join(HERE, "data", "quotes.csv")
TERMS_CSV = os.path.join(HERE, "data", "terms.csv")

# 语录集章节优先顺序(其余主题按出现顺序补在末尾)
THEME_ORDER = [
    "逻辑层次", "愿景与领导力", "迪士尼策略", "信念",
    "语言魔术 / 回应术", "英雄之旅", "模型仿效 / 系统派 NLP",
    "学习策略", "感知位置", "著作", "常见误传(勿归于迪尔茨)", "待核验",
]

# 结构化分组(供 05-structured.md / jsonl)
CAT_GROUPS = {
    "quote": "一、语录(观点表述)",
    "quote_pending": "二、待核验语录",
    "avoid": "三、常见误传(避坑,勿引用)",
    "model": "四、模型与方法论",
    "excerpt": "五、书籍原话摘录",
    "book": "六、著作与内容",
    "term": "七、术语集(NLP / 迪尔茨专有名词)",
}

BADGE = {"high": "✅", "pending": "⚠️", "avoid": "❓"}


def load_quotes():
    with open(QUOTES_CSV, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_terms():
    with open(TERMS_CSV, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def to_records():
    """把 CSV 统一成检索记录(id/category/theme/topic/question/answer/source/confidence)。"""
    recs = []
    for r in load_quotes():
        recs.append(dict(
            id=r["id"], category=r["category"], theme=r["theme"], topic=r.get("topic", ""),
            question=r["zh"], answer=r["zh"],
            source=r["source"], confidence=r["confidence"],
        ))
    for t in load_terms():
        recs.append(dict(
            id=t["id"], category="term", theme="术语", topic=t["zh"],
            question=f"{t['zh']}({t.get('en','')}) 是什么?",
            answer=t["definition"],
            source=t["source"], confidence=t["confidence"],
        ))
    return recs


def theme_sequence(present):
    known = [t for t in THEME_ORDER if t in present]
    extra = sorted(t for t in present if t not in THEME_ORDER)
    return known + extra


def build_quotes_md(recs):
    groups = {}
    for r in recs:
        if r["category"] == "term":
            continue
        groups.setdefault(r["theme"], []).append(r)
    seq = theme_sequence(groups.keys())
    out = [
        "# 罗伯特·迪尔茨语录集\n",
        "> 收录迪尔茨在其著作与 NLP 体系中表述的观点与金句,按主题归类。\n",
        "> 置信度:**✅ 可安全引用** · **⚠️ 待核验** · **❓ 误传勿引**。每条标注出处,便于溯源。\n",
        "> 来源:02-models.md / 03-quotes.md / 04-sourced-excerpts.md(均经百度百科、豆瓣核验)。\n",
        "> 本文件由 `build_kb.py` 从 `data/quotes.csv` 生成,往 CSV 追加语录后重跑即可同步。\n",
    ]
    for t in seq:
        items = groups.get(t)
        if not items:
            continue
        out.append(f"\n## {t}\n")
        for r in items:
            b = BADGE.get(r["confidence"], "")
            out.append(f"- {b} 「{r['answer']}」\n  _(出处:{r['source']})_\n")
    return "\n".join(out)


def build_terms_md(terms):
    out = [
        "# 罗伯特·迪尔茨 术语集(NLP 专有名词)\n",
        "> 收录迪尔茨体系中的关键术语:中文、英文原名、定义、相关概念与出处。\n",
        "> 由 `build_kb.py` 从 `data/terms.csv` 生成,往 CSV 追加术语后重跑即可同步。\n",
        "\n## 术语\n",
    ]
    for t in terms:
        en = t.get("en", "")
        rel = t.get("related", "")
        out.append(f"- **{t['zh']}** / {en}\n")
        out.append(f"  定义:{t['definition']}\n")
        if rel:
            out.append(f"  相关:{rel}\n")
        out.append(f"  出处:{t['source']}\n")
    return "\n".join(out)


def build_jsonl(recs):
    with open(os.path.join(HERE, "05-knowledge.jsonl"), "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def build_structured_md(recs):
    groups = {}
    for r in recs:
        groups.setdefault(r["category"], []).append(r)
    out = ["# grill-me 检索问答对(结构化)\n",
           "> 由 `build_kb.py` 从 `data/*.csv` 生成。每条含检索问句 + 答案 + 出处 + 置信度。\n",
           f"> 共 {len(recs)} 条。置信度:high=可安全引用 / pending=待核 / avoid=误传勿引。\n"]
    for cat, title in CAT_GROUPS.items():
        items = groups.get(cat)
        if not items:
            continue
        out.append(f"\n## {title}\n")
        for r in items:
            out.append(f"**Q: {r['question']}**  _(id={r['id']}, 置信={r['confidence']}, 出处={r['source']})_\n")
            out.append(f"> A: {r['answer']}\n")
    return "\n".join(out)


if __name__ == "__main__":
    recs = to_records()
    terms = load_terms()
    with open(os.path.join(HERE, "语录集.md"), "w", encoding="utf-8") as f:
        f.write(build_quotes_md(recs))
    with open(os.path.join(HERE, "术语集.md"), "w", encoding="utf-8") as f:
        f.write(build_terms_md(terms))
    build_jsonl(recs)
    with open(os.path.join(HERE, "05-structured.md"), "w", encoding="utf-8") as f:
        f.write(build_structured_md(recs))
    print(f"生成完成: 语录集.md + 术语集.md + 05-knowledge.jsonl({len(recs)}条) + 05-structured.md")
