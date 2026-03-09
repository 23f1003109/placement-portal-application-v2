<template>
  <div class="container">
    <Navbar />
    <router-view />
  </div>
</template>

<script setup>
import { watch } from 'vue'
import { useRoute} from 'vue-router'
import Navbar from "./components/Navbar.vue";

const route = useRoute();
function loadLayout(layout) {
  const existing = document.getElementById('layout-style');
  if (existing) {
    existing.remove();
  }
  const link = document.createElement('link')
  link.id = 'layout-style'
  link.rel = 'stylesheet'
  link.href = layout === 'mini'
    ? '/src/assets/css/mini-page.css'
    : '/src/assets/css/full-page.css'

  document.head.appendChild(link)
}

watch(
  () => route.meta.layout,
  (layout) => loadLayout(layout || 'full'),
  { immediate: true }
)
</script>

<style scoped></style>
