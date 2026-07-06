import { defineStore } from 'pinia';
import api from '../services/api';

/**
 * ==============================================================================
 * Weather Pinia Store
 * Pinia is the official state management library for Vue.js. Think of it as a 
 * central data bank that any component in our app can access.
 * This store handles fetching and caching the weather data from our Django backend.
 * ==============================================================================
 */
export const useWeatherStore = defineStore('weather', {
  // `state` is where we define the data properties this store will hold.
  state: () => ({
    data: null,      // Holds the JSON response from the API
    loading: false,  // True when we are waiting for a response (useful for loading spinners)
    error: null,     // Holds any error messages to display to the user
  }),
  
  // `actions` are methods that modify the state. They can be asynchronous!
  actions: {
    async fetchWeather(lat, lon) {
      // 1. Set loading to true and clear any previous errors before making the request
      this.loading = true;
      this.error = null;
      try {
        // 2. Make the HTTP GET request to our Django Weather Proxy endpoint
        const response = await api.get(`/api/dashboard/weather/?lat=${lat}&lon=${lon}`);
        // 3. Save the successful data into the state
        this.data = response.data;
      } catch (err) {
        // 4. If the server returns an error (e.g. 400 or 503), catch it and save the message
        this.error = err.response?.data?.error || 'Failed to fetch weather';
      } finally {
        // 5. Regardless of success or failure, we are no longer loading
        this.loading = false;
      }
    },
    async fetchWeatherByCity(cityName) {
      this.loading = true;
      this.error = null;
      try {
        const geoResponse = await fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(cityName)}&count=1`);
        const geoData = await geoResponse.json();
        
        if (!geoData.results || geoData.results.length === 0) {
          throw new Error('City not found');
        }
        
        const { latitude, longitude, name } = geoData.results[0];
        
        // Save to localStorage
        localStorage.setItem('weather_city', name);
        localStorage.setItem('weather_lat', latitude);
        localStorage.setItem('weather_lon', longitude);
        
        // Fetch actual weather using our backend proxy
        await this.fetchWeather(latitude, longitude);
      } catch (err) {
        this.error = err.message || 'Failed to fetch city data';
        this.loading = false;
      }
    },
    loadSavedLocation() {
      const savedCity = localStorage.getItem('weather_city');
      const savedLat = localStorage.getItem('weather_lat');
      const savedLon = localStorage.getItem('weather_lon');
      
      // Guard against invalid/corrupt values in localStorage
      if (savedLat === 'NaN' || savedLon === 'NaN' || savedLat === 'undefined' || savedLon === 'undefined') {
        localStorage.removeItem('weather_city');
        localStorage.removeItem('weather_lat');
        localStorage.removeItem('weather_lon');
        return null;
      }
      
      if (savedCity && savedLat && savedLon) {
        this.fetchWeather(savedLat, savedLon);
        return savedCity;
      }
      return null;
    }
  },
});
