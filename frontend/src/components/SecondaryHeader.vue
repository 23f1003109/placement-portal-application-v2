<template>
  <div class="secondary-header">
    <h1 class="secondary-header__title">Welcome, {{ displayTitle }}</h1>
    <div class="secondary-header__actions">
      <slot />
      <LogOut @logout="handleLogout" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import LogOut from '@/components/LogOut.vue'

const props = defineProps({
  title: {
    type: String,
    default: 'Admin',
  },
})

const router = useRouter()
const displayTitle = computed(() => props.title || 'Admin')

function handleLogout() {
  router.push('/login')
}
</script>

<style scoped>
.secondary-header__actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
}
</style>
