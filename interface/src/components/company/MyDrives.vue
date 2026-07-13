<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">My Drives</h5>

      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border spinner-border-sm text-primary" role="status"></div>
      </div>

      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <p v-else-if="drives.length === 0" class="text-muted mb-0">
        You haven't created any drives yet.
      </p>

      <div v-else>
        <div v-for="drive in drives" :key="drive.id" class="border rounded p-3 mb-3">
          <div class="d-flex justify-content-between align-items-start">
            <div>
              <h6 class="mb-1">{{ drive.title }}</h6>
              <span class="badge" :class="statusBadgeClass(drive.status)">{{ drive.status }}</span>
              <span v-if="drive.status === 'pending'" class="text-muted small ms-2">
                Awaiting admin approval
              </span>
            </div>
            <button
              v-if="drive.status === 'approved'"
              class="btn btn-sm btn-outline-primary"
              @click="toggleApplicants(drive.id)"
            >
              {{ expandedDriveId === drive.id ? 'Hide Applicants' : 'View Applicants' }}
            </button>
          </div>

          <ApplicantsList
            v-if="expandedDriveId === drive.id"
            :drive-id="drive.id"
            class="mt-3"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import companyService from '@/services/companyService'
import ApplicantsList from './ApplicantsList.vue'

export default {
  name: 'MyDrives',
  components: { ApplicantsList },
  data() {
    return {
      drives: [],
      loading: true,
      error: null,
      expandedDriveId: null
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
        const response = await companyService.getMyDrives()
        this.drives = response.data
      } catch (err) {
        this.error = 'Failed to load your drives.'
      } finally {
        this.loading = false
      }
    },
    toggleApplicants(driveId) {
      this.expandedDriveId = this.expandedDriveId === driveId ? null : driveId
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