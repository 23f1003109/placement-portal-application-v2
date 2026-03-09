<template>
  <tbody>
    <TableRow
      v-for="(row, index) in rows"
      :key="row.id ?? index"
      :row="row"
      :columns="columns"
      :buttonsPresent="buttonsPresent"
      :buttons="buttons"
    />
  </tbody>
</template>

<script setup>
import TableRow from '@/components/TableRow.vue'

defineProps({
  rows: {
    type: Array,
    required: true,
  },
  columns: {
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
