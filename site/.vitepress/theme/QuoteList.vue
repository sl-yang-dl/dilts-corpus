<script setup>
import { ref, computed } from 'vue'
import { quotes } from '../../quotes'

const search = ref('')
const active = ref(new Set())
const showPending = ref(true)
const showAvoid = ref(true)
const copiedId = ref('')

const themes = computed(() => [...new Set(quotes.map((q) => q.theme))])
const filtered = computed(() => {
  const s = search.value.trim().toLowerCase()
  return quotes.filter((q) => {
    if (!showPending.value && q.confidence === 'pending') return false
    if (!showAvoid.value && q.confidence === 'avoid') return false
    if (active.value.size && !active.value.has(q.theme)) return false
    if (!s) return true
    return (q.zh + q.source + q.theme).toLowerCase().includes(s)
  })
})

const grouped = computed(() =>
  themes.value
    .map((t) => ({ theme: t, items: filtered.value.filter((q) => q.theme === t) }))
    .filter((g) => g.items.length)
)

const badgeMap = {
  high: { t: '✅ 可引用', c: 'b-high' },
  pending: { t: '⚠️ 待核验', c: 'b-pending' },
  avoid: { t: '❓ 误传勿引', c: 'b-avoid' }
}

function toggleTheme(t) {
  const n = new Set(active.value)
  n.has(t) ? n.delete(t) : n.add(t)
  active.value = n
}

function randomOne() {
  const arr = filtered.value
  if (!arr.length) return
  const q = arr[Math.floor(Math.random() * arr.length)]
  const el = document.getElementById('q-' + q.id)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'center' })
    el.classList.add('flash')
    setTimeout(() => el.classList.remove('flash'), 1200)
  }
}

async function copy(q) {
  try {
    await navigator.clipboard.writeText(`「${q.zh}」——${q.source}`)
    copiedId.value = q.id
    setTimeout(() => { if (copiedId.value === q.id) copiedId.value = '' }, 1500)
  } catch (e) {}
}
</script>

<template>
  <div>
    <div class="page-head">
      <h1>语录集</h1>
      <p>罗伯特·迪尔茨的观点与金句,按主题归类;每条标注出处与置信度。</p>
    </div>

    <div class="q-bar">
      <input class="q-search" v-model="search" placeholder="搜索语录 / 出处 / 主题…" />
      <button class="btn primary" @click="randomOne">🎲 随机一条</button>
    </div>

    <div class="q-controls" style="margin-top:.8rem">
      <div class="chips">
        <span v-for="t in themes" :key="t" class="chip" :class="{ active: active.has(t) }" @click="toggleTheme(t)">{{ t }}</span>
      </div>
      <div class="toggles">
        <label><input type="checkbox" v-model="showPending" /> 待核验</label>
        <label><input type="checkbox" v-model="showAvoid" /> 误传</label>
      </div>
    </div>

    <div v-if="!grouped.length" class="empty">没有匹配的语录,试试调整筛选或搜索词。</div>

    <div v-for="g in grouped" :key="g.theme" class="q-group">
      <h2>{{ g.theme }} <small style="color:var(--ink-soft);font-weight:400">· {{ g.items.length }}</small></h2>
      <div class="q-grid">
        <div v-for="q in g.items" :key="q.id" :id="'q-' + q.id" class="q-card">
          <span class="qm">“</span>
          <p class="body">{{ q.zh }}</p>
          <div class="card-meta" v-if="q.date || q.occasion || q.added">
            <span v-if="q.date">📅 {{ q.date }}</span>
            <span v-if="q.occasion">· 场合:{{ q.occasion }}</span>
            <span v-if="q.added">· 📥 收录 {{ q.added }}</span>
          </div>
          <div class="card-foot">
            <div class="src">
              <span class="theme-tag">{{ q.theme }}</span>
              <span class="src-text">{{ q.source }}</span>
            </div>
            <span class="badge" :class="badgeMap[q.confidence].c">{{ badgeMap[q.confidence].t }}</span>
          </div>
          <div class="card-actions">
            <button class="copy" @click="copy(q)">{{ copiedId === q.id ? '已复制 ✓' : '复制金句' }}</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
