<script setup>
import { ref, computed, onMounted, nextTick, onUnmounted } from 'vue'
import { onSlideEnter, useSlideContext } from '@slidev/client'

// Movie-style scrolling credits, adapted from slidev-theme-neversink's
// `credits` layout so it works on the default theme used by this deck.
const props = defineProps({
  color: { default: 'navy' },
  speed: { type: Number, default: 1.0 },
  loop: { type: Boolean, default: false },
})

const { $renderContext } = useSlideContext()
const scrollPosition = ref(480)
let animationFrameId = null

// When exporting to PDF the scroll animation never runs, so the content would
// stay frozen off-screen. Instead, lay it out statically and scale it down to
// fit the slide height so every name is visible in the PDF. Detect the export
// render from the URL (Slidev exports via the .../print route).
const isPrint = ref(false)
const scrollRef = ref(null)
const contentRef = ref(null)
const printScale = ref(1)

onMounted(async () => {
  isPrint.value = /\/print(\b|\/|$)|[?&]print\b|\/export\b/.test(
    location.pathname + location.search,
  )
  if (!isPrint.value) return
  await nextTick()
  const content = contentRef.value
  const container = scrollRef.value
  if (!content || !container) return
  const contentH = content.scrollHeight
  const containerH = container.clientHeight
  if (contentH > containerH) printScale.value = (containerH / contentH) * 0.96
})

const contentStyle = computed(() =>
  isPrint.value
    ? { position: 'static', transform: `scale(${printScale.value})`, transformOrigin: 'top center' }
    : { transform: `translateY(${scrollPosition.value}px)` },
)

const scroll = () => {
  scrollPosition.value -= props.speed
  if (Math.abs(scrollPosition.value) >= 550) {
    if (props.loop) {
      resetScroll()
      animationFrameId = requestAnimationFrame(scroll)
    } else {
      stopScrolling()
    }
  } else {
    animationFrameId = requestAnimationFrame(scroll)
  }
}

const startScrolling = () => {
  animationFrameId = requestAnimationFrame(scroll)
}

const stopScrolling = () => {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId)
    animationFrameId = null
  }
}

const resetScroll = () => {
  scrollPosition.value = 480
  stopScrolling()
}

onSlideEnter(() => {
  if (!isPrint.value && ['slide', 'presenter'].includes($renderContext.value)) {
    resetScroll()
    startScrolling()
  }
})

onUnmounted(() => {
  stopScrolling()
})
</script>

<template>
  <div class="slidev-layout dx-credits" :class="[`dx-credits-${props.color}`, { 'dx-credits-print': isPrint }]">
    <div ref="scrollRef" class="dx-credits-scroll">
      <div
        ref="contentRef"
        class="dx-credits-content"
        :style="contentStyle"
      >
        <slot />
      </div>
    </div>
  </div>
</template>

<style scoped>
.dx-credits {
  height: 100%;
  padding: 0;
  display: flex;
  align-items: stretch;
}
.dx-credits-navy {
  background: var(--dx-ink, #16222c);
  color: #eef3f6;
}
.dx-credits-scroll {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}
.dx-credits-content {
  position: absolute;
  width: 100%;
}
.dx-credits-content :deep(i) {
  color: var(--dx-blue-light, #6db3e8);
}
.dx-credits-content :deep(strong) {
  color: #ffffff;
}

/* Static, fit-to-slide rendering when exporting to PDF */
.dx-credits-print .dx-credits-scroll {
  display: flex;
  justify-content: center;
  align-items: flex-start;
}
.dx-credits-print .dx-credits-content {
  padding-top: 2.5rem;
}
/* the large scroll spacer before "Questions?" is only needed for the animation */
.dx-credits-print .dx-credits-content :deep(.mt-180px) {
  margin-top: 2.5rem !important;
}
</style>
