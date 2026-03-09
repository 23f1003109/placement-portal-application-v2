<template>
  <main>
    <h1 class="view_details-header">{{ pageTitle }}</h1>
    <div class="view_details">
      <ul class="view_details-items">
        <li v-for="field in displayedFields" :key="field.key" class="view_details-item">
          <span class="item_title subentry">{{ field.label }}:</span>
          <span class="item_value subentry">{{ formatValue(field.value) }}</span>
        </li>
      </ul>
      <div class="view_details-image view_details-image--placeholder">{{ imageLabel }}</div>
    </div>
    <p v-if="errorMessage" class="view_details-error">{{ errorMessage }}</p>
    <div class="view_details-buttons">
      <router-link to="/admin" class="view_details-button item__button-blue">Back</router-link>
    </div>
  </main>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAdminDashboardStore } from '@/stores/adminStore.js'

const store = useAdminDashboardStore()
const route = useRoute()

const entity = ref(null)
const errorMessage = ref('')

const entityConfig = {
  companies: {
    title: 'Company Details',
    imageLabel: 'Company',
    fields: {
      id: 'ID',
      name: 'Name',
      industry: 'Industry',
      hr_name: 'HR Name',
      hr_email: 'HR Email',
      hr_contact: 'HR Contact',
      description: 'Description',
      location: 'Location',
      website: 'Website',
      is_approved: 'Approved',
      is_blacklisted: 'Blacklisted',
      user_id: 'User ID',
    },
  },
  students: {
    title: 'Student Details',
    imageLabel: 'Student',
    fields: {
      id: 'ID',
      name: 'Name',
      department: 'Department',
      degree: 'Degree',
      contact_number: 'Contact Number',
      is_blacklisted: 'Blacklisted',
      user_id: 'User ID',
    },
  },
  drives: {
    title: 'Drive Details',
    imageLabel: 'Drive',
    fields: {
      id: 'ID',
      company_id: 'Company ID',
      company_name: 'Company Name',
      name: 'Drive Name',
      job_title: 'Job Title',
      job_description: 'Job Description',
      job_location: 'Job Location',
      eligibility_criteria: 'Eligibility Criteria',
      application_deadline: 'Application Deadline',
      salary: 'Salary',
      is_completed: 'Completed',
    },
  },
  applications: {
    title: 'Application Details',
    imageLabel: 'Application',
    fields: {
      id: 'ID',
      student_id: 'Student ID',
      student_name: 'Student Name',
      drive_id: 'Drive ID',
      drive_name: 'Drive Name',
      company_id: 'Company ID',
      company_name: 'Company Name',
      application_date: 'Application Date',
      status: 'Status',
      resume_link: 'Resume Link',
    },
  },
}

const currentConfig = computed(() => entityConfig[route.params.entityType] ?? {
  title: 'Entity Details',
  imageLabel: 'Entity',
  fields: {},
})

const pageTitle = computed(() => currentConfig.value.title)
const imageLabel = computed(() => currentConfig.value.imageLabel)

const displayedFields = computed(() => {
  if (!entity.value) {
    return []
  }

  const configuredFields = currentConfig.value.fields
  const orderedKeys = Object.keys(configuredFields)
  const seenKeys = new Set(orderedKeys)
  const extraKeys = Object.keys(entity.value).filter((key) => !seenKeys.has(key))

  return [...orderedKeys, ...extraKeys].map((key) => ({
    key,
    label: configuredFields[key] ?? formatLabel(key),
    value: entity.value[key],
  }))
})

async function loadEntityDetails() {
  entity.value = null
  errorMessage.value = ''

  try {
    entity.value = await store.fetchEntityDetails(route.params.entityType, route.params.id)
  } catch (error) {
    errorMessage.value = error.message
  }
}

function formatLabel(value) {
  return value
    .split('_')
    .map((segment) => segment.charAt(0).toUpperCase() + segment.slice(1))
    .join(' ')
}

function formatValue(value) {
  if (typeof value === 'boolean') {
    return value ? 'Yes' : 'No'
  }

  if (value === null || value === undefined || value === '') {
    return 'N/A'
  }

  return value
}

onMounted(loadEntityDetails)

watch(
  () => [route.params.entityType, route.params.id],
  loadEntityDetails,
)
</script>

<style scoped>
.view_details-header {
  margin-bottom: 1.25rem;
}

.view_details-error {
  color: #e23d3d;
  font-weight: 700;
}

.view_details-image--placeholder {
  width: 120px;
  min-width: 120px;
  height: 120px;
  border: 3px solid black;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.subentry {
  display: inline-block;
}

.item_title {
  font-weight: 700;
  margin-right: 0.35rem;
}

@media (max-width: 720px) {
  .view_details {
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .view_details-items {
    margin: 0;
    padding: 0;
  }
}
</style>
