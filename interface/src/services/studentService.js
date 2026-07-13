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
  getMyPlacementHistory() {
    return api.get('/student/placement-history')
  }
}