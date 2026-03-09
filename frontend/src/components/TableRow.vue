<template>
  <tr class="table_display-item">
    <td
      v-for="column in columns"
      :key="column.key"
      class="row-item"
    >{{ formatCell(row[column.key]) }}</td>
    <td v-if="buttonsPresent" class="row-item row-item__actions">
      <button
        v-for="button in buttons"
        :key="button.key"
        type="button"
        :class="buttonClass(button, row)"
        @click="handleButton(button, row)"
      >
        {{ buttonLabel(button, row) }}
      </button>
    </td>
  </tr>
</template>

<script setup>
defineProps({
  row: {
    type: Object,
    required: true,
  },
  columns: {
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

function buttonClass(button, row) {
  const buttonClassMap = {
    red: 'item__button-red',
    green: 'item__button-green',
    blue: 'item__button-blue',
    cyan: 'item__button-cyan',
  }
  const cls = typeof button.cls === 'function' ? button.cls(row) : button.cls
  return buttonClassMap[cls]
}

function buttonLabel(button, row) {
  return typeof button.label === 'function' ? button.label(row) : button.label
}

function handleButton(button, row) {
  if (typeof button.onClick === 'function') {
    button.onClick(row)
  }
}

function formatCell(value) {
  if (typeof value === 'boolean') {
    return value ? 'Yes' : 'No'
  }

  return value ?? ''
}
</script>

<style scoped></style>
