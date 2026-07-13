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
  updateApplicationStatus(applicationId, payload) {
    return api.put(`/company/application/${applicationId}/status`, payload)
  }
}