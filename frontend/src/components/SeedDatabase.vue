<template>
  <div>Seeding database...</div>
</template>

<script setup>
import { onMounted } from 'vue'
import router from '@/router'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

onMounted(async () => {
  const res = await fetch(`${API_BASE_URL}/admin/seed`, {
    method: 'POST',
    credentials: 'include',
  })

  if (res.ok) {
    router.replace('/admin')
  } else {
    alert('Seeding failed')
  }
})
</script>
