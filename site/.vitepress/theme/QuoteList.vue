<script setup>
import { ref, computed } from 'vue'
import { quotes } from '../../quotes'

const THEME_ORDER = [
  '逻辑层次', '愿景与领导力', '迪士尼策略', '信念',
  '语言魔术 / 回应术', '英雄之旅', '模型仿效 / 系统派 NLP',
  '学习策略', '感知位置', '著作', '常见误传(勿归于迪尔茨)', '待核验'
]

const search = ref('')
const active = ref(new Set())
const showPending = ref(true)
const showAvoid = ref(true)
const copiedId = ref('')

const filtered = computed(() =>
  quotes.filter((q) => {
    if (q.confidence === 'pending' && !showPending.value) return false
    if (q.confidence === 'avoid' && !showAvoid.value) return false
    if (active.value.size && !active.value.has(q.theme)) return false
    const s = search.value.trim().toLowerCase()
    if (s) {
      const hay = (q.zh + q.source + q.topic + q.theme).toLowerCase()
      if (!hay.includes(s)) return false
    }
    return true
  })
)

const themes = computed(() => {
  const present = [...new Set(quotes.map((q) => q.theme))]
  const known = THEME_ORDER.filter((t) => present.includes(t))
  const extra = present.filter((t) => !THEME_ORDER.includes(t)).sort()
  return known.concat(extra)
})

const grouped = computed(() =>
  themes.value
    .map((t) => ({ theme: t, items: filtered.value.filter((q) => q.theme === t) }))
    .filter((g) => g.items.length)
)

const badgeMap = { high: { t: '✅ 可引用', c: 'b-high' }, pending: { t: '⚠️ 待核验', c: 'b-pending' }, avoid: { t: '❓ 误传勿引', c: 'b-avoid' } }

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
    <div class="q-controls">
      <input class="q-search" v-model="search" placeholder="搜索语录 / 出处 / 主题…" />
      <button class="btn" @click="randomOne">随机一条 🎲</button>
      <div class="toggles">
        <label><input type="checkbox" v-model="showPending" /> 待核验</label>
        <label><input type="checkbox" v-model="showAvoid" /> 误传</label>
      </div>
    </div>

    <div class="q-controls" style="margin-top:.6rem">
      <div class="chips">
        <span v-for="t in themes" :key="t" class="chip" :class="{ active: active.has(t) }" @click="toggleTheme(t)">{{ t }}</span>
      </div>
    </div>

    <div v-if="!grouped.length" class="empty">没有匹配的语录,试试调整筛选或搜索词。</div>

    <div v-for="g in grouped" :key="g.theme" class="q-group">
      <h2>{{ g.theme }} <small style="color:var(--ink-soft);font-weight:400">· {{ g.items.length }}</small></h2>
      <div class="q-grid">
        <div v-for="q in g.items" :key="q.id" :id="'q-' + q.id" class="q-card">
          <span class="qm">“</span>
          <div class="body">{{ q.zh }}</div>
          <div class="foot">
            <span class="src">{{ q.source }}</span>
            <span class="badge" :class="badgeMap[q.confidence].c">{{ badgeMap[q.confidence].t }}</span>
          </div>
          <div class="foot" style="margin-top:.5rem">
            <span></span>
            <button class="copy" @click="copy(q)">{{ copiedId === q.id ? '已复制 ✓' : '复制' }}</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
