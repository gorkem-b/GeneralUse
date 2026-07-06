<template>
  <BaseCard class="animate-slide-up flex flex-col h-[400px] group" style="animation-delay: 0.2s; opacity: 0; animation-fill-mode: forwards;">
    
    <div class="flex justify-between items-center mb-4">
      <h3 class="m-0 text-[#F0F0F0] font-bold tracking-tight">Notes Matrix</h3>
      <BaseButton @click="createNew" variant="ghost" size="sm">New Note</BaseButton>
    </div>
    
    <div class="flex flex-1 gap-4 overflow-hidden">
      
      <div class="w-1/3 overflow-y-auto pr-2 flex flex-col gap-2 custom-scrollbar border-r border-white/5 relative">
        <TransitionGroup name="list">
          <div v-for="n in notes" :key="n.id" 
               @click="$emit('select', n.id)"
               :class="['p-3 rounded-xl cursor-pointer truncate text-sm transition-all duration-200 border', activeNoteId === n.id ? 'bg-electric/20 text-electric border-electric/30 shadow-inner' : 'text-gray-400 border-transparent hover:bg-white/5 hover:border-white/10']">
            {{ n.title || 'Untitled Note' }}
          </div>
        </TransitionGroup>
        <div v-if="notes.length === 0" class="text-gray-500 italic text-xs text-center py-4">No notes yet.</div>
      </div>
      
      <Transition name="fade" mode="out-in">
        <div class="flex-1 flex flex-col gap-3" v-if="activeNote" :key="activeNote.id">
          <input v-model="activeNote.title" class="p-2 bg-transparent border-b border-white/10 text-[#F0F0F0] outline-none font-bold text-lg transition-colors focus:border-electric" placeholder="Note Title" @blur="save" />
          
          <textarea v-model="activeNote.content" class="flex-1 p-4 bg-black/20 rounded-xl border border-white/5 text-[#F0F0F0] outline-none resize-none font-mono text-sm leading-relaxed transition-colors focus:border-white/20 custom-scrollbar shadow-inner" placeholder="Start typing..." @blur="save"></textarea>
        </div>
        
        <div v-else class="flex-1 flex items-center justify-center text-gray-500 italic text-sm bg-black/10 rounded-xl border border-dashed border-white/10">
          Select a note or create a new one.
        </div>
      </Transition>
    </div>
  </BaseCard>
</template>

<script setup>
import { computed } from 'vue';
import BaseCard from '../ui/BaseCard.vue';
import BaseButton from '../ui/BaseButton.vue';

const props = defineProps({
  notes: { type: Array, required: true },
  activeNoteId: { type: String, default: null }
});

const emit = defineEmits(['create', 'save', 'select']);

const activeNote = computed(() => {
  return props.notes.find(n => n.id === props.activeNoteId) || null;
});

const createNew = () => {
  emit('create', { title: 'New Note', content: '' });
};

const save = () => {
  if (activeNote.value) {
    emit('save', activeNote.value);
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
  transition: all 0.3s ease;
}
.list-enter-from {
  opacity: 0;
  transform: translateX(-15px);
}
.list-leave-to {
  opacity: 0;
  transform: translateX(15px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
