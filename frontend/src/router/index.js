/**
 * ============================================================================
 * VUE ROUTER CONFIGURATION
 * ============================================================================
 * The Router is like the GPS for our Single Page Application (SPA).
 * It watches the URL in the browser (e.g., localhost:5173/settings) and decides 
 * which Vue Component to show on the screen, without actually reloading the webpage!
 */

import { createRouter, createWebHistory } from 'vue-router';
// We need the authStore so the router can check if someone is logged in before letting them into private pages.
import { useAuthStore } from '../stores/authStore';

// Import all the "Views" (full-page components) we want to navigate between.
import FinanceView from '../views/FinanceView.vue';
import TasksView from '../views/TasksView.vue';
import NotesView from '../views/NotesView.vue';
import WeatherView from '../views/WeatherView.vue';
import TransactionsView from '../views/TransactionsView.vue';
import CategoriesView from '../views/CategoriesView.vue';
import AppSettingsView from '../views/AppSettingsView.vue';
import AuthView from '../views/AuthView.vue';
import EventsView from '../views/EventsView.vue';
import MainLayout from '../components/layout/MainLayout.vue';

// 1. Define the Routes
// A list of rules that pair a URL path with a specific Vue component.
const routes = [
  // PUBLIC ROUTE: Anyone can go to '/login' to see the AuthView (Login/Register).
  { path: '/login', component: AuthView, name: 'auth' },
  
  // PRIVATE ROUTES: These routes are wrapped inside the 'MainLayout' component.
  // MainLayout provides the persistent Sidebar and Header.
  { 
    path: '/', 
    component: MainLayout, 
    // "meta" is a place to attach custom rules. Here, we tag this route as requiring authentication.
    meta: { requiresAuth: true },
    
    // "children" routes will be rendered INSIDE the MainLayout's <router-view> tag.
    children: [
      { path: '', component: FinanceView, name: 'finance' }, // The default page (/)
      { path: 'tasks', component: TasksView, name: 'tasks' },
      { path: 'notes', component: NotesView, name: 'notes' },
      { path: 'weather', component: WeatherView, name: 'weather' },
      { path: 'events', component: EventsView, name: 'events' },
      { path: 'transactions', component: TransactionsView, name: 'transactions' }, // (/transactions)
      { path: 'categories', component: CategoriesView, name: 'categories' },
      { path: 'settings', component: AppSettingsView, name: 'settings' }, // (/settings)
    ]
  },
];

// 2. Create the Router instance
const router = createRouter({
  // createWebHistory gives us normal-looking URLs (e.g., /settings instead of /#/settings)
  history: createWebHistory(),
  routes
});

// 3. Navigation Guards (The Bouncer)
// `router.beforeEach` runs EVERY SINGLE TIME the user clicks a link or changes the URL, 
// BEFORE the new page is actually loaded.
router.beforeEach((to, from) => {
  // `to` = the page they are trying to go to
  // `from` = the page they are currently on
  
  const authStore = useAuthStore();
  
  // Quick check to see if there's a token saved in Local Storage.
  authStore.verifyToken();

  // RULE 1: If the page requires auth (meta.requiresAuth === true) AND the user is NOT logged in...
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // ...kick them out and force them to the login page!
    return '/login';
  } 
  
  // RULE 2: If the user IS logged in, but they try to go back to the login page...
  else if (to.path === '/login' && authStore.isAuthenticated) {
    // ...redirect them to the dashboard, because they don't need to log in again!
    return '/';
  } 
  
  // RULE 3: If neither of the above rules apply, let them pass!
  // Returning nothing just means "proceed as normal".
});

// Finally, export the router so we can plug it into our app in main.js
export default router;
