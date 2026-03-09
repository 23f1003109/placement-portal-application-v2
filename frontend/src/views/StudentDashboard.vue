<template>
  <SecondaryHeader :title="store.student?.name || 'Student'">
    <router-link to="/student/profile/edit" class="item__button-blue">Edit Profile</router-link>
    <router-link to="/student/history" class="item__button-green">View History</router-link>
  </SecondaryHeader>

  <ListDisplay
    :title="'Organizations'"
    tableKey="student_companies"
    :filterEnabled="false"
    :buttonsPresent="true"
    :buttons="companyButtons"
    :options="[]"
    :table="companiesTable"
  />

  <ListDisplay
    :title="'Applied Drives'"
    tableKey="student_applications"
    :filterEnabled="false"
    :buttonsPresent="true"
    :buttons="applicationButtons"
    :options="[]"
    :table="applicationsTable"
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

const companyHeader = [
  { key: 'name', content: 'Organization', colspan: 1 },
]

const applicationHeader = [
  { key: 'drive_id', content: 'Serial No.', colspan: 1 },
  { key: 'drive_name', content: 'Drive Name', colspan: 1 },
  { key: 'company_name', content: 'Company', colspan: 1 },
  { key: 'application_date', content: 'Date', colspan: 1 },
]

const companyButtons = [
  {
    key: 'view_company',
    label: 'View Details',
    cls: 'blue',
    onClick: (company) => router.push(`/student/companies/${company.id}`),
  },
]

const applicationButtons = [
  {
    key: 'view_drive',
    label: 'View Details',
    cls: 'blue',
    onClick: (application) => router.push(`/student/drives/${application.drive_id}`),
  },
]

const companiesTable = computed(() => ({
  headers: companyHeader,
  data: store.companies,
}))

const applicationsTable = computed(() => ({
  headers: applicationHeader,
  data: store.appliedApplications,
}))

onMounted(() => {
  store.fetchDashboard()
})
</script>

<style scoped></style>
