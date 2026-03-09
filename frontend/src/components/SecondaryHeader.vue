<template>
  <div class="secondary-header">
    <h1 class="secondary-header__title">Welcome, {{ name }}</h1>
    <LogOut @logout="handleLogout" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import LogOut from '@/components/LogOut.vue'

const router = useRouter()

const name = ref('Admin')

function handleLogout() {
  router.push('/login')
}
</script>

<style scoped></style>
