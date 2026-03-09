<template>
  <h1 class="view_details-header">Update Applications for the Drive</h1>
  <p class="drive-meta">Job Title: {{ form.job_title || 'N/A' }}</p>

  <section class="applications-section">
    <h2>Received Applications</h2>
    <div class="scroll-wrapper">
      <TableDisplay
        :buttonsPresent="true"
        :buttons="buttons"
        :rows="store.driveApplications"
        :columns="headers"
      />
    </div>
  </section>
  <div class="view_details-buttons">
    <router-link to="/company" class="view_details-button item__button-blue">Back</router-link>
  </div>
</template>

<script setup>
import { onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCompanyStore } from '@/stores/companyStore'
import TableDisplay from '@/components/TableDisplay.vue'

const route = useRoute()
const router = useRouter()
const store = useCompanyStore()

const buttons = [viewButton()]
const headers = [
  {
    key: 'student_name',
    content: 'Student Name',
    colspan: 1,
  },
]

function viewButton() {
  return {
    key: 'view_application',
    label: 'Review Application',
    cls: 'blue',
    onClick: (entity) => router.push(`/company/applications/${entity.id}`),
  }
}

const form = reactive({
  name: '',
  job_title: '',
  job_description: '',
  job_location: '',
  eligibility_criteria: '',
  salary: '',
  application_deadline: '',
})

onMounted(loadPage)

async function loadPage() {
  const data = await store.fetchDriveApplications(route.params.id)
  Object.assign(form, data.drive)
}
</script>

<style scoped>
.drive-meta {
  margin-bottom: 1rem;
}

.applications-section {
  width: 100%;
}
</style>
