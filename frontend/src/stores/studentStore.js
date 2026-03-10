import { defineStore } from 'pinia'
import { ref } from 'vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export const useStudentStore = defineStore('student', () => {
  const student = ref(null)
  const companies = ref([])
  const availableDrives = ref([])
  const appliedApplications = ref([])
  const history = ref([])
  const currentCompany = ref(null)
  const companyDrives = ref([])
  const currentDrive = ref(null)

  async function request(path, options = {}) {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      },
      ...options,
    })

    let data = null
    try {
      data = await response.json()
    } catch {
      data = null
    }

    if (!response.ok) {
      const error = new Error(data?.error || data?.message || 'Request failed.')
      error.payload = data
      throw error
    }

    return data
  }

  async function fetchDashboard() {
    const data = await request('/student/dashboard')
    student.value = data.student
    companies.value = data.companies
    availableDrives.value = data.available_drives
    appliedApplications.value = data.applied_applications
    return data
  }

  async function fetchProfile() {
    const data = await request('/student/profile')
    student.value = data
    return data
  }

  async function updateProfile(payload) {
    const data = await request('/student/profile', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
    student.value = data
    return data
  }

  async function fetchAvailableDrives(params = '') {
    const suffix = params ? `?${params}` : ''
    const data = await request(`/student/drives${suffix}`)
    availableDrives.value = data
    return data
  }

  async function fetchHistory() {
    const data = await request('/student/history')
    history.value = data
    return data
  }

  async function fetchCompany(id) {
    const data = await request(`/student/companies/${id}`)
    currentCompany.value = data.company
    companyDrives.value = data.drives
    return data
  }

  async function fetchDrive(id) {
    const data = await request(`/student/drives/${id}`)
    currentDrive.value = data
    return data
  }

  async function applyToDrive(id, payload) {
    return request(`/student/drives/${id}/apply`, {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  }

  return {
    student,
    companies,
    availableDrives,
    appliedApplications,
    history,
    currentCompany,
    companyDrives,
    currentDrive,
    fetchDashboard,
    fetchProfile,
    updateProfile,
    fetchAvailableDrives,
    fetchHistory,
    fetchCompany,
    fetchDrive,
    applyToDrive,
  }
})
