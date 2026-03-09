import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import RegisterStudent from '@/views/RegisterStudent.vue'
import RegisterCompany from '@/views/RegisterCompany.vue'
import AdminDashboard from '@/views/AdminDashboard.vue'
import AdminEntityDetails from '@/views/AdminEntityDetails.vue'
import SeedDatabase from '@/components/SeedDatabase.vue'

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
    path: '/admin/:entityType/:id',
    component: AdminEntityDetails,
    meta: { layout: 'mini' },
  },
  {
    path: '/admin/seed',
    component: SeedDatabase,
    meta: { layout: 'full' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
