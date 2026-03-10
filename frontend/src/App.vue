<template>
  <div class="container">
    <Navbar />
    <router-view />
  </div>
</template>

<script setup>
import { onBeforeUnmount, watch } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from './components/Navbar.vue'
import fullPageStylesheetHref from '@/assets/css/full-page.css?url'
import miniPageStylesheetHref from '@/assets/css/mini-page.css?url'

const route = useRoute()
const layoutStylesheetId = 'layout-stylesheet'

function getLayoutStylesheetHref(layout) {
  return layout === 'mini' ? miniPageStylesheetHref : fullPageStylesheetHref
}

function attachLayoutStylesheet(layout) {
  const stylesheetHref = getLayoutStylesheetHref(layout)
  let stylesheetLink = document.getElementById(layoutStylesheetId)

  if (!(stylesheetLink instanceof HTMLLinkElement)) {
    stylesheetLink = document.createElement('link')
    stylesheetLink.id = layoutStylesheetId
    stylesheetLink.rel = 'stylesheet'
    document.head.appendChild(stylesheetLink)
  }

  if (stylesheetLink.href !== stylesheetHref) {
    stylesheetLink.href = stylesheetHref
  }
}

watch(
  () => route.meta.layout,
  (layout) => attachLayoutStylesheet(layout || 'full'),
  { immediate: true },
)

onBeforeUnmount(() => {
  document.getElementById(layoutStylesheetId)?.remove()
})
</script>

<style scoped></style>
