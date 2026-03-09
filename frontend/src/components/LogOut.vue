<template>
  <button @click="logOut" class="item__button-red" :disabled="loading">
    {{ loading ? 'Logging Out' : 'Log Out' }}
  </button>
</template>

<script setup>
import { ref } from 'vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

const emits = defineEmits(['logout'])

const loading = ref(false)

async function logOut() {
  loading.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/auth/logout`, {
      method: 'POST',
      credentials: 'include',
    })
    if (!response.ok) {
      throw new Error('Logout Failed!')
    }
  } catch (error) {
    console.log('Logout failed', error)
  } finally {
    loading.value = false
    emits('logout')
  }
}
</script>

<style scoped></style>
