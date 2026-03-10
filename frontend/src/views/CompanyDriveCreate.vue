<template>
  <div v-if="errors._form?.length" class="form__error">
    <div v-for="err in errors._form" :key="err">{{ err }}</div>
  </div>
  <form class="form" @submit.prevent="submit">
    <h1 class="form__header">Create a Drive</h1>
    <FormField
      v-for="field in formFields"
      :key="field.id"
      :id="field.id"
      :type="field.type"
      :as="field.as"
      :rows="field.rows"
      :options="field.options"
      :label="field.label"
      v-model="form[field.id]"
      :errors="errors[field.id]"
    />
    <div class="company-form__actions">
      <button type="submit" class="item__button-cyan">Create Drive</button>
      <router-link to="/company" class="item__button-blue">Back</router-link>
    </div>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import FormField from '@/components/FormField.vue'
import { useCompanyStore } from '@/stores/companyStore'

const router = useRouter()
const store = useCompanyStore()

const form = reactive({
  name: '',
  job_title: '',
  job_description: '',
  job_location: '',
  eligibility_criteria: '',
  required_skills: '',
  experience_required: '',
  benefits: '',
  salary: '',
  application_deadline: '',
})

const errors = reactive({
  name: [],
  job_title: [],
  job_description: [],
  job_location: [],
  eligibility_criteria: [],
  required_skills: [],
  experience_required: [],
  benefits: [],
  salary: [],
  application_deadline: [],
  _form: [],
})

const formFields = [
  { id: 'name', label: 'Drive Name', type: 'text' },
  { id: 'job_title', label: 'Job Title', type: 'text' },
  { id: 'job_description', label: 'Job Description', as: 'textarea', rows: 4 },
  { id: 'job_location', label: 'Job Location', type: 'text' },
  { id: 'eligibility_criteria', label: 'Eligibility Criteria', as: 'textarea', rows: 4 },
  { id: 'required_skills', label: 'Required Skills', as: 'textarea', rows: 3 },
  { id: 'experience_required', label: 'Experience Required', type: 'text' },
  { id: 'benefits', label: 'Benefits', as: 'textarea', rows: 3 },
  { id: 'salary', label: 'Salary', type: 'number' },
  { id: 'application_deadline', label: 'Application Deadline', type: 'date' },
]

async function submit() {
  resetErrors()

  try {
    const drive = await store.createDrive(form)
    router.push(`/company/drives/${drive.id}`)
  } catch (error) {
    applyErrors(error)
  }
}

function resetErrors() {
  for (const key in errors) {
    errors[key] = []
  }
}

function applyErrors(error) {
  const payloadErrors = error.payload?.errors
  if (payloadErrors) {
    for (const key in payloadErrors) {
      errors[key] = payloadErrors[key]
    }
    return
  }

  errors._form = [error.message]
}
</script>

<style scoped>
.company-form__actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem;
}
</style>
