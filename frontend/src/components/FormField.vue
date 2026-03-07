<template>
  <div class="form__field">
    <label :for="id" class="form__field-label">{{ label }}</label>
    <input :type="type" class="form__field-input" :id="id" v-model="model" />
    <div v-for="error in errors" :key="error" class="form__field-error">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
const model = defineModel();

defineProps({
    id: String,
    label: String,
    type: {
      type: String,
      default: 'text',
    },
    errors: {
      type: Array,
      default: () => [],
    }
})
</script>

<style scoped></style>
