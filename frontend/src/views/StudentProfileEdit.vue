<template>
  <div v-if="errors._form?.length" class="form__error">
    <div v-for="err in errors._form" :key="err">{{ err }}</div>
  </div>
  <form class="form" @submit.prevent="submit">
    <h1 class="form__header">Edit Student Profile</h1>
    <FormField
      v-for="field in formFields"
      :key="field.id"
      :id="field.id"
      :type="field.type"
      :label="field.label"
      v-model="form[field.id]"
      :errors="errors[field.id]"
    />
    <div class="student-form__actions">
      <button type="submit" class="item__button-cyan">Save</button>
      <router-link to="/student" class="item__button-blue">Back</router-link>
    </div>
  </form>
</template>

<script setup>
import { onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import FormField from '@/components/FormField.vue'
import { useStudentStore } from '@/stores/studentStore'

const router = useRouter()
const store = useStudentStore()

const form = reactive({
  name: '',
  department: '',
  degree: '',
  contact_number: '',
})

const errors = reactive({
  name: [],
  department: [],
  degree: [],
  contact_number: [],
  _form: [],
})

const formFields = [
  { id: 'name', label: 'Name', type: 'text' },
  { id: 'department', label: 'Department', type: 'text' },
  { id: 'degree', label: 'Degree', type: 'text' },
  { id: 'contact_number', label: 'Contact Number', type: 'text' },
]

onMounted(async () => {
  const profile = await store.fetchProfile()
  Object.assign(form, profile)
})

async function submit() {
  resetErrors()

  try {
    await store.updateProfile(form)
    router.push('/student')
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
.student-form__actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem;
}
</style>
