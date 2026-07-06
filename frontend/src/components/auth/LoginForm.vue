<template>
  <form @submit.prevent="handleSubmit" class="flex flex-col gap-5">
    <div class="flex flex-col gap-2">
      <label class="text-[#F0F0F0] font-medium tracking-wide text-sm uppercase">Username</label>
      <input type="text" v-model="username" required class="p-3.5 rounded-lg border border-white/10 bg-black/40 text-[#F0F0F0] outline-none transition-all duration-300 hover:border-white/20 focus:border-electric focus:ring-2 focus:ring-electric/30 shadow-inner" />
    </div>
    <div class="flex flex-col gap-2">
      <label class="text-[#F0F0F0] font-medium tracking-wide text-sm uppercase">Password</label>
      <input type="password" v-model="password" required class="p-3.5 rounded-lg border border-white/10 bg-black/40 text-[#F0F0F0] outline-none transition-all duration-300 hover:border-white/20 focus:border-electric focus:ring-2 focus:ring-electric/30 shadow-inner" />
    </div>
    <div v-if="error" class="text-coral text-sm bg-coral/10 p-3 rounded-lg border border-coral/20 animate-fade-in">{{ error }}</div>
    <button type="submit" class="mt-2 bg-gradient-to-r from-electric to-[#1c65d9] text-white p-3.5 border-none rounded-lg cursor-pointer font-bold text-lg transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_8px_20px_rgba(41,121,255,0.4)] disabled:opacity-70 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:hover:shadow-none" :disabled="isLoading">Login</button>
  </form>
</template>

<script setup>
/**
 * LoginForm Component
 * Handles user login by collecting credentials and dispatching the login action
 * to the AuthStore. Emits a 'success' event upon completion.
 */
import { ref } from 'vue';
import { useAuthStore } from '../../stores/authStore';

const emit = defineEmits(['success']);
const authStore = useAuthStore();

// Form state
const username = ref('');
const password = ref('');
const error = ref('');
const isLoading = ref(false);

/**
 * Handles the form submission by attempting to authenticate via the store.
 */
const handleSubmit = async () => {
  try {
    isLoading.value = true;
    error.value = '';
    // Call the login action from the Pinia store
    await authStore.login({ username: username.value, password: password.value });
    
    // Notify the parent component that login succeeded
    emit('success');
  } catch (err) {
    // Basic error handling for invalid credentials
    error.value = 'Invalid username or password.';
  } finally {
    isLoading.value = false;
  }
};
</script>
