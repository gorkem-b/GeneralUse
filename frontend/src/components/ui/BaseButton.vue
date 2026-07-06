<template>
  <button 
    :class="[
      'inline-flex items-center justify-center rounded-xl font-bold transition-all duration-300 outline-none cursor-pointer',
      sizeClasses[size] || sizeClasses.md,
      variantClasses[variant] || variantClasses.primary
    ]"
    @click="$emit('click')"
  >
    <slot></slot>
  </button>
</template>

<script setup>
const props = defineProps({
  variant: {
    type: String,
    default: 'primary' // primary, secondary, danger, ghost
  },
  size: {
    type: String,
    default: 'md' // sm, md, lg, icon
  }
});

defineEmits(['click']);

const sizeClasses = {
  sm: 'px-3 py-1.5 text-xs',
  md: 'px-5 py-2.5 text-sm',
  lg: 'px-6 py-3 text-base',
  icon: 'w-10 h-10 p-0 rounded-full'
};

const variantClasses = {
  primary: 'bg-gradient-to-r from-electric to-blue-600 text-white shadow-md shadow-electric/20 hover:-translate-y-0.5 hover:shadow-lg hover:shadow-electric/40 active:translate-y-0 border-none',
  secondary: 'bg-white/5 backdrop-blur-md text-white hover:bg-white/15 border border-white/10 shadow-sm hover:shadow-white/5 hover:-translate-y-0.5 active:translate-y-0',
  danger: 'bg-gradient-to-r from-coral/90 to-red-500/90 text-white shadow-md shadow-coral/20 hover:-translate-y-0.5 hover:shadow-lg hover:shadow-coral/40 active:translate-y-0 border-none',
  ghost: 'bg-transparent text-white/70 hover:bg-white/10 hover:text-white border border-transparent'
};
</script>
