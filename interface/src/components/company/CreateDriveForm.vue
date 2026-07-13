<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">Create a New Drive</h5>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div v-if="success" class="alert alert-success">Drive submitted for approval.</div>

      <form @submit.prevent="submit">
        <div class="mb-3">
          <label class="form-label">Title</label>
          <input type="text" class="form-control" v-model="form.title" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Description</label>
          <textarea class="form-control" rows="3" v-model="form.description"></textarea>
        </div>
        
        <div class="mb-3">
          <label class="form-label">Package (CTC, LPA)</label>
          <input type="number" step="0.1" class="form-control" v-model.number="form.package_ctc" />
        </div>
        <button type="submit" class="btn btn-primary" :disabled="submitting">
          {{ submitting ? 'Submitting...' : 'Submit for Approval' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import companyService from '@/services/companyService'

export default {
  name: 'CreateDriveForm',
  data() {
    return {
      form: {
        title: '',
        description: '',
        package_ctc: null
      },
      submitting: false,
      error: null,
      success: false
    }
  },
  methods: {
    async submit() {
      this.submitting = true
      this.error = null
      this.success = false
      try {
        await companyService.createDrive(this.form)
        this.success = true
        this.form = { title: '', description: '', package_ctc: null }
        this.$emit('created')
      } catch (err) {
        this.error = err.response?.data?.error?.message || 'Failed to create drive.'
      } finally {
        this.submitting = false
      }
    }
  }
}
</script>