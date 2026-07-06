<template>
  <header class="flex justify-between items-center px-8 py-4 bg-slate/70 backdrop-blur-lg border-b border-white/5 shadow-sm relative z-10">
    <div class="flex items-center gap-4">
      <img src="/logo.jpg" alt="GeneralUse Logo" class="w-10 h-10 rounded-xl shadow-lg ring-1 ring-white/10" />
      <h1 class="m-0 text-white text-xl tracking-tight font-bold font-sans">GeneralUse</h1>
    </div>
    
    <div class="flex items-center gap-8">
      <div class="flex items-center gap-4">
        <span v-if="authStore.user" class="text-[#F0F0F0] font-sans font-bold tracking-wide">{{ authStore.user.username }}</span>
        <BaseButton variant="ghost" @click="handleLogout">Logout</BaseButton>
      </div>
    </div>
  </header>
</template>

<script setup>
/**
 * AppHeader Component
 * Displays the application logo and user controls (username and logout button).
 */
import { useAuthStore } from '../../stores/authStore';
import { useRouter } from 'vue-router';
import BaseButton from '../ui/BaseButton.vue';

const authStore = useAuthStore();
const router = useRouter();

const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};
</script>
