import { defineStore } from 'pinia';
import api from '../services/api';

export const useEventsStore = defineStore('events', {
  state: () => ({
    events: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchEvents() {
      this.loading = true;
      try {
        const response = await api.get('/api/dashboard/events/');
        this.events = response.data;
      } catch (error) {
        this.error = error.response?.data || error.message;
      } finally {
        this.loading = false;
      }
    },
    async createEvent(eventData) {
      try {
        const response = await api.post('/api/dashboard/events/', eventData);
        this.events.push(response.data);
        return response.data;
      } catch (error) {
        this.error = error.response?.data || error.message;
        throw error;
      }
    }
  }
});
