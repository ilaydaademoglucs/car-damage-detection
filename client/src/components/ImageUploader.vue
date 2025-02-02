<template>
    <div class="p-8 bg-white shadow-2xl rounded-lg" :style="{ fontFamily: 'Poppin, sans-serif' }">
        <h2 class="text-lg font-semibold text-center mb-4 fancy-text">Upload two similar images</h2>
      <div class="flex space-x-6 mb-6">
        <div v-for="(image, index) in ['image1', 'image2']" :key="index" class="w-1/2">
          <div
            class="h-64 border-2 border-gray-300 border-dashed rounded-lg overflow-hidden transition-all duration-300 ease-in-out cursor-pointer"
            :class="{ 'border-gray-500 bg-gray-100': isDragging[image] }"
            @click="triggerFileInput(image)"
            @dragover.prevent="handleDragOver(image)"
            @dragleave.prevent="handleDragLeave(image)"
            @drop.prevent="handleDrop(image, $event)"
          >
            <div v-if="!images[image]" class="h-full flex flex-col items-center justify-center text-gray-400">
              <svg class="w-12 h-12 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
              </svg>
              <span class="text-sm text-center px-4 fancy-text">
                {{ index === 0 ? 'Drag & Drop or Upload Your First Image' : 'Drag & Drop or Upload Your Second Image' }}<br />
                (JPG/PNG, Max 200MB)
              </span>
            </div>
            <img v-else :src="imagePreview[image]" alt="Preview" class="w-full h-full object-cover" />
          </div>
          <input
            type="file"
            :id="image"
            :ref="image"
            class="hidden"
            @change="handleFileChange(image, $event)"
            accept="image/png, image/jpeg"
          />
        </div>
      </div>
      <button
        @click="compareImages"
        :disabled="!images.image1 || !images.image2 || loading"
        class="w-full bg-black text-white py-3 px-6 rounded-md text-lg font-semibold hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 ease-in-out transform hover:scale-105 fancy-text"
      >
        {{ loading ? 'Processing...' : 'Compare Images' }}
      </button>
      <p v-if="error" class="mt-2 text-red-600 text-sm">{{ error }}</p>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, defineEmits } from 'vue';
  import axios from 'axios';
  
  const images = reactive({
    image1: null,
    image2: null,
  });
  
  const imagePreview = reactive({
    image1: null,
    image2: null,
  });
  
  const isDragging = reactive({
    image1: false,
    image2: false,
  });
  
  const loading = ref(false);
  const error = ref('');
  const emit = defineEmits(['image-diff-result']);
  
  const triggerFileInput = (imageKey) => {
    const input = document.getElementById(imageKey);
    input.click();
  };
  
  const handleFileChange = (imageKey, event) => {
    const file = event.target.files[0];
    if (file && isValidFileType(file)) processFile(imageKey, file);
    else error.value = 'Only JPG and PNG files are allowed, and the size should be less than 200MB.';
  };
  
  const isValidFileType = (file) => {
    const validTypes = ['image/jpeg', 'image/png'];
    const maxSize = 200 * 1024 * 1024; // 200MB
    return validTypes.includes(file.type) && file.size <= maxSize;
  };
  
  const handleDragOver = (imageKey) => {
    isDragging[imageKey] = true;
  };
  
  const handleDragLeave = (imageKey) => {
    isDragging[imageKey] = false;
  };
  
  const handleDrop = (imageKey, event) => {
    isDragging[imageKey] = false;
    const file = event.dataTransfer.files[0];
    if (file && isValidFileType(file)) processFile(imageKey, file);
    else error.value = 'Only JPG and PNG files are allowed, and the size should be less than 200MB.';
  };
  
  const processFile = (imageKey, file) => {
    images[imageKey] = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview[imageKey] = e.target.result;
    };
    reader.readAsDataURL(file);
  };
  
  const compareImages = async () => {
    if (!images.image1 || !images.image2) {
      error.value = 'Please select both images.';
      return;
    }
  
    loading.value = true;
    error.value = '';
  
    const formData = new FormData();
formData.append('file1', images.image1); 
formData.append('file2', images.image2);  

try {
  const response = await axios.post('http://127.0.0.1:8000/process-images/', formData, {
  headers: { 'Content-Type': 'multipart/form-data' },
  responseType: 'arraybuffer',
});

  const blob = new Blob([response.data], { type: 'image/png' });


  emit('image-diff-result', blob);
} catch (err) {
  console.error('Error comparing images:', err);
  error.value = 'An error occurred while comparing the images. Please try again.';
} finally {
  loading.value = false;
}

  };

  </script>
  
  <style lang="css">
  </style>
  