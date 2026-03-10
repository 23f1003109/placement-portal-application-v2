import { defineStore } from 'pinia'
import { ref } from 'vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export const useAdminDashboardStore = defineStore('adminDashboard', () => {
  const companies = ref([])
  const students = ref([])
  const unapprovedCompanies = ref([])
  const pendingDrives = ref([])
  const ongoingDrives = ref([])
  const applications = ref([])

  const companyHeader = ref([
    { key: 'name', content: 'Name', colspan: 1 },
  ])

  const studentHeader = ref([
    { key: 'name', content: 'Name', colspan: 1 },
  ])

  const drivesHeader = ref([
    { key: 'id', colspan: 1, content: 'ID' },
    { key: 'name', colspan: 1, content: 'Drive Name' },
    { key: 'company_name', colspan: 1, content: 'Company' },
    { key: 'application_deadline', colspan: 1, content: 'Deadline' },
  ])

  const applicationHeader = ref([
    { key: 'id', colspan: 1, content: 'ID' },
    { key: 'student_name', colspan: 1, content: 'Student Name' },
    { key: 'drive_name', colspan: 1, content: 'Drive Name' },
    { key: 'company_name', colspan: 1, content: 'Company Name' },
    { key: 'application_date', colspan: 1, content: 'Application Date' },
  ])

  async function fetchCompanies(params = '') {
    const res = await fetch(`${API_BASE_URL}/admin/companies?${params}`, {
      credentials: 'include',
    })
    companies.value = await res.json()
  }

  async function fetchStudents(params = '') {
    const res = await fetch(`${API_BASE_URL}/admin/students?${params}`, {
      credentials: 'include',
    })
    students.value = await res.json()
  }

  async function fetchUnapprovedCompanies() {
    const res = await fetch(`${API_BASE_URL}/admin/companies?is_approved=false`, {
      credentials: 'include',
    })
    unapprovedCompanies.value = await res.json()
  }

  async function fetchPendingDrives() {
    const res = await fetch(`${API_BASE_URL}/admin/drives?is_approved=false&is_completed=false`, {
      credentials: 'include',
    })
    pendingDrives.value = await res.json()
  }

  async function fetchOngoingDrives() {
    const res = await fetch(`${API_BASE_URL}/admin/drives?is_completed=false&is_approved=true`, {
      credentials: 'include',
    })
    ongoingDrives.value = await res.json()
  }

  async function fetchApplications() {
    const res = await fetch(`${API_BASE_URL}/admin/applications`, {
      credentials: 'include',
    })
    applications.value = await res.json()
  }

  async function fetchEntityDetails(entityType, id) {
    const res = await fetch(`${API_BASE_URL}/admin/${entityType}/${id}`, {
      credentials: 'include',
    })

    if (!res.ok) {
      throw new Error('Unable to fetch details right now.')
    }

    return res.json()
  }

  async function toggleCompany(id) {
    await fetch(`${API_BASE_URL}/admin/companies/${id}/toggle-blacklist`, {
      method: 'POST',
      credentials: 'include',
    })
    await fetchCompanies()
  }

  async function toggleStudent(id) {
    await fetch(`${API_BASE_URL}/admin/students/${id}/toggle-blacklist`, {
      method: 'POST',
      credentials: 'include',
    })
    await fetchStudents()
  }

  async function approveCompany(id) {
    await fetch(`${API_BASE_URL}/admin/companies/${id}/approve`, {
      method: 'POST',
      credentials: 'include',
    })
    await Promise.all([fetchUnapprovedCompanies(), fetchCompanies()])
  }

  async function approveDrive(id) {
    await fetch(`${API_BASE_URL}/admin/drives/${id}/approve`, {
      method: 'POST',
      credentials: 'include',
    })
    await Promise.all([fetchPendingDrives(), fetchOngoingDrives()])
  }

  async function completeDrive(id) {
    await fetch(`${API_BASE_URL}/admin/drives/${id}/complete`, {
      method: 'POST',
      credentials: 'include',
    })
    await fetchOngoingDrives()
  }

  async function loadDashboard() {
    await Promise.all([
      fetchCompanies(),
      fetchStudents(),
      fetchUnapprovedCompanies(),
      fetchPendingDrives(),
      fetchOngoingDrives(),
      fetchApplications(),
    ])
  }

  return {
    companies,
    students,
    unapprovedCompanies,
    pendingDrives,
    ongoingDrives,
    applications,
    fetchCompanies,
    fetchStudents,
    fetchUnapprovedCompanies,
    fetchPendingDrives,
    fetchOngoingDrives,
    fetchApplications,
    fetchEntityDetails,
    toggleCompany,
    toggleStudent,
    approveCompany,
    approveDrive,
    completeDrive,
    companyHeader,
    studentHeader,
    drivesHeader,
    applicationHeader,
    loadDashboard,
  }
})
