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

const badgeMap = { high: { t: '✅ 可引用', c: 'b-high' }, pending: { t: '⚠️ 待核验', c: 'b-pending' }, avoid: { t: '❓ 误传勿引', c: 'b-avoid' } }
const themeCount = new Set(quotes.map((q) => q.theme)).size
</script>

<template>
  <div class="home-quote" v-if="featured">
    <span class="mark">“</span>
    <p class="txt">{{ featured.zh }}</p>
    <div class="meta">
      <span class="badge" :class="badgeMap[featured.confidence].c">{{ badgeMap[featured.confidence].t }}</span>
      &nbsp;出处:<span class="src">{{ featured.source }}</span>
    </div>

    <div class="stats">
      <div><b>{{ quotes.length }}</b>条语录</div>
      <div><b>{{ terms.length }}</b>个术语</div>
      <div><b>{{ themeCount }}</b>个主题</div>
      <div><b>{{ books.length }}</b>部作品</div>
    </div>

    <div class="home-actions">
      <button class="btn primary" @click="pick">换一条 🎲</button>
      <a class="btn" href="./quotes.html">浏览全部语录</a>
      <a class="btn" href="./terms.html">术语集</a>
      <a class="btn" href="./books.html">作品一览</a>
    </div>
  </div>
</template>
