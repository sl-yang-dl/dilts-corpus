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
    <div class="page-head">
      <h1>术语集</h1>
      <p>NLP 与迪尔茨体系中的关键概念解释,含专有名词与基础概念。</p>
    </div>

    <div class="q-controls">
      <input class="q-search" v-model="search" placeholder="搜索术语 / 英文 / 定义…" />
    </div>

    <div v-if="!filtered.length" class="empty">没有匹配的术语。</div>

    <div class="gloss">
      <div v-for="t in filtered" :key="t.id" class="gloss-row">
        <div class="gloss-term">
          <span class="g-name">{{ t.zh }}</span>
          <span class="g-en">{{ t.en }}</span>
        </div>
        <div class="gloss-def">
          <div class="g-def">{{ t.definition }}</div>
          <div class="g-rel" v-if="t.related"><b>相关:</b>{{ t.related }}</div>
          <div class="g-foot">
            <span class="src">{{ t.source }}</span>
            <button class="copy" @click="copy(t)">{{ copiedId === t.id ? '已复制 ✓' : '复制' }}</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
