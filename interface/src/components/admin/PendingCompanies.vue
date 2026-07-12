<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">Pending Company Approvals</h5>

      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border spinner-border-sm text-primary" role="status"></div>
      </div>

      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <p v-else-if="companies.length === 0" class="text-muted mb-0">
        No companies awaiting approval.
      </p>

      <table v-else class="table table-hover align-middle">
        <thead>
          <tr>
            <th>Username</th>
            <th>Email</th>
            <th class="text-end">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="company in companies" :key="company.id">
            <td>{{ company.username }}</td>
            <td>{{ company.email }}</td>
            <td class="text-end">
              <button
                class="btn btn-sm btn-success me-2"
                :disabled="actionInProgress === company.id"
                @click="approve(company.id)"
              >
                Approve
              </button>
              <button
                class="btn btn-sm btn-outline-danger"
                :disabled="actionInProgress === company.id"
                @click="reject(company.id)"
              >
                Reject
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import adminService from '@/services/adminService'

export default {
  name: 'PendingCompanies',
  data() {
    return {
      companies: [],
      loading: true,
      error: null,
      actionInProgress: null
    }
  },
  created() {
    this.fetchCompanies()
  },
  methods: {
    async fetchCompanies() {
      this.loading = true
      this.error = null
      try {
        const response = await adminService.getPendingCompanies()
        this.companies = response.data
      } catch (err) {
        this.error = 'Failed to load pending companies.'
      } finally {
        this.loading = false
      }
    },
    async approve(id) {
      this.actionInProgress = id
      try {
        await adminService.approveCompany(id)
        this.companies = this.companies.filter(c => c.id !== id)
        this.$emit('updated')
      } catch (err) {
        this.error = err.response?.data?.error?.message || 'Failed to approve company.'
      } finally {
        this.actionInProgress = null
      }
    },
    async reject(id) {
      this.actionInProgress = id
      try {
        await adminService.rejectCompany(id)
        this.companies = this.companies.filter(c => c.id !== id)
        this.$emit('updated')
      } catch (err) {
        this.error = err.response?.data?.error?.message || 'Failed to reject company.'
      } finally {
        this.actionInProgress = null
      }
    }
  }
}
</script>
