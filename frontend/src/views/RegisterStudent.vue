<template>
  <div v-if="errors._form?.length" class="form__error">
    <div v-for="err in errors._form" :key="err">{{ err }}</div>
  </div>
  <form class="form" @submit.prevent="submit">
    <FormField
      v-for="field in formFields"
      :key="field.id"
      :id="field.id"
      :type="field.type"
      :label="field.label"
      v-model="form[field.id]"
      :errors="errors[field.id]"
    />
    <button type="submit" class="form__submit">Register</button>
  </form>
  <div class="logout__form">
    <div class="logout__form-message">Already registered?</div>
    <router-link to="/login" class="logout__form-button sign_up">Login</router-link>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import FormField from '@/components/FormField.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL
const form = reactive({
  username: '',
  password: '',
  email: '',
  name: '',
  department: '',
  degree: '',
  contact_number: '',
})

const errors = reactive({
  username: [],
  password: [],
  email: [],
  name: [],
  department: [],
  degree: [],
  contact_number: [],
  _form: [],
})

const formFields = [
  { id: 'username', label: 'Username', type: 'text' },
  { id: 'password', label: 'Password', type: 'password' },
  { id: 'email', label: 'Email', type: 'email' },
  { id: 'name', label: 'Name', type: 'text' },
  { id: 'department', label: 'Department', type: 'text' },
  { id: 'degree', label: 'Degree', type: 'text' },
  { id: 'contact_number', label: 'Contact Number', type: 'text' },
]

async function submit() {
  for (const key in errors) {
    errors[key] = []
  }
  const res = await fetch(`${API_BASE_URL}/auth/register/student`, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(form),
  })
  let data = {}
  try {
    data = await res.json()
  } catch {}
  if (!res.ok) {
    for (const key in data.errors || {}) {
      errors[key] = data.errors[key]
    }
  } else {
    router.push('/login')
  }
}
</script>

<style scoped></style>

