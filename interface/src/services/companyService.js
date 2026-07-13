import api from './api'

export default {
  createDrive(payload) {
    return api.post('/company/drives', payload)
  },
  getMyDrives() {
    return api.get('/company/drives')
  },
  getApplicationsForDrive(driveId) {
    return api.get(`/company/drive/${driveId}/applications`)
  },
  getAllApplications() {
    return api.get('/company/applications')
  },
  updateApplicationStatus(applicationId, payload) {
    return api.put(`/company/application/${applicationId}/status`, payload)
  },
  downloadApplicantResume(applicationId) {
    return api.get(`/company/application/${applicationId}/resume`, { responseType: 'blob' })
  }
}