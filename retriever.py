# -*- coding: utf-8 -*-
"""
dilts-corpus 最小检索原型(零依赖,仅 numpy)。

功能:
  1. 加载 05-knowledge.jsonl(29 条迪尔茨语料)
  2. 用 TF-IDF + 余弦相似度做本地检索(中文按「字 + 二元字组」切分)
  3. 把命中的 top-k 记录格式化为 grill-me / LLM 的上下文

这是「嵌入 + 向量检索」的可运行雏形。将来联网后,只需替换 embed()
为 sentence-transformers / OpenAI 等真实句向量,其余流程不变。

用法:
  python3 retriever.py "迪尔茨的逻辑层次是什么"
  python3 retriever.py --json "地图不是疆域 是谁说的"
  (无参数则跑内置 demo)
"""
import os, re, json, sys, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
JSONL = os.path.join(HERE, "05-knowledge.jsonl")

# ---------- 文本处理 ----------
CJK = re.compile(r'[\u4e00-\u9fff]')

def tokenize(text):
    """混合中英文分词:英文按词,中文按「单字 + 相邻二元字组」。"""
    text = text.lower()
    tokens = []
    # 英文/数字词
    for m in re.findall(r'[a-z0-9]+', text):
        if len(m) >= 2:
            tokens.append(m)
    # 中文片段:单字 + bigram
    for seg in re.findall(r'[\u4e00-\u9fff]+', text):
        for ch in seg:
            tokens.append(ch)
        for i in range(len(seg) - 1):
            tokens.append(seg[i:i+2])
    return tokens

def load_records(path=JSONL):
    with open(path, encoding='utf-8') as f:
        return [json.loads(l) for l in f if l.strip()]

# ---------- 可替换的嵌入函数 ----------
def embed(text, vocab=None, idf=None):
    """
    默认:TF-IDF 词袋向量(零依赖)。
    升级路径(联网后):
        from sentence_transformers import SentenceTransformer
        _m = SentenceTransformer('shibing624/text2vec-base-chinese')
        def embed(text, *a, **k): return _m.encode(text)   # 直接返回句向量
    其余检索逻辑无需改动。
    """
    if vocab is None:
        raise ValueError("TF-IDF 模式需先 build_index()")
    vec = np.zeros(len(vocab), dtype=np.float32)
    toks = tokenize(text)
    n = len(toks) or 1
    for t in toks:
        if t in vocab:
            vec[vocab[t]] += 1.0 / n          # 词频归一
    if idf is not None:
        vec = vec * idf
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec /= norm
    return vec

# ---------- 索引 ----------
class Retriever:
    def __init__(self, records):
        self.records = records
        docs = [f"{r['topic']} {r['question']} {r['answer']}" for r in records]
        toks_list = [tokenize(d) for d in docs]
        vocab = {}
        df = {}
        for toks in toks_list:
            for t in set(toks):
                df[t] = df.get(t, 0) + 1
                if t not in vocab:
                    vocab[t] = len(vocab)
        N = len(docs)
        idf = np.array([math.log((N + 1) / (df[t] + 1)) + 1 for t in vocab], dtype=np.float32)
        # 文档矩阵(N x V),每行已是 L2 归一化的 tf-idf
        self.vocab = vocab
        self.idf = idf
        self.matrix = np.stack([embed(d, vocab, idf) for d in docs])

    def retrieve(self, query, k=3):
        q = embed(query, self.vocab, self.idf)
        sims = self.matrix @ q            # 已归一化 -> 余弦
        idx = np.argsort(-sims)[:k]
        out = []
        for i in idx:
            if sims[i] <= 0:
                continue
            r = dict(self.records[i])
            r['_score'] = round(float(sims[i]), 4)
            out.append(r)
        return out

# ---------- 给 grill-me / LLM 的上下文 ----------
CONF_HINT = {
    'high': '可直接引用',
    'pending': '引用时须注明「出处待核」',
    'avoid': '这是常见误传,应主动纠正归因,不要当作迪尔茨原话',
}

def build_context(results):
    lines = ["以下是与用户问题相关的迪尔茨语料(按相关度排序):", ""]
    for i, r in enumerate(results, 1):
        hint = CONF_HINT.get(r['confidence'], '')
        lines.append(f"[{i}] (置信={r['confidence']}·{hint}·来源={r['source']})")
        lines.append(f"问:{r['question']}")
        lines.append(f"答:{r['answer']}")
        lines.append("")
    return "\n".join(lines)

def build_prompt(query, k=3):
    ret = Retriever(load_records())
    results = ret.retrieve(query, k=k)
    ctx = build_context(results)
    sys_prompt = (
        "你是 grill-me,基于给定语料回答罗伯特·迪尔茨相关的问题。"
        "只使用下方语料,不要编造;按每条的「置信」标注决定引用方式。"
    )
    return {
        "system": sys_prompt,
        "context": ctx,
        "user": query,
        "results": results,
    }

# ---------- CLI ----------
def demo():
    for q in ["迪尔茨的逻辑层次是什么",
              "地图不是疆域 是谁说的",
              "如果你总是做你一直在做的事"]:
        print("="*60)
        print("查询:", q)
        p = build_prompt(q, k=2)
        for r in p['results']:
            print(f"  · [{r['_score']}] ({r['confidence']}) {r['question']}")
        print()

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        demo()
    else:
        as_json = '--json' in args
        q = " ".join(a for a in args if a != '--json')
        p = build_prompt(q, k=3)
        if as_json:
            print(json.dumps(p['results'], ensure_ascii=False, indent=2))
        else:
            print(p['context'])
