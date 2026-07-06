<template>
  <div class="flex flex-col gap-6 h-full">
    <header class="flex justify-between items-center">
      <h2 class="m-0 text-[#F0F0F0] text-3xl font-bold tracking-tight animate-fade-in">Weather Tracker</h2>
    </header>
    
    <div class="max-w-md w-full mx-auto mt-12 flex flex-col gap-6">
      <!-- City Input Form -->
      <div class="bg-slate/40 backdrop-blur-md p-6 rounded-2xl shadow-xl ring-1 ring-white/10 flex flex-col gap-4">
        <label for="city" class="text-white text-sm font-bold uppercase tracking-wide">Enter City</label>
        <div class="flex gap-2">
          <input 
            type="text" 
            id="city" 
            v-model="cityQuery" 
            placeholder="e.g. London, Tokyo, New York" 
            class="flex-1 bg-dark/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-electric transition-all"
            @keyup.enter="handleSearch"
          />
          <button 
            @click="handleSearch" 
            class="bg-electric text-white px-6 py-3 rounded-xl font-bold tracking-wide shadow-lg shadow-electric/30 transition-all hover:bg-electric/90 hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="!cityQuery || weatherStore.loading"
          >
            Search
          </button>
        </div>
        <p v-if="savedCityName" class="text-sm text-white/50 m-0">Current Location: <strong class="text-electric">{{ savedCityName }}</strong></p>
      </div>

      <WeatherWidget 
        v-if="weatherStore.data || weatherStore.loading || weatherStore.error"
        :loading="weatherStore.loading"
        :error="weatherStore.error"
        :data="weatherStore.data"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useWeatherStore } from '../stores/weatherStore';
import WeatherWidget from '../components/dashboard/WeatherWidget.vue';

const weatherStore = useWeatherStore();
const cityQuery = ref('');
const savedCityName = ref('');

onMounted(() => {
  const loadedCity = weatherStore.loadSavedLocation();
  if (loadedCity) {
    savedCityName.value = loadedCity;
  }
});

const handleSearch = async () => {
  if (!cityQuery.value.trim()) return;
  await weatherStore.fetchWeatherByCity(cityQuery.value.trim());
  if (!weatherStore.error) {
    savedCityName.value = localStorage.getItem('weather_city');
    cityQuery.value = '';
  }
};
</script>
