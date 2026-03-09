<template>
  <div class="form__field">
    <label :for="id" class="form__field-label">{{ label }}</label>
    <textarea
      v-if="as === 'textarea'"
      :id="id"
      :rows="rows"
      class="form__field-input form__field-input--textarea"
      :placeholder="placeholder"
      v-model="model"
    />
    <select
      v-else-if="as === 'select'"
      :id="id"
      class="form__field-input"
      v-model="model"
    >
      <option v-for="option in options" :key="option.value" :value="option.value">
        {{ option.label }}
      </option>
    </select>
    <input
      v-else
      :type="type"
      class="form__field-input"
      :id="id"
      :placeholder="placeholder"
      v-model="model"
    />
    <div v-for="error in errors" :key="error" class="form__field-error">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
const model = defineModel()

defineProps({
  id: String,
  label: String,
  type: {
    type: String,
    default: 'text',
  },
  as: {
    type: String,
    default: 'input',
  },
  rows: {
    type: Number,
    default: 4,
  },
  placeholder: {
    type: String,
    default: '',
  },
  options: {
    type: Array,
    default: () => [],
  },
  errors: {
    type: Array,
    default: () => [],
  },
})
</script>

<style scoped>
.form__field-input--textarea {
  min-height: 7rem;
  resize: vertical;
  padding-top: 0.75rem;
}
</style>
