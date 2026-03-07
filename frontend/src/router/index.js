import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'
import RegisterStudent from '@/views/RegisterStudent.vue'
import RegisterCompany from '@/views/RegisterCompany.vue'

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
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  })

export default router
