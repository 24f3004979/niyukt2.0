import api from './api'

export default {
  // Drives
  getPendingDrives() {
    return api.get('/admin/drives/pending')
  },
  getAllDrives(status = '') {
    return api.get('/admin/drives', { params: status ? { status } : {} })
  },
  approveDrive(driveId) {
    return api.put(`/admin/drive/${driveId}/approve`)
  },
  rejectDrive(driveId, reason = '') {
    return api.put(`/admin/drive/${driveId}/reject`, { reason })
  },

  // Companies (registration approval)
  getPendingCompanies() {
    return api.get('/admin/companies/pending')
  },
  approveCompany(companyId) {
    return api.put(`/admin/company/${companyId}/approve`)
  },
  rejectCompany(companyId) {
    return api.put(`/admin/company/${companyId}/reject`)
  },

  // Users (listing + block/unblock)
  getAllStudents() {
    return api.get('/admin/students')
  },
  getAllCompanies() {
    return api.get('/admin/companies')
  },
  blockUser(userId) {
    return api.put(`/admin/user/${userId}/block`)
  },
  unblockUser(userId) {
    return api.put(`/admin/user/${userId}/unblock`)
  }
}
