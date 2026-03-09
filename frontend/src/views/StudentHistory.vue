<template>
  <SecondaryHeader :title="store.student?.name || 'Student'">
    <router-link to="/student/profile/edit" class="item__button-blue">Edit Profile</router-link>
    <router-link to="/student" class="item__button-green">Dashboard</router-link>
  </SecondaryHeader>

  <ListDisplay
    :title="'Application History'"
    tableKey="student_history"
    :filterEnabled="false"
    :buttonsPresent="true"
    :buttons="historyButtons"
    :options="[]"
    :table="historyTable"
  />
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ListDisplay from '@/components/ListDisplay.vue'
import SecondaryHeader from '@/components/SecondaryHeader.vue'
import { useStudentStore } from '@/stores/studentStore'

const router = useRouter()
const store = useStudentStore()

const historyHeader = [
  { key: 'drive_name', content: 'Drive Name', colspan: 1 },
  { key: 'company_name', content: 'Company', colspan: 1 },
  { key: 'application_date', content: 'Application Date', colspan: 1 },
  { key: 'status', content: 'Status', colspan: 1 },
]

const historyButtons = [
  {
    key: 'view_drive',
    label: 'View Details',
    cls: 'blue',
    onClick: (application) => router.push(`/student/drives/${application.drive_id}`),
  },
]

const historyTable = computed(() => ({
  headers: historyHeader,
  data: store.history,
}))

onMounted(async () => {
  await Promise.all([store.fetchProfile(), store.fetchHistory()])
})
</script>

<style scoped></style>
