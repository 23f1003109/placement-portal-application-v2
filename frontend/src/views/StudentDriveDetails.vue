<template>
  <main>
    <h1 class="view_details-header">{{ store.currentDrive?.drive?.name || 'Drive Details' }}</h1>
    <div class="view_details">
      <ul class="view_details-items">
        <li class="view_details-item"><span class="item_title subentry">Company:</span><span class="item_value subentry">{{ store.currentDrive?.company?.name || 'N/A' }}</span></li>
        <li class="view_details-item"><span class="item_title subentry">Job Title:</span><span class="item_value subentry">{{ store.currentDrive?.drive?.job_title || 'N/A' }}</span></li>
        <li class="view_details-item"><span class="item_title subentry">Job Location:</span><span class="item_value subentry">{{ store.currentDrive?.drive?.job_location || 'N/A' }}</span></li>
        <li class="view_details-item"><span class="item_title subentry">Application Deadline:</span><span class="item_value subentry">{{ store.currentDrive?.drive?.application_deadline || 'N/A' }}</span></li>
        <li class="view_details-item"><span class="item_title subentry">Salary:</span><span class="item_value subentry">{{ store.currentDrive?.drive?.salary || 'N/A' }}</span></li>
        <li class="view_details-item"><span class="item_title subentry">Eligibility Criteria:</span><span class="item_value subentry">{{ store.currentDrive?.drive?.eligibility_criteria || 'N/A' }}</span></li>
      </ul>
      <div class="view_details-image view_details-image--placeholder">Drive</div>
    </div>
    <div class="view_details-buttons">
      <router-link v-if="!store.currentDrive?.has_applied" :to="`/student/drives/${route.params.id}/apply`" class="view_details-button item__button-cyan">Apply</router-link>
      <span v-else class="item__button-green">Applied</span>
      <router-link v-if="store.currentDrive?.company?.id" :to="`/student/companies/${store.currentDrive.company.id}`" class="view_details-button item__button-blue">Back</router-link>
      <router-link v-else to="/student" class="view_details-button item__button-blue">Back</router-link>
    </div>
  </main>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useStudentStore } from '@/stores/studentStore'

const route = useRoute()
const store = useStudentStore()

onMounted(() => {
  store.fetchDrive(route.params.id)
})
</script>

<style scoped>
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
