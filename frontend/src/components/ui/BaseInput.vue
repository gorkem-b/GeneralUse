<template>
  <input 
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
    @keyup.enter="$emit('enter')"
    :placeholder="placeholder"
    class="w-full px-4 py-2.5 rounded-xl border border-white/10 bg-black/40 text-[#F0F0F0] outline-none transition-all duration-300 focus:border-electric focus:ring-1 focus:ring-electric/50 shadow-inner placeholder:text-gray-500"
  />
</template>

<script setup>
defineProps({
  modelValue: [String, Number],
  placeholder: String
});

defineEmits(['update:modelValue', 'enter']);
</script>
