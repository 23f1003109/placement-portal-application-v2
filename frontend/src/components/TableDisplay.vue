<template>
  <table class="table_display-items">
    <TableHeader
      v-if="columns.length"
      :headers="columns"
      :buttonsPresent="buttonsPresent"
      :buttons="buttons"
    />
    <TableBody
      :rows="rows"
      :columns="columns"
      :buttonsPresent="buttonsPresent"
      :buttons="buttons"
    />
  </table>
</template>

<script setup>
import TableBody from '@/components/TableBody.vue'
import TableHeader from '@/components/TableHeader.vue'

defineProps({
  columns: {
    type: Array,
    required: true,
  },
  rows: {
    type: Array,
    required: true,
  },
  buttons: {
    type: Array,
    default: () => [],
  },
  buttonsPresent: {
    type: Boolean,
    required: true,
  },
})
</script>

<style scoped></style>
