<template>
  <BaseCard style="animation-delay: 0.1s; opacity: 0; animation-fill-mode: forwards;" class="animate-slide-up group">
    <h3 class="mt-0 mb-4 text-[#F0F0F0] font-bold tracking-tight">Tasks</h3>
    
    <div class="flex gap-3 mb-4">
      <BaseInput v-model="newTask" @enter="add" placeholder="Add a new task..." />
      <BaseButton @click="add" variant="primary" size="icon">+</BaseButton>
    </div>
    
    <div v-if="loading" class="text-gray-400 text-sm">Loading tasks...</div>
    
    <ul v-else class="list-none p-0 m-0 flex flex-col gap-2 max-h-[250px] overflow-y-auto pr-2 custom-scrollbar relative">
      <TransitionGroup name="list">
        <li v-for="t in tasks" :key="t.id" class="flex items-center gap-3 p-3 bg-black/20 rounded-xl hover:bg-black/40 transition-colors border border-transparent hover:border-white/5 group/item">
          
          <input type="checkbox" :checked="t.status === 'completed'" @change="$emit('toggle', t)" class="cursor-pointer w-4 h-4 accent-electric" />
          
          <span :class="{'line-through text-gray-500': t.status === 'completed', 'text-[#F0F0F0]': t.status !== 'completed'}" class="flex-1 text-sm transition-colors">{{ t.title }}</span>
          
          <BaseButton @click="$emit('delete', t.id)" variant="danger" size="sm" class="opacity-0 group-hover/item:opacity-100">Del</BaseButton>
        </li>
      </TransitionGroup>
      
      <li v-if="tasks.length === 0" class="text-gray-500 italic text-sm text-center py-4">No tasks pending.</li>
    </ul>
  </BaseCard>
</template>

<script setup>
import { ref } from 'vue';
import BaseCard from '../ui/BaseCard.vue';
import BaseInput from '../ui/BaseInput.vue';
import BaseButton from '../ui/BaseButton.vue';

const props = defineProps({
  tasks: { type: Array, required: true },
  loading: { type: Boolean, required: true }
});

const emit = defineEmits(['add', 'toggle', 'delete']);

const newTask = ref('');

const add = () => {
  if (newTask.value.trim()) {
    emit('add', { title: newTask.value.trim(), status: 'pending' });
    newTask.value = '';
  }
};
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.2);
}

.list-enter-active,
.list-leave-active {
  transition: all 0.4s ease;
}
.list-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}
.list-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>
