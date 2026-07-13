<template>
  <div>
    <div v-if="loading" class="text-center py-3">
      <div class="spinner-border spinner-border-sm text-primary" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <p v-else-if="applications.length === 0" class="text-muted mb-0">
      No applicants yet.
    </p>

    <table v-else class="table table-sm table-bordered align-middle mb-0">
      <thead>
        <tr>
          <th>Student</th>
          <th>Current Status</th>
          <th>Set Status</th>
          <th>Resume</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="app in applications" :key="app.id">
          <td>{{ app.student_name }}</td>
          <td>
            <span class="badge" :class="statusBadgeClass(app.status)">{{ app.status }}</span>
          </td>
          <td>
            <select class="form-select form-select-sm" v-model="app.pendingStatus">
              <option v-for="s in statuses" :key="s" :value="s">{{ s }}</option>
            </select>
          </td>
          <td>
            <button
              v-if="app.student_has_resume"
              class="btn btn-sm btn-outline-secondary"
              @click="downloadResume(app)"
            >
              Download
            </button>
            <span v-else class="text-muted small">Not uploaded</span>
          </td>
          <td>
            <button
              class="btn btn-sm btn-primary"
              :disabled="app.pendingStatus === app.status || updatingId === app.id"
              @click="updateStatus(app)"
            >
              Update
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import companyService from '@/services/companyService'

export default {
  name: 'ApplicantsList',
  props: {
    driveId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      applications: [],
      loading: true,
      error: null,
      updatingId: null,
      statuses: ['applied', 'shortlisted', 'interview', 'selected', 'rejected']
    }
  },
  created() {
    this.fetchApplicants()
  },
  methods: {
    async fetchApplicants() {
      this.loading = true
      this.error = null
      try {
        const response = await companyService.getApplicationsForDrive(this.driveId)
        this.applications = response.data.map(a => ({ ...a, pendingStatus: a.status }))
      } catch (err) {
        this.error = err.response?.data?.error?.message || 'Failed to load applicants.'
      } finally {
        this.loading = false
      }
    },
    async updateStatus(app) {
      this.updatingId = app.id
      this.error = null
      try {
        const response = await companyService.updateApplicationStatus(app.id, { status: app.pendingStatus })
        app.status = response.data.data.status
      } catch (err) {
        this.error = err.response?.data?.error?.message || 'Failed to update status.'
      } finally {
        this.updatingId = null
      }
    },
    async downloadResume(app) {
      try {
        const response = await companyService.downloadApplicantResume(app.id)
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `${app.student_name}_resume`)
        document.body.appendChild(link)
        link.click()
        link.remove()
      } catch (err) {
        this.error = 'Failed to download resume.'
      }
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