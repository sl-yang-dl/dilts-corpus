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

// 按「是否译本」分为两组,英文原著在前,中文译本在后
const originals = computed(() => filtered.value.filter((b) => !b.role.includes('译')))
const translations = computed(() => filtered.value.filter((b) => b.role.includes('译')))

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
    <div class="page-head">
      <h1>作品集</h1>
      <p>罗伯特·迪尔茨所有著作一览与简介,分英文原著与中文译本。</p>
    </div>

    <div class="q-controls">
      <input class="q-search" v-model="search" placeholder="搜索书名 / 简介 / 年份…" />
    </div>

    <div v-if="!filtered.length" class="empty">没有匹配的作品。</div>

    <template v-if="originals.length">
      <h2 class="bk-h">英文原著</h2>
      <div class="bk-list">
        <div v-for="b in originals" :key="b.id" class="bk-row">
          <div class="bk-year">{{ b.year }}</div>
          <div class="bk-main">
            <div class="bk-title">{{ b.title || b.title_en }}</div>
            <div class="bk-en" v-if="b.title_en && b.title">{{ b.title_en }}</div>
            <div class="bk-role">{{ b.role }}</div>
            <div class="bk-intro">{{ b.intro }}</div>
          </div>
          <button class="copy" @click="copy(b)">{{ copiedId === b.id ? '已复制 ✓' : '复制' }}</button>
        </div>
      </div>
    </template>

    <template v-if="translations.length">
      <h2 class="bk-h">中文译本</h2>
      <div class="bk-list">
        <div v-for="b in translations" :key="b.id" class="bk-row">
          <div class="bk-year">{{ b.year }}</div>
          <div class="bk-main">
            <div class="bk-title">{{ b.title || b.title_en }}</div>
            <div class="bk-en" v-if="b.title_en && b.title">{{ b.title_en }}</div>
            <div class="bk-role">{{ b.role }}</div>
            <div class="bk-intro">{{ b.intro }}</div>
          </div>
          <button class="copy" @click="copy(b)">{{ copiedId === b.id ? '已复制 ✓' : '复制' }}</button>
        </div>
      </div>
    </template>
  </div>
</template>
