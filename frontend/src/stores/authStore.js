/**
 * ============================================================================
 * AUTHENTICATION STORE (PINIA)
 * ============================================================================
 * Pinia is the official state management library for Vue.
 * Think of this file like a "global brain" for the app that remembers 
 * whether the user is logged in, what their token is, and provides functions 
 * to log them in or out.
 */

import { defineStore } from 'pinia';
// Import our custom axios postman we created in api.js
import api from '../services/api';

// defineStore creates our "global brain" and names it 'auth'
export const useAuthStore = defineStore('auth', {
  
  // 1. STATE: The variables that the brain remembers.
  state: () => ({
    // The currently logged-in user object (e.g., { username: 'testuser' })
    user: null,
    
    // We check the browser's Local Storage to see if a token was saved from a previous visit.
    // If it was, we load it. Otherwise, it's null.
    accessToken: localStorage.getItem('access_token') || null,
    
    // A quick boolean (true/false) to know if the user is currently authenticated.
    // "!!" is a JavaScript trick that converts a value into a strict true or false.
    isAuthenticated: !!localStorage.getItem('access_token'),
  }),
  
  // 2. ACTIONS: The functions that can modify the state (the brain's variables).
  actions: {
    
    /**
     * LOGIN ACTION
     * Sends the username/password to the backend, gets the token, and saves it.
     */
    async login(credentials) {
      // We send a POST request to the Django endpoint we set up earlier.
      // We wait (await) for the backend to respond with the JWT tokens.
      const response = await api.post('/api/token/', credentials);
      
      // We take the "access" token from the response and save it in our Pinia state...
      this.accessToken = response.data.access;
      // ...and we also save it directly into the browser's Local Storage so it survives page reloads!
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      
      // Update our state to reflect that the user is now officially logged in.
      this.isAuthenticated = true;
      this.user = { username: credentials.username };
    },
    
    /**
     * REGISTER ACTION
     * Creates a new user and then automatically logs them in.
     */
    async register(credentials) {
      // First, tell the backend to create the new account in the database.
      await api.post('/api/register/', credentials);
      
      // Second, reuse our login action from above to log them in automatically!
      await this.login(credentials);
    },
    
    /**
     * LOGOUT ACTION
     * Forgets the user, deletes the tokens, and sets authenticated to false.
     */
    logout() {
      // Erase the variables from Pinia state
      this.user = null;
      this.accessToken = null;
      this.isAuthenticated = false;
      
      // CRITICAL: Delete the physical tokens from the browser's memory, 
      // otherwise they'll still be logged in if they refresh the page!
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    },
    
    /**
     * VERIFY TOKEN ACTION
     * A helper function that just makes sure the Pinia state matches what's in Local Storage.
     * This is useful when the user first opens the app in a new tab.
     */
    verifyToken() {
      this.isAuthenticated = !!localStorage.getItem('access_token');
    }
  }
});
