<script setup>
import { bio } from '../../bio'
</script>

<template>
  <div class="bio">
    <header class="bio-hero">
      <h1 class="bio-name">{{ bio.name }}</h1>
      <div class="bio-en">{{ bio.en }} · {{ bio.life }}</div>
      <div class="bio-roles">
        <span v-for="r in bio.roles" :key="r" class="bio-role">{{ r }}</span>
      </div>
      <p class="bio-tag">{{ bio.tagline }}</p>
    </header>

    <section class="bio-block">
      <h2 class="bio-h">生平轨迹</h2>
      <ol class="timeline">
        <li v-for="(t, i) in bio.timeline" :key="i" class="tl-item">
          <div class="tl-year">{{ t.year }}</div>
          <div class="tl-body">
            <div class="tl-title">{{ t.title }}</div>
            <div class="tl-desc">{{ t.desc }}</div>
          </div>
        </li>
      </ol>
    </section>

    <section class="bio-block">
      <h2 class="bio-h">主要贡献与方法</h2>
      <div class="chips">
        <span v-for="c in bio.contributions" :key="c" class="chip">{{ c }}</span>
      </div>
    </section>

    <section class="bio-block">
      <h2 class="bio-h">教学与机构</h2>
      <p class="bio-p">{{ bio.institution }}</p>
      <p class="bio-p">{{ bio.worksNote }}</p>
    </section>

    <section class="bio-block">
      <div class="bio-note">ⓘ {{ bio.note }}</div>
    </section>
  </div>
</template>
