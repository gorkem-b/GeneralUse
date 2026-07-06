<template>
  <div class="bg-slate/40 backdrop-blur-md p-6 rounded-2xl shadow-xl ring-1 ring-white/10 relative overflow-hidden transition-all duration-300 hover:shadow-[0_8px_30px_rgb(0,0,0,0.12)]">
    <!-- Optional glow effect -->
    <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-electric/50 to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100"></div>
    <slot></slot>
  </div>
</template>

<script setup>
</script>
