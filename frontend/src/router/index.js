// Routing given pages to their dedicated unit

import Vue from 'vue';
import VueRouter from 'vue-router';

// Import your unified view page layout wrappers
import AuthView from '@/views/AuthView.vue';
import DashboardView from '@/views/DashboardView.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    redirect: '/auth' // Send root visitors directly to the auth screen
  },
  {
    path: '/auth',
    name: 'Authentication',
    component: AuthView // Loads your tab switcher wrapper into App.vue
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView // Loads your dashboard wrapper into App.vue
  }
];

const router = new VueRouter({
  mode: 'history',
  routes
});

export default router;

