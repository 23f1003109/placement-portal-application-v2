<template>
  <SecondaryHeader :title="store.currentCompany?.name || 'Company'">
    <router-link to="/student/history" class="item__button-green">View History</router-link>
    <router-link to="/student" class="item__button-blue">Back</router-link>
  </SecondaryHeader>

  <article class="list_display">
    <div class="list_display-header">
      <h2 class="list_display-title">Overview</h2>
    </div>
    <p class="list_display-description">{{ store.currentCompany?.description || 'No description available.' }}</p>
  </article>

  <ListDisplay
    :title="'Current Drives'"
    tableKey="student_company_drives"
    :filterEnabled="false"
    :buttonsPresent="true"
    :buttons="driveButtons"
    :options="[]"
    :table="drivesTable"
  />
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ListDisplay from '@/components/ListDisplay.vue'
import SecondaryHeader from '@/components/SecondaryHeader.vue'
import { useStudentStore } from '@/stores/studentStore'

const route = useRoute()
const router = useRouter()
const store = useStudentStore()

const driveHeader = [
  { key: 'name', content: 'Drive Name', colspan: 1 },
]

const driveButtons = [
  {
    key: 'view_drive',
    label: 'View Details',
    cls: 'blue',
    onClick: (drive) => router.push(`/student/drives/${drive.id}`),
  },
]

const drivesTable = computed(() => ({
  headers: driveHeader,
  data: store.companyDrives,
}))

onMounted(() => {
  store.fetchCompany(route.params.id)
})
</script>

<style scoped></style>
