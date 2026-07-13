<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">Available Drives</h5>

      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border spinner-border-sm text-primary" role="status"></div>
      </div>

      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <p v-else-if="drives.length === 0" class="text-muted mb-0">
        No drives open for applications right now.
      </p>

      <div v-else class="row g-3">
        <div class="col-md-6" v-for="drive in drives" :key="drive.id">
          <div class="card h-100">
            <div class="card-body d-flex flex-column">
              <h6 class="card-title">{{ drive.title }}</h6>
              <h6 class="card-subtitle mb-2 text-muted">{{ drive.company_name }}</h6>
              <p class="card-text small">{{ drive.description }}</p>
              <p class="mb-1" v-if="drive.role_offered"><strong>Role:</strong> {{ drive.role_offered }}</p>
              <p class="mb-1" v-if="drive.package_ctc"><strong>Package:</strong> {{ drive.package_ctc }} LPA</p>
              <p class="mb-3" v-if="drive.eligibility_criteria">
                <strong>Eligibility:</strong> {{ drive.eligibility_criteria }}
              </p>
              <div class="mt-auto">
                <button
                  class="btn btn-primary btn-sm"
                  :disabled="applyingId === drive.id || appliedIds.includes(drive.id)"
                  @click="apply(drive.id)"
                >
                  {{ appliedIds.includes(drive.id) ? 'Applied' : (applyingId === drive.id ? 'Applying...' : 'Apply') }}
                </button>
                <div v-if="applyErrorId === drive.id" class="text-danger small mt-2">
                  {{ applyErrorMessage }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import studentService from '@/services/studentService'

export default {
  name: 'AvailableDrives',
  data() {
    return {
      drives: [],
      appliedIds: [],
      loading: true,
      error: null,
      applyingId: null,
      applyErrorId: null,
      applyErrorMessage: ''
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      this.loading = true
      this.error = null
      try {
        const [drivesRes, applicationsRes] = await Promise.all([
          studentService.getOpenDrives(),
          studentService.getMyApplications()
        ])
        this.drives = drivesRes.data
        this.appliedIds = applicationsRes.data.map(a => a.drive_id)
      } catch (err) {
        this.error = 'Failed to load drives.'
      } finally {
        this.loading = false
      }
    },
    async apply(driveId) {
      this.applyingId = driveId
      this.applyErrorId = null
      try {
        await studentService.applyToDrive(driveId)
        this.appliedIds.push(driveId)
        this.$emit('applied')
      } catch (err) {
        this.applyErrorId = driveId
        this.applyErrorMessage = err.response?.data?.error?.message || 'Failed to apply.'
      } finally {
        this.applyingId = null
      }
    }
  }
}
</script>