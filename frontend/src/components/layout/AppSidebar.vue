<template>
  <aside class="w-[250px] bg-charcoal/50 backdrop-blur-sm border-r border-white/5 py-8 z-0">
    <nav class="flex flex-col gap-2">
      <router-link to="/" class="block px-8 py-3 text-gray-400 no-underline text-base transition-all duration-300 border-l-[3px] border-transparent hover:bg-white/5 hover:text-[#F0F0F0] hover:translate-x-1" exact-active-class="!text-electric !border-electric !bg-electric/10 !translate-x-1 shadow-[inset_4px_0_0_0_#2979FF]">Finance</router-link>
      <router-link to="/tasks" class="block px-8 py-3 text-gray-400 no-underline text-base transition-all duration-300 border-l-[3px] border-transparent hover:bg-white/5 hover:text-[#F0F0F0] hover:translate-x-1" active-class="!text-electric !border-electric !bg-electric/10 !translate-x-1 shadow-[inset_4px_0_0_0_#2979FF]">Tasks</router-link>
      <router-link to="/notes" class="block px-8 py-3 text-gray-400 no-underline text-base transition-all duration-300 border-l-[3px] border-transparent hover:bg-white/5 hover:text-[#F0F0F0] hover:translate-x-1" active-class="!text-electric !border-electric !bg-electric/10 !translate-x-1 shadow-[inset_4px_0_0_0_#2979FF]">Notes Matrix</router-link>
      <router-link to="/events" class="block px-8 py-3 text-gray-400 no-underline text-base transition-all duration-300 border-l-[3px] border-transparent hover:bg-white/5 hover:text-[#F0F0F0] hover:translate-x-1" active-class="!text-electric !border-electric !bg-electric/10 !translate-x-1 shadow-[inset_4px_0_0_0_#2979FF]">Reminders</router-link>
      <router-link to="/weather" class="block px-8 py-3 text-gray-400 no-underline text-base transition-all duration-300 border-l-[3px] border-transparent hover:bg-white/5 hover:text-[#F0F0F0] hover:translate-x-1" active-class="!text-electric !border-electric !bg-electric/10 !translate-x-1 shadow-[inset_4px_0_0_0_#2979FF]">Weather</router-link>
      <div class="h-px bg-white/5 my-2 mx-4"></div>
      <router-link to="/categories" class="block px-8 py-3 text-gray-400 no-underline text-base transition-all duration-300 border-l-[3px] border-transparent hover:bg-white/5 hover:text-[#F0F0F0] hover:translate-x-1" active-class="!text-electric !border-electric !bg-electric/10 !translate-x-1 shadow-[inset_4px_0_0_0_#2979FF]">Categories</router-link>
      <router-link to="/settings" class="block px-8 py-3 text-gray-400 no-underline text-base transition-all duration-300 border-l-[3px] border-transparent hover:bg-white/5 hover:text-[#F0F0F0] hover:translate-x-1" active-class="!text-electric !border-electric !bg-electric/10 !translate-x-1 shadow-[inset_4px_0_0_0_#2979FF]">App Settings</router-link>
    </nav>
  </aside>
</template>

<script setup>
/**
 * AppSidebar Component
 * Provides navigation links to the main sections of the application.
 */
</script>
