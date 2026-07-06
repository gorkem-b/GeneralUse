<template>
  <div class="flex flex-col h-screen overflow-hidden relative">
    <AppHeader />
    <div class="flex flex-1 overflow-hidden">
      <AppSidebar />
      <main class="flex-1 p-8 overflow-y-auto bg-transparent animate-fade-in relative">
        <router-view></router-view>
      </main>
    </div>

    <!-- Notifications Overlay -->
    <div class="fixed top-20 right-8 z-[200] flex flex-col gap-4">
      <div v-for="note in notificationsStore.notifications" :key="note.id" 
           class="bg-electric text-white p-4 rounded-xl shadow-lg border border-white/20 animate-slide-up w-80 relative cursor-pointer"
           @click="notificationsStore.clearNotification(note.id)">
        <h4 class="font-bold m-0 mb-1 text-lg">{{ note.title }}</h4>
        <p class="m-0 text-sm text-white/90">{{ note.message }}</p>
        <button class="absolute top-2 right-2 text-white/50 hover:text-white" @click.stop="notificationsStore.clearNotification(note.id)">✕</button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue';
import AppHeader from './AppHeader.vue';
import AppSidebar from './AppSidebar.vue';
import { useNotificationsStore } from '../../stores/notificationsStore';

const notificationsStore = useNotificationsStore();

onMounted(() => {
  notificationsStore.startPolling();
});

onUnmounted(() => {
  notificationsStore.stopPolling();
});
</script>
