<template>
  <main>
    <h1 class="view_details-header">Student Application</h1>
    <div class="view_details">
      <ul class="view_details-items">
        <li class="view_details-item"><span class="item_title subentry">Student Name:</span><span class="item_value subentry">{{ application.student?.name || 'N/A' }}</span></li>
        <li class="view_details-item"><span class="item_title subentry">Department:</span><span class="item_value subentry">{{ application.student?.department || 'N/A' }}</span></li>
        <li class="view_details-item"><span class="item_title subentry">Drive:</span><span class="item_value subentry">{{ application.drive?.name || 'N/A' }}</span></li>
        <li class="view_details-item"><span class="item_title subentry">Job Title:</span><span class="item_value subentry">{{ application.drive?.job_title || 'N/A' }}</span></li>
      </ul>
      <div class="view_details-image view_details-image--placeholder">Student</div>
    </div>

    <form class="application-form" @submit.prevent="saveStatus">
      <a :href="application.resume_link || '#'" target="_blank" rel="noreferrer" class="item__button-blue">view resume</a>
      <FormField id="status" label="Application Status" as="select" :options="statusOptions" v-model="status" :errors="errors.status" />
      <button type="submit" class="item__button-cyan">Save</button>
    </form>

    <div class="view_details-buttons">
      <router-link :to="`/company/drives/${application.drive?.id || ''}`" class="view_details-button item__button-blue">Back</router-link>
    </div>
  </main>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import FormField from '@/components/FormField.vue'
import { useCompanyStore } from '@/stores/companyStore'

const route = useRoute()
const store = useCompanyStore()
const application = ref({ student: {}, drive: {} })
const status = ref('applied')
const errors = reactive({ status: [] })

const statusOptions = [
  { label: 'Applied', value: 'applied' },
  { label: 'Shortlisted', value: 'shortlisted' },
  { label: 'Selected', value: 'selected' },
  { label: 'Rejected', value: 'rejected' },
]

onMounted(loadApplication)

async function loadApplication() {
  application.value = await store.fetchApplication(route.params.id)
  status.value = application.value.status
}

async function saveStatus() {
  errors.status = []

  try {
    application.value = await store.updateApplicationStatus(route.params.id, { status: status.value })
  } catch (error) {
    const payloadErrors = error.payload?.errors
    if (payloadErrors?.status) {
      errors.status = payloadErrors.status
      return
    }

    errors.status = [error.message]
  }
}
</script>

<style scoped>
.application-form {
  display: flex;
  align-items: flex-end;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin: 1rem 0;
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
}

.subentry {
  display: inline-block;
}

.item_title {
  font-weight: 700;
  margin-right: 0.35rem;
}
</style>
