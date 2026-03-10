<template>
  <div class="bordered-items">
    <h1 class="view_details-header">Student Application</h1>
    <div class="view_details">
      <ul class="view_details-items">
        <li class="view_details-item">
          <span class="item_title subentry">Student Name:</span
          ><span class="item_value subentry">{{ application.student?.name || 'N/A' }}</span>
        </li>
        <li class="view_details-item">
          <span class="item_title subentry">Department:</span
          ><span class="item_value subentry">{{ application.student?.department || 'N/A' }}</span>
        </li>
        <li class="view_details-item">
          <span class="item_title subentry">Drive:</span
          ><span class="item_value subentry">{{ application.drive?.name || 'N/A' }}</span>
        </li>
        <li class="view_details-item">
          <span class="item_title subentry">Job Title:</span
          ><span class="item_value subentry">{{ application.drive?.job_title || 'N/A' }}</span>
        </li>
      </ul>
      <div class="view_details-image view_details-image--placeholder">Student</div>
    </div>
    <div class="company-review__actions">
      <a
        :href="application.resume_link || '#'"
        target="_blank"
        rel="noreferrer"
        class="item__button-blue"
        >view resume</a
      >
      <a
        v-if="application.offer_letter_link"
        :href="application.offer_letter_link"
        target="_blank"
        rel="noreferrer"
        class="item__button-green"
        >view offer</a
      >
    </div>
  </div>

  <form class="form" @submit.prevent="saveStatus">
    <FormField
      v-for="field in reviewFields"
      :key="field.id"
      :id="field.id"
      :label="field.label"
      :type="field.type"
      :as="field.as"
      :rows="field.rows"
      :options="field.options"
      v-model="form[field.id]"
      :errors="errors[field.id]"
    />

    <button type="submit" class="item__button-cyan">Save</button>
  </form>

  <div class="view_details-buttons bordered-buttons">
    <router-link
      :to="`/company/drives/${application.drive?.id || ''}`"
      class="view_details-button item__button-blue"
      >Back</router-link
    >
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import FormField from '@/components/FormField.vue'
import { useCompanyStore } from '@/stores/companyStore'

const route = useRoute()
const store = useCompanyStore()
const application = ref({ student: {}, drive: {} })

const statusOptions = [
  { label: 'Applied', value: 'applied' },
  { label: 'Shortlisted', value: 'shortlisted' },
  { label: 'Selected', value: 'selected' },
  { label: 'Rejected', value: 'rejected' },
]

const interviewModeOptions = [
  { label: 'Select Mode', value: '' },
  { label: 'Online', value: 'Online' },
  { label: 'Offline', value: 'Offline' },
  { label: 'Phone', value: 'Phone' },
]

const reviewFields = [
  {
    id: 'status',
    label: 'Application Status',
    as: 'select',
    options: statusOptions,
    initialValue: 'applied',
    getValue: (data) => data.status || 'applied',
  },
  {
    id: 'remark',
    label: 'Feedback',
    as: 'textarea',
    rows: 3,
    initialValue: '',
    getValue: (data) => (data.remark === 'None' ? '' : data.remark || ''),
  },
  {
    id: 'interview_date',
    label: 'Interview Date',
    type: 'date',
    initialValue: '',
  },
  {
    id: 'interview_mode',
    label: 'Interview Mode',
    as: 'select',
    options: interviewModeOptions,
    initialValue: '',
  },
  {
    id: 'interview_location',
    label: 'Interview Location',
    type: 'text',
    initialValue: '',
  },
  {
    id: 'interview_feedback',
    label: 'Interview Feedback',
    as: 'textarea',
    rows: 3,
    initialValue: '',
  },
  {
    id: 'placement_position',
    label: 'Position Offered',
    type: 'text',
    initialValue: '',
  },
  {
    id: 'placement_salary',
    label: 'Offer Salary',
    type: 'number',
    initialValue: '',
  },
  {
    id: 'joining_date',
    label: 'Joining Date',
    type: 'date',
    initialValue: '',
  },
  {
    id: 'offer_letter_link',
    label: 'Offer Letter Link',
    type: 'text',
    initialValue: '',
  },
]

const form = reactive(
  Object.fromEntries(reviewFields.map((field) => [field.id, field.initialValue ?? ''])),
)

const errors = reactive({
  ...Object.fromEntries(reviewFields.map((field) => [field.id, []])),
  _form: [],
})

onMounted(loadApplication)

async function loadApplication() {
  application.value = await store.fetchApplication(route.params.id)
  syncForm(application.value)
}

function syncForm(data) {
  for (const field of reviewFields) {
    const nextValue = field.getValue
      ? field.getValue(data)
      : (data[field.id] ?? field.initialValue ?? '')
    form[field.id] = nextValue
  }
}

async function saveStatus() {
  resetErrors()

  try {
    application.value = await store.updateApplicationStatus(route.params.id, { ...form })
    syncForm(application.value)
  } catch (error) {
    const payloadErrors = error.payload?.errors
    if (payloadErrors) {
      for (const key in payloadErrors) {
        errors[key] = payloadErrors[key]
      }
      return
    }

    errors.status = [error.message]
  }
}

function resetErrors() {
  for (const key in errors) {
    errors[key] = []
  }
}
</script>

<style scoped>
.company-review__actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
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
