<template>
  <div class="auth-form">
    <h3>Create Account</h3>
    <form @submit.prevent="submitRegister">
      <div>
        <label>Username</label>
        <input type="text" v-model="username" required />
      </div>
      <div>
        <label>Password</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Register Now</button>
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
    async submitRegister() {
      this.errorMessage = '';
      this.successMessage = '';
      
      try {
        await axios.post('http://127.0.0', {
          username: this.username,
          password: this.password,
          role: 'student' // Sets default role according to service specifications
        }, {
          headers: { 'Content-Type': 'application/json' }
        });
        
        this.successMessage = 'Registration complete! You can switch tabs to log in.';
        this.username = '';
        this.password = '';
      } catch (err) {
        this.errorMessage = err.response?.data?.error || 'Registration service unreachable.';
      }
    }
  }
};
</script>
