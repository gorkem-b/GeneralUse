<template>
  <BaseCard class="animate-slide-up relative overflow-hidden group">
    
    <div class="absolute -right-10 -top-10 w-32 h-32 bg-mint/10 rounded-full blur-3xl pointer-events-none group-hover:bg-mint/20 transition-colors duration-500"></div>
    
    <h3 class="mt-0 mb-4 text-[#F0F0F0] font-bold tracking-tight">Weather</h3>
    
    <div v-if="loading" class="text-gray-400">Loading...</div>
    <div v-else-if="error" class="text-coral">{{ error }}</div>
    <div v-else-if="data" class="flex flex-col gap-1">
      <div class="text-4xl font-bold font-mono text-transparent bg-clip-text bg-gradient-to-r from-mint to-[#00b35c]">
        {{ data.temperature }}°C
      </div>
      <div class="text-gray-400 font-medium text-sm">
        Wind Speed: {{ data.windspeed }} km/h
      </div>
    </div>
  </BaseCard>
</template>

<script setup>
import BaseCard from '../ui/BaseCard.vue';

defineProps({
  loading: Boolean,
  error: String,
  data: Object
});
</script>
