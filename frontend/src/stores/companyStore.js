import { defineStore } from 'pinia'
import { ref } from 'vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export const useCompanyStore = defineStore('company', () => {
  const company = ref(null)
  const ongoingDrives = ref([])
  const completedDrives = ref([])
  const currentDrive = ref(null)
  const driveApplications = ref([])
  const currentApplication = ref(null)

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
    const data = await request('/company/dashboard')
    company.value = data.company
    ongoingDrives.value = data.ongoing_drives
    completedDrives.value = data.completed_drives
    return data
  }

  async function fetchProfile() {
    const data = await request('/company/profile')
    company.value = data
    return data
  }

  async function updateProfile(payload) {
    const data = await request('/company/profile', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
    company.value = data
    return data
  }

  async function createDrive(payload) {
    return request('/company/drives', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  }

  async function fetchDrive(id) {
    const data = await request(`/company/drives/${id}`)
    currentDrive.value = data
    return data
  }

  async function updateDrive(id, payload) {
    const data = await request(`/company/drives/${id}`, {
      method: 'POST',
      body: JSON.stringify(payload),
    })
    currentDrive.value = data
    return data
  }

  async function toggleDriveStatus(id) {
    return request(`/company/drives/${id}/toggle`, {
      method: 'POST',
    })
  }

  async function fetchDriveApplications(id) {
    const data = await request(`/company/drives/${id}/applications`)
    currentDrive.value = data.drive
    driveApplications.value = data.applications
    return data
  }

  async function fetchApplication(id) {
    const data = await request(`/company/applications/${id}`)
    currentApplication.value = data
    return data
  }

  async function updateApplicationStatus(id, payload) {
    const data = await request(`/company/applications/${id}/status`, {
      method: 'POST',
      body: JSON.stringify(payload),
    })
    currentApplication.value = data
    return data
  }

  return {
    company,
    ongoingDrives,
    completedDrives,
    currentDrive,
    driveApplications,
    currentApplication,
    fetchDashboard,
    fetchProfile,
    updateProfile,
    createDrive,
    fetchDrive,
    updateDrive,
    toggleDriveStatus,
    fetchDriveApplications,
    fetchApplication,
    updateApplicationStatus,
  }
})
