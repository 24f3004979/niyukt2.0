// src/main.js
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import api from './services/api'; // Import our configured file

// This makes it available globally as this.$api
Vue.prototype.$api = api; 

new Vue({
  router,
  render: h => h(App)
}).$mount('#app');

