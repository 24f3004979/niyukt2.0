<template>
  <div class="auth-form">
    <h3>Account Login</h3>
    <form @submit.prevent="submitLogin">
      <div>
        <label>Username</label>
        <input type="text" v-model="username" required />
      </div>
      <div>
        <label>Password</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Sign In</button>
    </form>
    <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>
    <p v-if="successMessage" class="success-msg">{{ successMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
      successMessage: ''
    };
  },
  methods: {
    async submitLogin() {
      this.errorMessage = '';
      this.successMessage = '';
      
      try {
        const response = await axios.post('api/login', {
          username: this.username,
          password: this.password
        }, {
          headers: { 'Content-Type': 'application/json' }
        });
        
        // Save the web token into local storage session wrapper
        localStorage.setItem('user-token', response.data.token);
        this.successMessage = 'Logged in successfully! Token saved.';
      } catch (err) {
        this.errorMessage = err.response?.data?.error || 'Connection failed to auth api.';
      }
    }
  }
};
</script>
