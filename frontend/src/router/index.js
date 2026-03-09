import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import RegisterStudent from '@/views/RegisterStudent.vue'
import RegisterCompany from '@/views/RegisterCompany.vue'
import AdminDashboard from '@/views/AdminDashboard.vue'
import AdminEntityDetails from '@/views/AdminEntityDetails.vue'
import CompanyApplicationReview from '@/views/CompanyApplicationReview.vue'
import CompanyDashboard from '@/views/CompanyDashboard.vue'
import CompanyDriveCreate from '@/views/CompanyDriveCreate.vue'
import CompanyDriveDetails from '@/views/CompanyDriveDetails.vue'
import CompanyProfileEdit from '@/views/CompanyProfileEdit.vue'
import SeedDatabase from '@/components/SeedDatabase.vue'
import StudentCompanyDetails from '@/views/StudentCompanyDetails.vue'
import StudentDashboard from '@/views/StudentDashboard.vue'
import StudentDriveApply from '@/views/StudentDriveApply.vue'
import StudentDriveDetails from '@/views/StudentDriveDetails.vue'
import StudentHistory from '@/views/StudentHistory.vue'
import StudentProfileEdit from '@/views/StudentProfileEdit.vue'

const routes = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    component: Login,
    meta: { layout: 'mini' },
  },
  {
    path: '/register/student',
    component: RegisterStudent,
    meta: { layout: 'mini' },
  },
  {
    path: '/register/company',
    component: RegisterCompany,
    meta: { layout: 'mini' },
  },
  {
    path: '/admin',
    component: AdminDashboard,
    meta: { layout: 'full' },
  },
  {
    path: '/admin/seed',
    component: SeedDatabase,
    meta: { layout: 'full' },
  },
  {
    path: '/admin/:entityType/:id',
    component: AdminEntityDetails,
    meta: { layout: 'mini' },
  },
  {
    path: '/company',
    component: CompanyDashboard,
    meta: { layout: 'full' },
  },
  {
    path: '/company/profile/edit',
    component: CompanyProfileEdit,
    meta: { layout: 'mini' },
  },
  {
    path: '/company/drives/new',
    component: CompanyDriveCreate,
    meta: { layout: 'mini' },
  },
  {
    path: '/company/drives/:id',
    component: CompanyDriveDetails,
    meta: { layout: 'full' },
  },
  {
    path: '/company/applications/:id',
    component: CompanyApplicationReview,
    meta: { layout: 'mini' },
  },
  {
    path: '/student',
    component: StudentDashboard,
    meta: { layout: 'full' },
  },
  {
    path: '/student/profile/edit',
    component: StudentProfileEdit,
    meta: { layout: 'mini' },
  },
  {
    path: '/student/history',
    component: StudentHistory,
    meta: { layout: 'full' },
  },
  {
    path: '/student/companies/:id',
    component: StudentCompanyDetails,
    meta: { layout: 'full' },
  },
  {
    path: '/student/drives/:id',
    component: StudentDriveDetails,
    meta: { layout: 'mini' },
  },
  {
    path: '/student/drives/:id/apply',
    component: StudentDriveApply,
    meta: { layout: 'mini' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
