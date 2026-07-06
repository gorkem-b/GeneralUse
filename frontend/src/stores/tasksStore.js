import { defineStore } from 'pinia';
import api from '../services/api';

/**
 * ==============================================================================
 * Tasks Pinia Store
 * Manages the state for the Task Scheduler Widget (To-Do list).
 * Handles all standard CRUD (Create, Read, Update, Delete) operations asynchronously.
 * ==============================================================================
 */
export const useTasksStore = defineStore('tasks', {
  state: () => ({
    collection: [], // Array holding all task objects retrieved from the DB
    loading: false, // Flag to show a loading state in the UI
    error: null,    // Stores any error messages
  }),
  actions: {
    async fetchTasks() {
      // Fetch all tasks belonging to the current user
      this.loading = true;
      try {
        const response = await api.get('/api/dashboard/tasks/');
        this.collection = response.data;
      } catch (err) {
        this.error = 'Failed to fetch tasks';
      } finally {
        this.loading = false;
      }
    },
    async addTask(taskData) {
      // Send a new task to the backend and append the newly created task to our local collection
      try {
        const response = await api.post('/api/dashboard/tasks/', taskData);
        this.collection.push(response.data);
      } catch (err) {
        this.error = 'Failed to add task';
      }
    },
    async updateTask(id, taskData) {
      // Update an existing task (e.g. toggling 'completed' status)
      try {
        const response = await api.put(`/api/dashboard/tasks/${id}/`, taskData);
        
        // Find the task in our local array and replace it with the updated version from the server
        const index = this.collection.findIndex(t => t.id === id);
        if (index !== -1) {
          this.collection[index] = response.data;
        }
      } catch (err) {
        this.error = 'Failed to update task';
      }
    },
    async deleteTask(id) {
      // Tell the server to delete the task, then remove it from our local array
      try {
        await api.delete(`/api/dashboard/tasks/${id}/`);
        
        // Filter out the task with the matching ID
        this.collection = this.collection.filter(t => t.id !== id);
      } catch (err) {
        this.error = 'Failed to delete task';
      }
    }
  },
});
