<template>
  <div class="flex flex-col gap-6 h-full">
    <header class="flex justify-between items-center">
      <h2 class="m-0 text-[#F0F0F0] text-3xl font-bold tracking-tight animate-fade-in">Notes Matrix</h2>
    </header>
    
    <div class="w-full flex-1 mt-4">
      <NotesWidget 
        class="h-[calc(100vh-200px)]" 
        :notes="notesStore.items"
        :active-note-id="notesStore.activeNoteId"
        @create="handleCreate"
        @save="handleSave"
        @select="handleSelect"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useNotesStore } from '../stores/notesStore';
import NotesWidget from '../components/dashboard/NotesWidget.vue';

const notesStore = useNotesStore();

onMounted(() => {
  notesStore.fetchNotes();
});

const handleCreate = (noteData) => {
  notesStore.saveNote(noteData);
};

const handleSave = (noteData) => {
  notesStore.saveNote(noteData);
};

const handleSelect = (id) => {
  notesStore.setActiveNote(id);
};
</script>
