<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">My Resume</h5>
      <p class="text-muted small">
        PDF, DOC, or DOCX. Companies you apply to can view and download this.
      </p>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div v-if="success" class="alert alert-success">Resume uploaded successfully.</div>

      <input
        type="file"
        class="form-control mb-3"
        accept=".pdf,.doc,.docx"
        @change="onFileSelected"
      />

      <button class="btn btn-primary" :disabled="!selectedFile || uploading" @click="upload">
        {{ uploading ? 'Uploading...' : 'Upload Resume' }}
      </button>
    </div>
  </div>
</template>

<script>
import studentService from '@/services/studentService'

export default {
  name: 'ResumeUpload',
  data() {
    return {
      selectedFile: null,
      uploading: false,
      error: null,
      success: false
    }
  },
  methods: {
    onFileSelected(e) {
      this.selectedFile = e.target.files[0] || null
      this.success = false
      this.error = null
    },
    async upload() {
      if (!this.selectedFile) return
      this.uploading = true
      this.error = null
      this.success = false
      try {
        await studentService.uploadResume(this.selectedFile)
        this.success = true
        this.selectedFile = null
      } catch (err) {
        this.error = err.response?.data?.error?.message || 'Failed to upload resume.'
      } finally {
        this.uploading = false
      }
    }
  }
}
</script>