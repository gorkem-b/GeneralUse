import { defineStore } from 'pinia';
import api from '../services/api';

export const useNotificationsStore = defineStore('notifications', {
  state: () => ({
    notifications: [],
    isPolling: false,
  }),
  actions: {
    async startPolling() {
      if (this.isPolling) return;
      this.isPolling = true;
      
      while (this.isPolling) {
        try {
          // Long polling request. Will block up to 30s.
          const response = await api.get('/api/notifications/poll/');
          
          if (response.data && response.data.length > 0) {
            // Add new notifications
            this.notifications.push(...response.data);
            
            // Mark them as read on the server so they aren't fetched again
            const ids = response.data.map(n => n.id);
            await api.post('/api/notifications/mark-read/', { ids });
          }
          
          // Wait 5 seconds before making the next request
          await new Promise(resolve => setTimeout(resolve, 5000));
        } catch (error) {
          console.error("Notification Polling Error:", error);
          
          // If we receive a 401 Unauthorized, our token is dead.
          // Stop polling immediately to prevent spamming the backend!
          if (error.response && error.response.status === 401) {
            this.stopPolling();
            break;
          }
          
          // If it's a different error (e.g. server restart), wait 5 seconds before retrying
          await new Promise(resolve => setTimeout(resolve, 5000));
        }
      }
    },
    stopPolling() {
      this.isPolling = false;
    },
    clearNotification(id) {
      this.notifications = this.notifications.filter(n => n.id !== id);
    }
  }
});
