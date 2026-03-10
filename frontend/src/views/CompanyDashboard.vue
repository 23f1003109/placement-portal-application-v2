<template>
  <SecondaryHeader :title="store.company?.name || 'Company'">
    <router-link to="/company/profile/edit" class="item__button-blue">Update Profile</router-link>
    <router-link v-if="!accessError" to="/company/drives/new" class="item__button-cyan">Create Drive</router-link>
  </SecondaryHeader>

  <article v-if="accessError" class="list_display">
    <div class="list_display-header">
      <h2 class="list_display-title">Company Access</h2>
    </div>
    <p class="list_display-description">{{ accessError }}</p>
  </article>

  <ListDisplay
    v-else
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
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import ListDisplay from '@/components/ListDisplay.vue'
import SecondaryHeader from '@/components/SecondaryHeader.vue'
import { useCompanyStore } from '@/stores/companyStore'

const router = useRouter()
const store = useCompanyStore()
const accessError = ref('')

const upcomingDrivesHeader = [
  { key: 'id', content: 'Sr No.', colspan: 1 },
  { key: 'name', content: 'Drive Name', colspan: 1 },
  { key: 'application_count', content: 'Applications', colspan: 1 },
]

const closedDrivesHeader = [
  { key: 'id', content: 'Sr No.', colspan: 1 },
  { key: 'name', content: 'Drive Name', colspan: 1 },
]

onMounted(loadDashboard)

async function loadDashboard() {
  accessError.value = ''

  try {
    await store.fetchDashboard()
  } catch (error) {
    if (error.status === 403) {
      accessError.value = error.message
      await store.fetchProfile()
      return
    }

    throw error
  }
}

async function toggleDriveStatus(drive) {
  await store.toggleDriveStatus(drive.id)
  await loadDashboard()
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
