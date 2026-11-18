<script setup>
import { ref, computed, onMounted } from 'vue'
import { quotes } from '../../quotes'
import { terms } from '../../terms'
import { books } from '../../books'

const idx = ref(0)
const featured = computed(() => quotes[idx.value])

function pick() {
  if (!quotes.length) return
  let n = idx.value
  while (n === idx.value && quotes.length > 1) {
    n = Math.floor(Math.random() * quotes.length)
  }
  idx.value = n
}
onMounted(pick)

const badgeMap = {
  high: { t: '✅ 可引用', c: 'b-high' },
  pending: { t: '⚠️ 待核验', c: 'b-pending' },
  avoid: { t: '❓ 误传勿引', c: 'b-avoid' }
}
const themeCount = new Set(quotes.map((q) => q.theme)).size
</script>

<template>
  <div class="cover">
    <header class="cover-head">
      <div class="cover-seal">语录</div>
      <h1 class="cover-title">罗伯特·迪尔茨<br />语录集</h1>
      <p class="cover-sub">NLP 先驱的观点、金句与术语 · 按主题归类 · 标注出处与置信度</p>
    </header>

    <figure class="plate" v-if="featured">
      <span class="plate-mark">“</span>
      <blockquote class="plate-text">{{ featured.zh }}</blockquote>
      <figcaption class="plate-meta">
        <span class="badge" :class="badgeMap[featured.confidence].c">{{ badgeMap[featured.confidence].t }}</span>
        <span class="plate-theme">{{ featured.theme }}</span>
        <span class="plate-src">出处:{{ featured.source }}</span>
      </figcaption>
      <button class="plate-btn" @click="pick">换一条 🎲</button>
    </figure>

    <nav class="tiles">
      <a class="tile" href="./quotes.html">
        <span class="tile-t">语录集</span>
        <span class="tile-d">他的观点与金句,按主题归类</span>
        <span class="tile-n">{{ quotes.length }}</span>
      </a>
      <a class="tile" href="./terms.html">
        <span class="tile-t">术语集</span>
        <span class="tile-d">NLP 与迪尔茨专有概念解释</span>
        <span class="tile-n">{{ terms.length }}</span>
      </a>
      <a class="tile" href="./books.html">
        <span class="tile-t">作品集</span>
        <span class="tile-d">所有著作一览与简介</span>
        <span class="tile-n">{{ books.length }}</span>
      </a>
      <a class="tile" href="./about.html">
        <span class="tile-t">关于</span>
        <span class="tile-d">罗伯特·迪尔茨生平</span>
        <span class="tile-n">›</span>
      </a>
    </nav>

    <div class="cover-stats">
      <div><b>{{ quotes.length }}</b>条语录</div>
      <div><b>{{ terms.length }}</b>个术语</div>
      <div><b>{{ books.length }}</b>部作品</div>
      <div><b>{{ themeCount }}</b>个主题</div>
    </div>
  </div>
</template>
