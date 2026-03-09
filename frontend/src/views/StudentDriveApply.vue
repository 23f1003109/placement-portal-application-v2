<template>
  <div v-if="errors._form?.length" class="form__error">
    <div v-for="err in errors._form" :key="err">{{ err }}</div>
  </div>
  <form class="form" @submit.prevent="submit">
    <FormField
      id="resume_link"
      label="Resume Link"
      type="url"
      v-model="form.resume_link"
      :errors="errors.resume_link"
    />
    <div class="student-form__actions">
      <button type="submit" class="form__submit">Apply</button>
      <router-link :to="`/student/drives/${route.params.id}`" class="item__button-blue">Back</router-link>
    </div>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import FormField from '@/components/FormField.vue'
import { useStudentStore } from '@/stores/studentStore'

const route = useRoute()
const router = useRouter()
const store = useStudentStore()

const form = reactive({
  resume_link: '',
})

const errors = reactive({
  resume_link: [],
  _form: [],
})

async function submit() {
  resetErrors()

  try {
    await store.applyToDrive(route.params.id, form)
    router.push(`/student/drives/${route.params.id}`)
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
