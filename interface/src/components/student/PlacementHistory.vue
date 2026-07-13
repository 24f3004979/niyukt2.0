<!-- frontend/src/components/student/PlacementHistory.vue -->
<!--
  Assumes a `placementService.getHistoryForStudent()` (or similar) already
  exists from Phase 3 for the table data. This component adds the CSV
  download button using the blob-response pattern.
-->
<template>
  <div class="placement-history">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h6 class="mb-0">My Placement History</h6>
      <button
        class="btn btn-outline-primary btn-sm"
        :disabled="downloading"
        @click="downloadCsv"
      >
        <span v-if="downloading" class="spinner-border spinner-border-sm me-1"></span>
        {{ downloading ? "Preparing..." : "Download CSV" }}
      </button>
    </div>

    <div v-if="downloadError" class="alert alert-danger py-2">
      {{ downloadError }}
    </div>

    <table class="table table-hover align-middle">
      <thead>
        <tr>
          <th>Drive</th>
          <th>Company</th>
          <th>Status</th>
          <th>Package (CTC)</th>
          <th>Updated</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="entry in history" :key="entry.id">
          <td>{{ entry.drive_title }}</td>
          <td>{{ entry.company_name }}</td>
          <td>
            <span :class="statusBadgeClass(entry.status)">{{ entry.status }}</span>
          </td>
          <td>{{ entry.package_ctc || "-" }}</td>
          <td>{{ formatDate(entry.recorded_at) }}</td>
        </tr>
        <tr v-if="history.length === 0">
          <td colspan="5" class="text-center text-muted py-3">
            No placement activity yet.
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import reportService from "@/services/reportService";
// import placementService from "@/services/placementService"; // Phase 3

export default {
  name: "PlacementHistory",

  data() {
    return {
      history: [],
      downloading: false,
      downloadError: null,
    };
  },

  created() {
    this.fetchHistory();
  },

  methods: {
    async fetchHistory() {
      // Wire up once Phase 3's placementService exists:
      // const response = await placementService.getHistoryForStudent();
      // this.history = response.data.data;
    },

    async downloadCsv() {
      this.downloading = true;
      this.downloadError = null;
      try {
        const response = await reportService.downloadStudentHistoryCsv();
        const blob = new Blob([response.data], { type: "text/csv" });
        const url = window.URL.createObjectURL(blob);

        const link = document.createElement("a");
        link.href = url;
        link.download = "placement_history.csv";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      } catch (err) {
        this.downloadError = "Failed to download your placement history.";
      } finally {
        this.downloading = false;
      }
    },

    formatDate(iso) {
      if (!iso) return "";
      return new Date(iso).toLocaleDateString();
    },

    statusBadgeClass(status) {
      return {
        applied: "badge bg-secondary",
        shortlisted: "badge bg-primary",
        interview: "badge bg-warning text-dark",
        selected: "badge bg-success",
        rejected: "badge bg-danger",
      }[status] || "badge bg-light text-dark";
    },
  },
};
</script>