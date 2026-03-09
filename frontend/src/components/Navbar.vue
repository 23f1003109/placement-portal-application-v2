<template>
  <header class="navbar">
    <div class="navbar__brand">
      <router-link class="navbar__brand-logo_container navbar-link" :to="brandLink">
        <Logo />
      </router-link>

      <router-link class="navbar__brand-name navbar-link" :to="brandLink"> iPlaced! </router-link>
    </div>
  </header>
</template>

<script setup>
import Logo from '../components/Logo.vue'

const brandLink = '/'
</script>

<style></style>
