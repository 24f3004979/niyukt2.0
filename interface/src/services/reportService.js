// frontend/src/services/reportService.js
//
// Mirrors the adminService.js / userService.js pattern: thin wrapper around
// the shared api.js axios instance, no component ever calls axios directly.

import api from "@/services/api";

export default {
  getAnalytics(monthsBack = 6) {
    return api.get("/admin/analytics", { params: { months_back: monthsBack } });
  },

  listReports(page = 1, perPage = 20) {
    return api.get("/admin/reports", { params: { page, per_page: perPage } });
  },

  generateReportNow() {
    return api.post("/admin/reports/generate-now");
  },

  getReportTaskStatus(taskId) {
    return api.get(`/admin/reports/task/${taskId}`);
  },

  downloadReportUrl(reportId) {
    // Used directly as an <a href> / window.open target since it's a
    // file stream response, not JSON.
    return `${api.defaults.baseURL}/admin/reports/${reportId}/download`;
  },

  downloadStudentHistoryCsv() {
    // responseType "blob" so axios doesn't try to parse the CSV as JSON.
    return api.get("/students/placement-history/csv", { responseType: "blob" });
  },
};