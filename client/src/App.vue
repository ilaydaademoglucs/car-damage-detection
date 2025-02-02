<template>
  <div class="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-4xl font-extrabold text-gray-900 text-center mb-8">
        ImagiDiff: Visual Difference Finder
            </h1>
      <div class="bg-white shadow-2xl rounded-lg overflow-hidden">
        <ImageUploader @image-diff-result="handleImageResult" />
        <ImageDiffResult :imageResult="imageDiffResult" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ImageUploader from './components/ImageUploader.vue';
import ImageDiffResult from './components/ImageDiffResult.vue';

const imageDiffResult = ref(null);

const handleImageResult = (result) => {
  imageDiffResult.value = URL.createObjectURL(result);
};
</script>

<style lang="css">
</style>