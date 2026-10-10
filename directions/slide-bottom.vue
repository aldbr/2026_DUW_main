<script setup lang="ts">
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'

// Rendered once per slide (inside each slide container), so it appears on
// every page when exporting to PDF — unlike global-bottom.vue, which renders
// only once for the whole deck.
const { $page, $frontmatter } = useSlideContext()

// layouts that should NOT carry the footer
const bare = ['cover', 'section', 'center', 'end', 'intro', 'credits']

const showFooter = computed(() => {
  if ($page.value === 1) return false // title slide
  const layout = $frontmatter?.layout ?? 'default'
  return !bare.includes(layout)
})

const page = computed(() => String($page.value).padStart(2, '0'))
</script>

<template>
  <footer v-if="showFooter" class="dx-footer">
    <span class="dx-footer-meta">
      DiracX developments: directions · DUW 12 · alexandre.boyer@cern.ch
      <img class="dx-footer-logo" src="/logos/diracx-square.svg" alt="DiracX" />
    </span>
    <span class="dx-footer-page">{{ page }}</span>
  </footer>
</template>
