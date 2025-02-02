<template>
    <div v-if="imageResult" class="mt-8 p-6 bg-gray-100 rounded-lg shadow-inner">
      <h2 class="text-2xl font-bold text-gray-800 mb-4">Difference Image</h2>
      <div class="bg-white rounded-lg p-4 shadow-md">
        <img :src="imageResult" alt="Difference Image" class="w-full rounded-lg" />
      </div>
      <button
        @click="downloadImage"
        class="mt-4 w-full bg-black text-white py-2 px-4 rounded-md hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-all duration-300 ease-in-out transform hover:scale-105"
      >
        Download 
      </button>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue'
  
  const props = defineProps({
    imageResult: {
      type: String,
      required: true
    }
  })
  
  const downloadImage = () => {
    const link = document.createElement('a')
    link.href = props.imageResult
    link.download = 'difference_image.png'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
  </script>