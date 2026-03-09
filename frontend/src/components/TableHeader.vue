<template>
  <thead class="table_head">
    <tr class="table_display-item">
      <th class="row-item" v-for="header in headers" :key="header.key" :colspan="header.colspan">
        {{ header.content }}
      </th>
      <th class="row-item" v-if="buttonsPresent" :colspan="buttons.length">Actions</th>
    </tr>
  </thead>
</template>

<script setup>
defineProps({
  headers: {
    type: Array,
    required: true,
  },
  buttonsPresent: {
    type: Boolean,
    default: false,
  },
  buttons: {
    type: Array,
    default: () => [],
  },
})
</script>

<style scoped></style>
