import { defineStore } from 'pinia';
import api from '../services/api';

/**
 * ==============================================================================
 * Notes Pinia Store
 * Manages the state for the Notes Matrix widget.
 * This handles saving and loading notes, and tracks which note is currently
 * open in the plaintext editor.
 * ==============================================================================
 */
export const useNotesStore = defineStore('notes', {
  state: () => ({
    items: [],           // Array holding all note objects for the user
    activeNoteId: null,  // ID of the note currently selected in the UI
    loading: false,
    error: null,
  }),
  actions: {
    async fetchNotes() {
      // Load all notes from the backend
      this.loading = true;
      try {
        const response = await api.get('/api/dashboard/notes/');
        this.items = response.data;
      } catch (err) {
        this.error = 'Failed to fetch notes';
      } finally {
        this.loading = false;
      }
    },
    async saveNote(noteData) {
      // This method handles BOTH creating a new note and updating an existing one!
      try {
        if (noteData.id) {
          // If the note has an ID, it already exists in the DB -> UPDATE (PUT)
          const response = await api.put(`/api/dashboard/notes/${noteData.id}/`, noteData);
          const index = this.items.findIndex(n => n.id === noteData.id);
          if (index !== -1) this.items[index] = response.data;
        } else {
          // If the note has NO ID, it is a brand new note -> CREATE (POST)
          const response = await api.post('/api/dashboard/notes/', noteData);
          this.items.push(response.data);
          
          // Automatically set the new note as the active one so the user can start typing
          this.activeNoteId = response.data.id;
        }
      } catch (err) {
        this.error = 'Failed to save note';
      }
    },
    async deleteNote(id) {
      // Remove a note from the DB and the local UI array
      try {
        await api.delete(`/api/dashboard/notes/${id}/`);
        this.items = this.items.filter(n => n.id !== id);
        
        // If the user deleted the note they were currently viewing, clear the editor
        if (this.activeNoteId === id) this.activeNoteId = null;
      } catch (err) {
        this.error = 'Failed to delete note';
      }
    },
    setActiveNote(id) {
      // Simple synchronous method to change which note is displayed in the editor
      this.activeNoteId = id;
    }
  },
});
