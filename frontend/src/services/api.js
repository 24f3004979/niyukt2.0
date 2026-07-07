// src/services/api.js
import axios from 'axios';
import router from '@/router';

// 1. Re-create your custom instance with your exact required port
const api = axios.create({
  baseURL: 'http://localhost:8080/', // 🚀 Your required base URL
  timeout: 10000,
});

// 2. Outgoing Request Middleware: Automatically attach tokens
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 3. Incoming Response Middleware: Global security gatekeeper
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
      localStorage.clear();
      router.push('/auth').catch(() => {}); // Safely redirect back to our unified tab page
    }
    return Promise.reject(error);
  }
);

export default api;

