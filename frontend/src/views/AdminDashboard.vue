<template>
  <SecondaryHeader />
  <ListDisplay
    v-for="tableItem in tableItems"
    :key="tableItem.key"
    :title="tableItem.title"
    :tableKey="tableItem.key"
    :filterEnabled="tableItem.filter_enabled"
    :buttonsPresent="tableItem.buttons_present"
    :buttons="tableItem.buttons"
    :options="tableItem.options"
    :table="tableItem.table"
  />
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ListDisplay from '@/components/ListDisplay.vue'
import SecondaryHeader from '@/components/SecondaryHeader.vue'
import { useAdminDashboardStore } from '@/stores/adminStore.js'

const router = useRouter()
const store = useAdminDashboardStore()

onMounted(() => {
  store.loadDashboard()
})

function viewButton(entityType) {
  return {
    key: `view_${entityType}`,
    label: 'View Details',
    cls: 'blue',
    onClick: (entity) => router.push(`/admin/${entityType}/${entity.id}`),
  }
}

const tableItems = computed(() => [
  {
    key: 'approved_companies',
    title: 'Approved Companies',
    filter_enabled: true,
    buttons_present: true,
    buttons: [
      viewButton('companies'),
      {
        key: 'toggle_company',
        label: (company) => (company.is_blacklisted ? 'Unblacklist' : 'Blacklist'),
        cls: (company) => (company.is_blacklisted ? 'green' : 'red'),
        onClick: (company) => store.toggleCompany(company.id),
      },
    ],
    options: [
      { key: 'name', label: 'Name' },
      { key: 'company_id', label: 'Company ID' },
      { key: 'industry', label: 'Industry' },
    ],
    table: {
      headers: store.companyHeader,
      data: store.companies,
    },
  },
  {
    key: 'registered_student',
    title: 'Registered Students',
    filter_enabled: true,
    buttons_present: true,
    buttons: [
      viewButton('students'),
      {
        key: 'toggle_student',
        label: (student) => (student.is_blacklisted ? 'Unblacklist' : 'Blacklist'),
        cls: (student) => (student.is_blacklisted ? 'green' : 'red'),
        onClick: (student) => store.toggleStudent(student.id),
      },
    ],
    options: [
      { key: 'name', label: 'Name' },
      { key: 'student_id', label: 'Student ID' },
      { key: 'contact_number', label: 'Contact Number' },
    ],
    table: {
      headers: store.studentHeader,
      data: store.students,
    },
  },
  {
    key: 'approve_companies',
    title: 'Approve Companies',
    filter_enabled: false,
    buttons_present: true,
    buttons: [
      viewButton('companies'),
      {
        key: 'approve_company',
        label: 'Approve',
        cls: 'green',
        onClick: (company) => store.approveCompany(company.id),
      },
    ],
    options: [],
    table: {
      headers: store.companyHeader,
      data: store.unapprovedCompanies,
    },
  },
  {
    key: 'approve_drives',
    title: 'Approve Drives',
    filter_enabled: false,
    buttons_present: true,
    buttons: [
      viewButton('drives'),
      {
        key: 'approve_drive',
        label: 'Approve',
        cls: 'green',
        onClick: (drive) => store.approveDrive(drive.id),
      },
    ],
    options: [],
    table: {
      headers: store.drivesHeader,
      data: store.pendingDrives,
    },
  },
  {
    key: 'ongoing_drives',
    title: 'Ongoing Drives',
    filter_enabled: false,
    buttons_present: true,
    buttons: [
      viewButton('drives'),
      {
        key: 'complete_drive',
        label: 'Mark as Complete',
        cls: 'green',
        onClick: (drive) => store.completeDrive(drive.id),
      },
    ],
    options: [],
    table: {
      headers: store.drivesHeader,
      data: store.ongoingDrives,
    },
  },
  {
    key: 'student_applications',
    title: 'Student Applications',
    filter_enabled: false,
    buttons_present: true,
    buttons: [viewButton('applications')],
    options: [],
    table: {
      headers: store.applicationHeader,
      data: store.applications,
    },
  },
])
</script>

<style scoped></style>
