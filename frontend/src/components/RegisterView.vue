<template>
  <div>
    <h3 class="text-center mb-4">Create Account</h3>
    <form @submit.prevent="submitRegister">
      <div class="mb-3">
        <label class="form-label">Username</label>
        <input type="text" class="form-control" v-model="username" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Password</label>
        <input type="password" class="form-control" v-model="password" required />
      </div>

      <div class="mb-3">
        <div class="form-check">
          <input
            class="form-check-input"
            type="radio"
            value="student"
            v-model="role"
            id="roleStudent"
          />
          <label class="form-check-label" for="roleStudent">
            I am a Student
          </label>
        </div>
        <div class="form-check">
          <input
            class="form-check-input"
            type="radio"
            value="company"
            v-model="role"
            id="roleCompany"
          />
          <label class="form-check-label" for="roleCompany">
            I am a Company Representative
          </label>
        </div>
      </div>

      <button type="submit" class="btn btn-primary w-100" :disabled="loading">
        <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
        <strong> REGISTER NOW </strong>
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
      role: 'student',
      errorMessage: '',
      successMessage: '',
      loading: false
    };
  },
  methods: {
    async submitRegister() {
      this.errorMessage = '';
      this.successMessage = '';
      this.loading = true;

      try {
        await axios.post(
          'api/register',
          {
            username: this.username,
            password: this.password,
            role: this.role
          },
          { headers: { 'Content-Type': 'application/json' } }
        );

        this.successMessage = 'Registration complete! You can switch tabs to log in.';
        this.username = '';
        this.password = '';
      } catch (err) {
        this.errorMessage = err.response?.data?.error || 'Registration service unreachable.';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
