<template>
  <SecondaryHeader :title="store.company?.name || 'Company'">
    <router-link to="/company/profile/edit" class="item__button-blue">Update Profile</router-link>
    <router-link to="/company/drives/new" class="item__button-cyan">Create Drive</router-link>
  </SecondaryHeader>

  <ListDisplay
    v-for="tableItem in tableItems"
    :key="tableItem.key"
    :title="tableItem.title"
    :tableKey="tableItem.key"
    :filterEnabled="false"
    :buttonsPresent="true"
    :buttons="tableItem.buttons"
    :options="[]"
    :table="tableItem.table"
  />
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ListDisplay from '@/components/ListDisplay.vue'
import SecondaryHeader from '@/components/SecondaryHeader.vue'
import { useCompanyStore } from '@/stores/companyStore'

const router = useRouter()
const store = useCompanyStore()

const upcomingDrivesHeader = [
  {
    key: 'id',
    content: 'Sr No.',
    colspan: 1,
  },
  {
    key: 'name',
    content: 'Drive Name',
    colspan: 1,
  },
  {
    key: 'application_count',
    content: 'Applications',
    colspan: 1,
  },
]

const closedDrivesHeader = [
  {
    key: 'id',
    content: 'Sr No.',
    colspan: 1,
  },
  {
    key: 'name',
    content: 'Drive Name',
    colspan: 1,
  },
]

onMounted(() => {
  store.fetchDashboard()
})

async function toggleDriveStatus(drive) {
  await store.toggleDriveStatus(drive.id)
  await store.fetchDashboard()
}

const tableItems = computed(() => [
  {
    key: 'upcoming_drives',
    title: 'Upcoming Drives',
    buttons: [
      {
        key: 'view_drive',
        label: 'View Details',
        cls: 'blue',
        onClick: (drive) => router.push(`/company/drives/${drive.id}`),
      },
      {
        key: 'complete_drive',
        label: 'Mark as Complete',
        cls: 'green',
        onClick: toggleDriveStatus,
      },
    ],
    table: {
      headers: upcomingDrivesHeader,
      data: store.ongoingDrives,
    },
  },
  {
    key: 'closed_drives',
    title: 'Closed Drives',
    buttons: [
      {
        key: 'update_drive_status',
        label: 'Update',
        cls: 'blue',
        onClick: toggleDriveStatus,
      },
    ],
    table: {
      headers: closedDrivesHeader,
      data: store.completedDrives,
    },
  },
])
</script>

<style scoped></style>
