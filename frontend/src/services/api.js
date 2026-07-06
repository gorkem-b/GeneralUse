/**
 * ============================================================================
 * API SERVICE CONFIGURATION
 * ============================================================================
 * Think of this file like a dedicated postman that handles all communication 
 * between our Vue frontend and our Django backend. Instead of using raw `fetch`,
 * we use the `axios` library because it gives us powerful features like 
 * interceptors and automatic JSON conversion.
 */

import axios from 'axios';

// 1. Create a custom Axios "instance" called apiClient.
// This allows us to set default rules for EVERY request we send to the backend.
const apiClient = axios.create({
    // baseURL is the starting URL for all our API calls.
    // import.meta.env.VITE_API_URL lets us change this URL easily based on where 
    // the app is running (e.g., localhost during development, or a real website URL in production).
    baseURL: import.meta.env.VITE_API_URL || 'http://84.235.166.113:8000',
    
    // timeout tells axios to stop trying if the server doesn't respond in 10 seconds.
    timeout: 10000,
    
    // headers tell the server: "Hey, we are sending you JSON data!"
    headers: { 'Content-Type': 'application/json' }
});

// 2. Set up a "Request Interceptor".
// An interceptor is like a bouncer that checks every single HTTP request RIGHT BEFORE it leaves the frontend.
apiClient.interceptors.request.use(config => {
    // We check if the user has a JWT access token saved in their browser's Local Storage.
    const token = localStorage.getItem('access_token');
    
    // If they DO have a token, we attach it to the request's Authorization header.
    // It looks like this: "Authorization: Bearer <token_string_here>"
    // This acts like a digital ID card so the backend knows exactly who is making the request!
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Finally, we let the request proceed to the backend.
    return config;
});

// 3. Set up a "Response Interceptor".
// This catches any errors returned by the backend before they reach our components.
apiClient.interceptors.response.use(
    response => response,
    error => {
        // If the backend says "401 Unauthorized", it means our token is expired or invalid.
        if (error.response && error.response.status === 401) {
            // Clear the dead tokens from Local Storage
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            
            // If we aren't already on the login page, redirect the user so they can log in again.
            if (window.location.pathname !== '/login') {
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

// 4. Export the apiClient so other files (like our stores) can use it to make requests.
export default apiClient;
