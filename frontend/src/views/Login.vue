<template>
  <form class="form" @submit.prevent="submit">
    <div v-if="errors._form?.length" class="form__error">
      <div v-for="err in errors._form" :key="err">{{ err }}</div>
    </div>
    <FormField
      v-for="formField in formFields"
      :key="formField.id"
      :id="formField.id"
      :label="formField.label"
      :type="formField.type"
      v-model="form[formField.id]"
      :errors="errors[formField.id]"
    />
    <button type="submit" class="form__submit">Login</button>
  </form>

  <div class="logout__form">
    <div class="logout__form-message">Don't have an account? Register as:</div>
    <div class="logout__form-buttons">
      <router-link to="/register/student" class="logout__form-button sign_up">Student</router-link>
      <router-link to="/register/company" class="logout__form-button sign_up">Company</router-link>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import FormField from '@/components/FormField.vue'
import router from '@/router/index.js'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

const form = reactive({
  username: '',
  password: '',
})

const errors = reactive({
  username: [],
  password: [],
  _form: [],
})

const formFields = [
  { id: 'username', label: 'Username', type: 'text' },
  { id: 'password', label: 'Password', type: 'password' },
]

async function submit() {
  for (const key in errors) {
    errors[key] = []
  }

  const res = await fetch(`${API_BASE_URL}/auth/login`, {
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
    Object.assign(errors, data.errors || {})
    return
  }

  if (data.user?.role === 'admin') {
    router.replace('/admin')
  } else if (data.user?.role === 'company') {
    if (data.user?.company?.is_blacklisted) {
      errors._form = ['Your company account has been blacklisted.']
      return
    }

    router.replace(data.user?.company?.is_approved ? '/company' : '/company/profile/edit')
  } else if (data.user?.role === 'student') {
    if (data.user?.student?.is_blacklisted) {
      errors._form = ['Your student account has been blacklisted.']
      return
    }

    router.replace('/student')
  }
}
</script>

<style scoped></style>
