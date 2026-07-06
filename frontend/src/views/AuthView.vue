<template>
  <div class="flex items-center justify-center h-screen bg-transparent relative overflow-hidden">
    <!-- Animated background specific to Auth -->
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-electric/20 via-charcoal to-charcoal -z-10"></div>
    
    <div class="bg-slate/60 backdrop-blur-xl p-8 rounded-2xl w-full max-w-[400px] shadow-[0_8px_32px_rgba(0,0,0,0.5)] ring-1 ring-white/10 animate-slide-up">
      <LoginForm v-if="isLogin" @success="handleSuccess" />
      <RegisterForm v-else @success="handleSuccess" />
      <p class="mt-6 text-center text-gray-400 cursor-pointer text-sm transition-colors duration-300 hover:text-electric font-medium" @click="isLogin = !isLogin">
        {{ isLogin ? "Don't have an account? Register" : "Already have an account? Login" }}
      </p>
    </div>
  </div>
</template>

<script setup>
/**
 * AuthView Component
 * Acts as a container for the authentication flow.
 * Toggles between LoginForm and RegisterForm based on user interaction.
 * On successful authentication, it redirects the user to the Dashboard.
 */
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import LoginForm from '../components/auth/LoginForm.vue';
import RegisterForm from '../components/auth/RegisterForm.vue';

// State to track whether the user wants to login (true) or register (false)
const isLogin = ref(true);
const router = useRouter();

/**
 * Callback triggered when either the login or register form completes successfully.
 * Navigates the user to the application's root dashboard.
 */
const handleSuccess = () => {
  router.push('/');
};
</script>
