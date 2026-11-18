<script setup>
import { ref, computed } from 'vue'
import { terms } from '../../terms'

const search = ref('')
const copiedId = ref('')

const filtered = computed(() => {
  const s = search.value.trim().toLowerCase()
  if (!s) return terms
  return terms.filter((t) =>
    (t.zh + t.en + t.definition + t.related + t.source).toLowerCase().includes(s)
  )
})

async function copy(t) {
  try {
    await navigator.clipboard.writeText(`${t.zh} / ${t.en}:${t.definition}`)
    copiedId.value = t.id
    setTimeout(() => { if (copiedId.value === t.id) copiedId.value = '' }, 1500)
  } catch (e) {}
}
</script>

<template>
  <div>
    <div class="q-controls">
      <input class="q-search" v-model="search" placeholder="搜索术语 / 英文 / 定义…" />
    </div>

    <div v-if="!filtered.length" class="empty">没有匹配的术语。</div>

    <div class="t-grid">
      <div v-for="t in filtered" :key="t.id" class="t-card">
        <div><span class="name">{{ t.zh }}</span><span class="en">{{ t.en }}</span></div>
        <div class="def">{{ t.definition }}</div>
        <div class="rel" v-if="t.related"><b>相关:</b>{{ t.related }}</div>
        <div class="foot">
          <span class="src">{{ t.source }}</span>
          <button class="copy" @click="copy(t)">{{ copiedId === t.id ? '已复制 ✓' : '复制' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>
