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
      <StudentDashboard v-else-if="user.role === 'student'" />
      <CompanyDashboard v-else-if="user.role === 'company'" />
    </div>
  </div>
</template>

<script>
import userService from '@/services/userService'
import AdminDashboard from '@/components/admin/AdminDashboard.vue'
import StudentDashboard from '@/components/student/StudentDashboard.vue'
import CompanyDashboard from '@/components/company/CompanyDashboard.vue'

export default {
  name: 'DashboardView',
  components: { AdminDashboard, StudentDashboard, CompanyDashboard },
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
        const backendMessage = err.response?.data?.error?.message
        if (err.response?.status === 401) {
          // token missing/expired/invalid -> send them back to login rather than
          // showing a dead-end error screen
          localStorage.removeItem('token')
          this.$router.push('/login')
          return
        }
        this.error = backendMessage || 'Could not load your account details. Please try again.'
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