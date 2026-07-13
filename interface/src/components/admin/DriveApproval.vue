<template>
  <div class="card">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h5 class="card-title mb-0">Drives</h5>
        <select class="form-select form-select-sm w-auto" v-model="statusFilter" @change="fetchDrives">
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
          <option value="">All</option>
        </select>
      </div>

      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border spinner-border-sm text-primary" role="status"></div>
      </div>

      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <p v-else-if="drives.length === 0" class="text-muted mb-0">No drives found.</p>

      <table v-else class="table table-hover align-middle">
        <thead>
          <tr>
            <th>Title</th>
            <th>Company</th>
            <th>Package (CTC)</th>
            <th>Status</th>
            <th class="text-end">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="drive in drives" :key="drive.id">
            <td>{{ drive.title }}</td>
            <td>{{ drive.company_name }}</td>
            <td>{{ drive.package_ctc ?? '—' }}</td>
            <td>
              <span class="badge" :class="statusBadgeClass(drive.status)">
                {{ drive.status }}
              </span>
            </td>
            <td class="text-end">
              <template v-if="drive.status === 'pending'">
                <button
                  class="btn btn-sm btn-success me-2"
                  :disabled="actionInProgress === drive.id"
                  @click="approve(drive.id)"
                >
                  Approve
                </button>
                <button
                  class="btn btn-sm btn-outline-danger"
                  :disabled="actionInProgress === drive.id"
                  @click="reject(drive.id)"
                >
                  Reject
                </button>
              </template>
              <span v-else class="text-muted small">No actions</span>
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
  name: 'DriveApproval',
  data() {
    return {
      drives: [],
      statusFilter: 'pending',
      loading: true,
      error: null,
      actionInProgress: null
    }
  },
  created() {
    this.fetchDrives()
  },
  methods: {
    async fetchDrives() {
      this.loading = true
      this.error = null
      try {
        const response = await adminService.getAllDrives(this.statusFilter)
        this.drives = response.data
      } catch (err) {
        this.error = 'Failed to load drives.'
      } finally {
        this.loading = false
      }
    },
    async approve(id) {
      this.actionInProgress = id
      try {
        await adminService.approveDrive(id)
        this.drives = this.drives.filter(d => d.id !== id)
        this.$emit('updated')
      } catch (err) {
        this.error = err.response?.data?.error?.message || 'Failed to approve drive.'
      } finally {
        this.actionInProgress = null
      }
    },
    async reject(id) {
      this.actionInProgress = id
      try {
        await adminService.rejectDrive(id)
        this.drives = this.drives.filter(d => d.id !== id)
        this.$emit('updated')
      } catch (err) {
        this.error = err.response?.data?.error?.message || 'Failed to reject drive.'
      } finally {
        this.actionInProgress = null
      }
    },
    statusBadgeClass(status) {
      return {
        pending: 'bg-warning text-dark',
        approved: 'bg-success',
        rejected: 'bg-danger'
      }[status] || 'bg-secondary'
    }
  }
}
</script>