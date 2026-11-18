<script setup>
import { ref, computed } from 'vue'
import { books } from '../../books'

const search = ref('')
const copiedId = ref('')

const filtered = computed(() => {
  const s = search.value.trim().toLowerCase()
  if (!s) return books
  return books.filter((b) =>
    (b.title + b.title_en + b.intro + b.role + b.year).toLowerCase().includes(s)
  )
})

async function copy(b) {
  try {
    await navigator.clipboard.writeText(`${b.title || b.title_en}(${b.year}) ${b.role}:${b.intro}`)
    copiedId.value = b.id
    setTimeout(() => { if (copiedId.value === b.id) copiedId.value = '' }, 1500)
  } catch (e) {}
}
</script>

<template>
  <div>
    <div class="q-controls">
      <input class="q-search" v-model="search" placeholder="搜索书名 / 简介 / 年份…" />
    </div>

    <div v-if="!filtered.length" class="empty">没有匹配的作品。</div>

    <div class="b-grid">
      <div v-for="b in filtered" :key="b.id" class="b-card">
        <div class="b-top">
          <span class="b-title">{{ b.title || b.title_en }}</span>
          <span class="b-year">{{ b.year }}</span>
        </div>
        <div class="b-en" v-if="b.title_en && b.title">{{ b.title_en }}</div>
        <div class="b-role">{{ b.role }}</div>
        <div class="b-intro">{{ b.intro }}</div>
        <div class="foot">
          <span class="src">{{ b.source }}</span>
          <button class="copy" @click="copy(b)">{{ copiedId === b.id ? '已复制 ✓' : '复制' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>
