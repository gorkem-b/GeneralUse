<template>
  <div class="flex flex-col gap-6 h-full">
    <header class="flex justify-between items-center">
      <h2 class="m-0 text-[#F0F0F0] text-3xl font-bold tracking-tight animate-fade-in">Events & Reminders</h2>
      <button 
        @click="showCreateForm = !showCreateForm"
        class="bg-electric/20 text-electric hover:bg-electric/30 font-semibold py-2 px-4 rounded-xl transition-colors border border-electric/30"
      >
        {{ showCreateForm ? 'Cancel' : '+ New Event' }}
      </button>
    </header>

    <div v-if="showCreateForm" class="bg-slate/50 backdrop-blur-md rounded-2xl p-6 ring-1 ring-white/5 animate-slide-down">
      <h3 class="text-xl font-bold text-white mb-4">Schedule Event</h3>
      <form @submit.prevent="submitEvent" class="flex flex-col gap-4">
        <div class="flex flex-col gap-1">
          <label class="text-xs text-gray-400 uppercase font-bold tracking-wider">Event Name</label>
          <input v-model="newEvent.event_name" type="text" required class="bg-dark/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-electric transition-shadow" placeholder="Dentist Appointment" />
        </div>
        
        <div class="flex flex-col gap-1">
          <label class="text-xs text-gray-400 uppercase font-bold tracking-wider">Description (Optional)</label>
          <textarea v-model="newEvent.description" class="bg-dark/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-electric transition-shadow resize-none" rows="2" placeholder="Don't forget insurance card..."></textarea>
        </div>
        
        <div class="flex flex-col gap-1">
          <label class="text-xs text-gray-400 uppercase font-bold tracking-wider">Date & Time</label>
          <input v-model="newEvent.event_timestamp" type="datetime-local" required class="bg-dark/50 border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-electric transition-shadow" />
        </div>

        <button type="submit" :disabled="eventsStore.loading" class="mt-2 bg-electric text-white font-bold py-3 px-6 rounded-xl hover:bg-[#1c65d9] transition-colors shadow-lg disabled:opacity-50">
          {{ eventsStore.loading ? 'Saving...' : 'Save & Set Reminder' }}
        </button>
      </form>
    </div>

    <div v-if="eventsStore.loading && !eventsStore.events.length" class="text-center p-8 text-gray-400">Loading events...</div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="event in eventsStore.events" :key="event.id" class="bg-slate/30 backdrop-blur-sm border border-white/5 rounded-2xl p-6 hover:bg-slate/50 transition-colors flex flex-col gap-3 group relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-electric opacity-50 group-hover:opacity-100 transition-opacity"></div>
        <h4 class="text-lg font-bold text-white m-0">{{ event.event_name }}</h4>
        <p class="text-sm text-gray-400 m-0">{{ formatDate(event.event_timestamp) }}</p>
        <p class="text-gray-300 mt-2">{{ event.description }}</p>
      </div>
      
      <div v-if="eventsStore.events.length === 0" class="col-span-full text-center p-12 bg-slate/20 rounded-2xl border border-dashed border-white/10">
        <p class="text-gray-400">No events scheduled. Create one to get started!</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useEventsStore } from '../stores/eventsStore';

const eventsStore = useEventsStore();
const showCreateForm = ref(false);

const newEvent = ref({
  event_name: '',
  description: '',
  event_timestamp: ''
});

onMounted(() => {
  eventsStore.fetchEvents();
});

const submitEvent = async () => {
  try {
    const dateObj = new Date(newEvent.value.event_timestamp);
    await eventsStore.createEvent({
      ...newEvent.value,
      event_timestamp: dateObj.toISOString()
    });
    showCreateForm.value = false;
    newEvent.value = { event_name: '', description: '', event_timestamp: '' };
  } catch (e) {
    alert("Failed to create event: " + e);
  }
};

const formatDate = (isoString) => {
  if (!isoString) return '';
  const date = new Date(isoString);
  return date.toLocaleString(undefined, { 
    weekday: 'short', 
    month: 'short', 
    day: 'numeric', 
    hour: '2-digit', 
    minute: '2-digit' 
  });
};
</script>
