<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">My Applications</h5>

      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border spinner-border-sm text-primary" role="status"></div>
      </div>

      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <p v-else-if="applications.length === 0" class="text-muted mb-0">
        You haven't applied to any drives yet.
      </p>

      <table v-else class="table table-hover align-middle">
        <thead>
          <tr>
            <th>Drive</th>
            <th>Company</th>
            <th>Status</th>
            <th>Applied On</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications" :key="app.id">
            <td>{{ app.drive_title }}</td>
            <td>{{ app.company_name }}</td>
            <td>
              <span class="badge" :class="statusBadgeClass(app.status)">{{ app.status }}</span>
            </td>
            <td>{{ formatDate(app.applied_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import studentService from '@/services/studentService'

export default {
  name: 'MyApplications',
  data() {
    return {
      applications: [],
      loading: true,
      error: null
    }
  },
  created() {
    this.fetchApplications()
  },
  methods: {
    async fetchApplications() {
      this.loading = true
      this.error = null
      try {
        const response = await studentService.getMyApplications()
        this.applications = response.data
      } catch (err) {
        this.error = 'Failed to load your applications.'
      } finally {
        this.loading = false
      }
    },
    formatDate(iso) {
      if (!iso) return '—'
      return new Date(iso).toLocaleDateString()
    },
    statusBadgeClass(status) {
      return {
        applied: 'bg-secondary',
        shortlisted: 'bg-info text-dark',
        interview: 'bg-warning text-dark',
        selected: 'bg-success',
        rejected: 'bg-danger'
      }[status] || 'bg-secondary'
    }
  }
}
</script>