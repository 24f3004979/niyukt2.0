import api from './api'

export default {
  getOpenDrives() {
    return api.get('/student/drives')
  },
  applyToDrive(driveId) {
    return api.post(`/student/drive/${driveId}/apply`)
  },
  getMyApplications() {
    return api.get('/student/applications')
  },
  uploadResume(file) {
    const formData = new FormData()
    formData.append('resume', file)
    return api.post('/student/resume', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}