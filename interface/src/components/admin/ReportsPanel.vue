<!-- frontend/src/components/admin/ReportsPanel.vue -->
<template>
  <div class="reports-panel">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h6 class="mb-0">Monthly Reports</h6>
      <button
        class="btn btn-primary btn-sm"
        :disabled="generating"
        @click="generateNow"
      >
        <span v-if="generating" class="spinner-border spinner-border-sm me-1"></span>
        {{ generating ? "Generating..." : "Generate Now" }}
      </button>
    </div>

    <div v-if="generateError" class="alert alert-danger py-2">
      {{ generateError }}
    </div>
    <div v-if="generateSuccess" class="alert alert-success py-2">
      Report generated successfully.
    </div>

    <div v-if="loading" class="text-center py-4">
      <div class="spinner-border" role="status"></div>
    </div>

    <table v-else class="table table-hover align-middle">
      <thead>
        <tr>
          <th>Period</th>
          <th>Generated At</th>
          <th>Status</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="report in reports" :key="report.id">
          <td>{{ report.period_start }} to {{ report.period_end }}</td>
          <td>{{ formatDate(report.generated_at) }}</td>
          <td>
            <span :class="statusBadgeClass(report.status)">
              {{ report.status }}
            </span>
          </td>
          <td>
            <a
              v-if="report.status === 'completed'"
              class="btn btn-sm btn-outline-primary"
              :href="downloadUrl(report.id)"
              target="_blank"
            >
              Download
            </a>
          </td>
        </tr>
        <tr v-if="reports.length === 0">
          <td colspan="4" class="text-center text-muted py-3">
            No reports generated yet.
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import reportService from "@/services/reportService";

const POLL_INTERVAL_MS = 3000;
const POLL_TIMEOUT_MS = 60000;

export default {
  name: "ReportsPanel",

  data() {
    return {
      reports: [],
      loading: true,
      generating: false,
      generateError: null,
      generateSuccess: false,
    };
  },

  created() {
    this.fetchReports();
  },

  methods: {
    async fetchReports() {
      this.loading = true;
      try {
        const response = await reportService.listReports();
        this.reports = response.data.data.reports;
      } catch (err) {
        this.generateError =
          err.response?.data?.error?.message || "Failed to load reports.";
      } finally {
        this.loading = false;
      }
    },

    async generateNow() {
      this.generating = true;
      this.generateError = null;
      this.generateSuccess = false;

      try {
        const response = await reportService.generateReportNow();
        const taskId = response.data.data.task_id;
        await this.pollTask(taskId);
        this.generateSuccess = true;
        await this.fetchReports();
      } catch (err) {
        this.generateError =
          err.response?.data?.error?.message || "Failed to generate report.";
      } finally {
        this.generating = false;
        setTimeout(() => (this.generateSuccess = false), 4000);
      }
    },

    pollTask(taskId) {
      const start = Date.now();
      return new Promise((resolve, reject) => {
        const check = async () => {
          if (Date.now() - start > POLL_TIMEOUT_MS) {
            reject(new Error("Report generation timed out."));
            return;
          }
          try {
            const res = await reportService.getReportTaskStatus(taskId);
            const status = res.data.data.status;
            if (status === "SUCCESS") {
              resolve();
            } else if (status === "FAILURE") {
              reject(new Error("Report generation failed."));
            } else {
              setTimeout(check, POLL_INTERVAL_MS);
            }
          } catch (err) {
            reject(err);
          }
        };
        check();
      });
    },

    downloadUrl(reportId) {
      return reportService.downloadReportUrl(reportId);
    },

    formatDate(iso) {
      if (!iso) return "";
      return new Date(iso).toLocaleString();
    },

    statusBadgeClass(status) {
      return {
        completed: "badge bg-success",
        queued: "badge bg-warning text-dark",
        failed: "badge bg-danger",
      }[status] || "badge bg-secondary";
    },
  },
};
</script>