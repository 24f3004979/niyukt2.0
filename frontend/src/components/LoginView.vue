<template>
  <div>
    <h3 class="text-center mb-4">Account Login</h3>
    <form @submit.prevent="submitLogin">
      <div class="mb-3">
        <label class="form-label">Username</label>
        <input type="text" class="form-control" v-model="username" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Password</label>
        <input type="password" class="form-control" v-model="password" required />
      </div>

      <button type="submit" class="btn btn-primary w-100" :disabled="loading">
        <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
        <strong> LOG IN </strong>
      </button>
    </form>

    <div v-if="errorMessage" class="alert alert-danger mt-3 py-2 mb-0">
      {{ errorMessage }}
    </div>
    <div v-if="successMessage" class="alert alert-success mt-3 py-2 mb-0">
      {{ successMessage }}
    </div>
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
      successMessage: '',
      loading: false
    };
  },
  methods: {
    async submitLogin() {
      this.errorMessage = '';
      this.successMessage = '';
      this.loading = true;

      try {
        const response = await axios.post(
          'api/login',
          { username: this.username, password: this.password },
          { headers: { 'Content-Type': 'application/json' } }
        );

        localStorage.setItem('user-token', response.data.token);
        this.successMessage = 'Logged in successfully! Token saved.';
      } catch (err) {
        this.errorMessage = err.response?.data?.error || 'Connection failed to auth api.';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
