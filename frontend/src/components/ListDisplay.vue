<template>
  <article class="list_display">
    <div class="list_display-header">
      <h2 class="list_display-title">{{ title }}</h2>
      <div v-if="filterEnabled" class="list_display-form">
        <FilterBar
          :options="options"
          @filter="unpack_payload"
          v-model="query_string"
        />
      </div>
    </div>
    <div class="scroll-wrapper">
      <TableDisplay
        :rows="table.data"
        :columns="table.headers"
        :buttonsPresent="buttonsPresent"
        :buttons="buttons"
      />
    </div>
  </article>
</template>

<script setup>
import FilterBar from '@/components/FilterBar.vue'
import TableDisplay from '@/components/TableDisplay.vue'
import { ref } from 'vue'
import { useAdminDashboardStore } from '@/stores/adminStore.js'

const store = useAdminDashboardStore()
const query_string = ref('')

const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  tableKey: {
    type: String,
    required: true,
  },
  table: {
    type: Object,
    required: true,
  },
  filterEnabled: {
    type: Boolean,
    default: false,
  },
  options: {
    type: Array,
    default: () => [],
  },
  buttons: {
    type: Array,
    default: () => [],
  },
  buttonsPresent: {
    type: Boolean,
    required: true,
  },
  onFilter: {
    type: Function,
    default: null,
  },
})

function unpack_payload(payload) {
  if (!payload.filter_by) {
    return
  }

  const params = new URLSearchParams({ [payload.filter_by]: query_string.value })

  if (typeof props.onFilter === 'function') {
    props.onFilter(params, payload)
    return
  }

  if (props.tableKey === 'approved_companies') {
    store.fetchCompanies(params)
  } else if (props.tableKey === 'registered_student') {
    store.fetchStudents(params)
  }
}
</script>

<style scoped></style>
