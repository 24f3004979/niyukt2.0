<template>
  <div class="container mt-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h1 class="mb-0">Placement Portal Dashboard</h1>
        <p class="text-muted mb-0" v-if="user">
          Welcome, {{ user.username }}
          <span class="badge bg-secondary text-uppercase ms-2">{{ user.role }}</span>
        </p>
      </div>
      <button class="btn btn-outline-danger" @click="logout">Logout</button>
    </div>

    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else>
      <AdminDashboard v-if="user.role === 'admin'" />

      <div v-else class="card">
        <div class="card-body">
          <h5 class="card-title text-capitalize">{{ user.role }} Dashboard</h5>
          <p class="card-text text-muted mb-0">
            This section is coming next — drives, applications, and profile management.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import userService from '@/services/userService'
import AdminDashboard from '@/components/admin/AdminDashboard.vue'

export default {
  name: 'DashboardView',
  components: { AdminDashboard },
  data() {
    return {
      user: null,
      loading: true,
      error: null
    }
  },
  created() {
    this.fetchUser()
  },
  methods: {
    async fetchUser() {
      this.loading = true
      this.error = null
      try {
        const response = await userService.getCurrentUser()
        this.user = response.data
      } catch (err) {
        this.error = 'Could not load your account details. Please try logging in again.'
      } finally {
        this.loading = false
      }
    },
    logout() {
      localStorage.removeItem('token')
      this.$router.push('/login')
    }
  }
}
</script>
