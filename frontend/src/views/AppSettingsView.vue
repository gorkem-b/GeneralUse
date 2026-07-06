<template>
  <div class="flex flex-col gap-6 h-full">
    <header class="flex justify-between items-center">
      <h2 class="m-0 text-[#F0F0F0] text-3xl font-bold tracking-tight animate-fade-in">App Settings</h2>
    </header>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-4">
      <!-- Profile Card -->
      <BaseCard>
        <h3 class="mt-0 mb-4 text-[#F0F0F0] font-bold tracking-tight border-b border-white/5 pb-2">User Profile</h3>
        <div class="flex flex-col gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-400 mb-1">Username</label>
            <BaseInput type="text" :value="authStore.user?.username" disabled class="opacity-50" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-400 mb-1">Email</label>
            <BaseInput type="email" :value="authStore.user?.email" disabled class="opacity-50" />
          </div>
        </div>
      </BaseCard>

      <!-- Preferences Card -->
      <BaseCard>
        <h3 class="mt-0 mb-4 text-[#F0F0F0] font-bold tracking-tight border-b border-white/5 pb-2">Preferences</h3>
        <div class="flex flex-col gap-4">
          <div class="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-white/10">
            <div>
              <div class="text-[#F0F0F0] font-medium">Dark Mode</div>
              <div class="text-sm text-gray-400">Enable dark theme across the app</div>
            </div>
            <!-- Dummy toggle -->
            <div class="w-12 h-6 bg-electric rounded-full relative cursor-pointer">
              <div class="absolute right-1 top-1 w-4 h-4 bg-white rounded-full"></div>
            </div>
          </div>
          
          <div class="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-white/10">
            <div>
              <div class="text-[#F0F0F0] font-medium">Email Notifications</div>
              <div class="text-sm text-gray-400">Receive weekly summaries</div>
            </div>
            <!-- Dummy toggle off -->
            <div class="w-12 h-6 bg-slate rounded-full relative cursor-pointer border border-white/20">
              <div class="absolute left-1 top-1 w-4 h-4 bg-gray-400 rounded-full"></div>
            </div>
          </div>
        </div>
      </BaseCard>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/authStore';
import BaseCard from '../components/ui/BaseCard.vue';
import BaseInput from '../components/ui/BaseInput.vue';

const authStore = useAuthStore();
</script>
