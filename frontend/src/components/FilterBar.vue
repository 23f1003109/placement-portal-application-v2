<template>
  <select class="dropdown" v-model="filter_by">
    <option v-for="option in options"
            :key="option.key"
            :value="option.key">{{ option.label }}</option>
  </select>
  <input class="search-box" type="search" placeholder="Search by:" v-model="model"/>
  <button class="item__button-blue filter-button"
          @click="applyFilter">Filter</button>
</template>

<script setup>
import { ref } from "vue";
const model = defineModel()
const filter_by = ref("")
const emit = defineEmits(['filter'])
defineProps({
  options: {
    type: Array,
    required: true
  }
})

function applyFilter(){
  emit('filter', {
    filter_by: filter_by.value
  })
}
</script>

<style scoped></style>
