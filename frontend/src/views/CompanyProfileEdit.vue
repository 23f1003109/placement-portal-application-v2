<template>
  <div v-if="errors._form?.length" class="form__error">
    <div v-for="err in errors._form" :key="err">{{ err }}</div>
  </div>
  <form class="form" @submit.prevent="submit">
    <h1 class="form__header">Update Company Profile</h1>
    <FormField
      v-for="field in formFields"
      :key="field.id"
      :id="field.id"
      :type="field.type"
      :as="field.as"
      :rows="field.rows"
      :label="field.label"
      v-model="form[field.id]"
      :errors="errors[field.id]"
    />
    <div class="company-form__actions">
      <button type="submit" class="item__button-cyan">Save</button>
      <router-link to="/company" class="item__button-blue">Back</router-link>
    </div>
  </form>
</template>

<script setup>
import { onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import FormField from '@/components/FormField.vue'
import { useCompanyStore } from '@/stores/companyStore'

const router = useRouter()
const store = useCompanyStore()

const form = reactive({
  name: '',
  industry: '',
  hr_name: '',
  hr_email: '',
  hr_contact: '',
  description: '',
  location: '',
  website: '',
})

const errors = reactive({
  name: [],
  industry: [],
  hr_name: [],
  hr_email: [],
  hr_contact: [],
  description: [],
  location: [],
  website: [],
  _form: [],
})

const formFields = [
  { id: 'name', label: 'Company Name', type: 'text' },
  { id: 'industry', label: 'Industry', type: 'text' },
  { id: 'hr_name', label: 'H.R. Name', type: 'text' },
  { id: 'hr_email', label: 'H.R. Email', type: 'email' },
  { id: 'hr_contact', label: 'H.R. Contact', type: 'text' },
  { id: 'description', label: 'Description', as: 'textarea', rows: 4 },
  { id: 'location', label: 'Location', as: 'textarea', rows: 3 },
  { id: 'website', label: 'Website', type: 'url' },
]

onMounted(async () => {
  const profile = await store.fetchProfile()
  Object.assign(form, profile)
})

async function submit() {
  resetErrors()

  try {
    await store.updateProfile(form)
    router.push('/company')
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
