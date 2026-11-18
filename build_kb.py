# -*- coding: utf-8 -*-
"""
语录集生成器(单一数据源 = data/*.csv)

- data/quotes.csv : 语录/观点/模型/误传(每条可带 date、occasion 元信息)
- data/terms.csv  : 术语(解释性)
- data/books.csv  : 作品集(所有作品一览 + 简介)

产出:
- 语录集.md         人类可读的语录墙正文
- 术语集.md         术语解释
- 05-knowledge.jsonl  给 grill-me 检索用的结构化记录(语录+术语+作品)
- 05-structured.md    按类别分组的结构化整理

用法:  python3 build_kb.py
"""
import csv, json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, 'data')


def load(name):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        print(f'[warn] 缺少 {name},跳过', file=sys.stderr)
        return []
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def to_records():
    recs = []
    for q in load('quotes.csv'):
        recs.append({
            'id': q['id'],
            'category': q['category'],
            'theme': q['theme'],
            'topic': q.get('topic', ''),
            'question': q['zh'],
            'answer': q['zh'],
            'source': q['source'],
            'confidence': q['confidence'],
            'date': q.get('date', ''),
            'occasion': q.get('occasion', ''),
        })
    for t in load('terms.csv'):
        recs.append({
            'id': t['id'],
            'category': 'term',
            'theme': '术语',
            'topic': t['zh'],
            'question': f"{t['zh']}({t['en']}) 是什么?",
            'answer': t['definition'],
            'source': t['source'],
            'confidence': t['confidence'],
            'date': '', 'occasion': '',
        })
    for b in load('books.csv'):
        recs.append({
            'id': b['id'],
            'category': 'book',
            'theme': '著作',
            'topic': b['title'] or b['title_en'],
            'question': f"{b['title'] or b['title_en']} 讲什么?",
            'answer': b['intro'],
            'source': b['source'],
            'confidence': b['confidence'],
            'date': '', 'occasion': '',
        })
    return recs


def build_quotes_md(recs):
    lines = ['# 罗伯特·迪尔茨语录集', '',
             '> 按主题归类;每条标注出处与置信度。',
             '> 置信度:✅ 可引用 / ⚠️ 待核验 / ❓ 误传勿引。', '']
    groups = {}
    for r in recs:
        if r['category'] in ('term', 'book'):
            continue
        groups.setdefault(r['theme'], []).append(r)
    for theme, items in groups.items():
        lines += ['## ' + theme, '']
        for r in items:
            badge = {'high': '✅', 'pending': '⚠️', 'avoid': '❓'}.get(r['confidence'], '')
            meta = ''
            if r['date'] or r['occasion']:
                parts = []
                if r['date']:
                    parts.append(f"📅 {r['date']}")
                if r['occasion']:
                    parts.append(f"场合:{r['occasion']}")
                meta = '  _(' + ' · '.join(parts) + ')_'
            lines.append(f"- {badge} {r['question']}  —— 出处:{r['source']}{meta}")
        lines.append('')
    return '\n'.join(lines)


def build_terms_md(terms):
    lines = ['# 术语集', '',
             '> 解释迪尔茨体系中的关键概念(含 NLP 基础概念)。', '']
    for t in terms:
        lines.append(f"## {t['zh']} / {t['en']}")
        lines.append('')
        lines.append(t['definition'])
        extra = []
        if t.get('related'):
            extra.append(f"**相关:** {t['related']}")
        if t.get('source'):
            extra.append(f"**出处:** {t['source']}")
        if extra:
            lines.append('')
            lines.append('  ' + '  '.join(extra))
        lines.append('')
    return '\n'.join(lines)


def build_jsonl(recs):
    out = []
    for r in recs:
        out.append(json.dumps({
            'id': r['id'],
            'category': r['category'],
            'theme': r['theme'],
            'topic': r['topic'],
            'question': r['question'],
            'answer': r['answer'],
            'source': r['source'],
            'confidence': r['confidence'],
            'date': r.get('date', ''),
            'occasion': r.get('occasion', ''),
        }, ensure_ascii=False))
    return '\n'.join(out)


CAT_GROUPS = [
    ('quote', '一、语录与观点'),
    ('quote_pending', '二、待核验语录'),
    ('model', '三、模型与框架'),
    ('excerpt', '四、有出处的摘录'),
    ('term', '五、术语'),
    ('book', '六、著作与内容'),
    ('avoid', '七、常见误传(勿归于迪尔茨)'),
]


def build_structured_md(recs):
    lines = ['# 结构化整理', '']
    by_cat = {}
    for r in recs:
        by_cat.setdefault(r['category'], []).append(r)
    for cat, title in CAT_GROUPS:
        items = by_cat.get(cat, [])
        if not items:
            continue
        lines += [f'## {title}', '']
        for r in items:
            head = f"[{r['theme']}] {r['question']}"
            lines.append(f"- {head}")
            lines.append(f"  - 答:{r['answer']}")
            lines.append(f"  - 出处:{r['source']}  置信度:{r['confidence']}")
            if r.get('date') or r.get('occasion'):
                m = ' · '.join(x for x in [r.get('date', ''), r.get('occasion', '')] if x)
                lines.append(f"  - 元信息:{m}")
        lines.append('')
    return '\n'.join(lines)


def main():
    recs = to_records()
    terms = load('terms.csv')
    os.makedirs(ROOT, exist_ok=True)
    with open(os.path.join(ROOT, '语录集.md'), 'w', encoding='utf-8') as f:
        f.write(build_quotes_md(recs))
    with open(os.path.join(ROOT, '术语集.md'), 'w', encoding='utf-8') as f:
        f.write(build_terms_md(terms))
    with open(os.path.join(ROOT, '05-knowledge.jsonl'), 'w', encoding='utf-8') as f:
        f.write(build_jsonl(recs))
    with open(os.path.join(ROOT, '05-structured.md'), 'w', encoding='utf-8') as f:
        f.write(build_structured_md(recs))

    n_book = sum(1 for r in recs if r['category'] == 'book')
    n_term = sum(1 for r in recs if r['category'] == 'term')
    n_q = sum(1 for r in recs if r['category'] not in ('term', 'book'))
    print(f'[ok] 语录/观点 {n_q} 条 + 术语 {n_term} 条 + 作品 {n_book} 部 → '
          f'语录集.md / 术语集.md / 05-knowledge.jsonl / 05-structured.md')


if __name__ == '__main__':
    main()
