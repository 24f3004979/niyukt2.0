<!-- frontend/src/components/admin/AnalyticsPanel.vue -->
<!--
  New tab for AdminDashboard.vue. Uses Chart.js directly (not the
  vue-chartjs wrapper) so it works the same regardless of Vue 2 vs Vue 3,
  and keeps full control over dual-axis config for the trend chart.

  npm install chart.js
-->
<template>
  <div class="analytics-panel">
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border" role="status"></div>
      <p class="mt-2">Loading analytics...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
      <button class="btn btn-sm btn-outline-danger ms-2" @click="fetchAnalytics">
        Retry
      </button>
    </div>

    <div v-else class="row g-4">
      <div class="col-md-6">
        <div class="card h-100">
          <div class="card-body">
            <h6 class="card-title">Application Status Breakdown</h6>
            <canvas ref="applicationChart"></canvas>
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card h-100">
          <div class="card-body">
            <h6 class="card-title">Drive Status Breakdown</h6>
            <canvas ref="driveChart"></canvas>
          </div>
        </div>
      </div>

      <div class="col-md-8">
        <div class="card h-100">
          <div class="card-body">
            <h6 class="card-title">Placement Trend ({{ monthsBack }} months)</h6>
            <canvas ref="trendChart"></canvas>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card h-100">
          <div class="card-body">
            <h6 class="card-title">Top Companies by Hires</h6>
            <canvas ref="topCompaniesChart"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js/auto";
import reportService from "@/services/reportService";

export default {
  name: "AnalyticsPanel",

  data() {
    return {
      loading: true,
      error: null,
      monthsBack: 6,
      charts: {}, // keep chart instances so we can destroy() on refresh/unmount
    };
  },

  created() {
    this.fetchAnalytics();
  },

  beforeUnmount() {
    this.destroyCharts();
  },
  // Vue 2 fallback lifecycle hook name — harmless no-op under Vue 3
  beforeDestroy() {
    this.destroyCharts();
  },

  methods: {
    async fetchAnalytics() {
      this.loading = true;
      this.error = null;
      try {
        const response = await reportService.getAnalytics(this.monthsBack);
        const data = response.data.data;
        this.$nextTick(() => this.renderCharts(data));
      } catch (err) {
        this.error =
          err.response?.data?.error?.message || "Failed to load analytics.";
      } finally {
        this.loading = false;
      }
    },

    destroyCharts() {
      Object.values(this.charts).forEach((chart) => chart && chart.destroy());
      this.charts = {};
    },

    renderCharts(data) {
      this.destroyCharts();

      this.charts.application = new Chart(this.$refs.applicationChart, {
        type: "bar",
        data: {
          labels: ["Applied", "Shortlisted", "Interview", "Selected", "Rejected"],
          datasets: [
            {
              label: "Applications",
              data: [
                data.application_status_breakdown.applied,
                data.application_status_breakdown.shortlisted,
                data.application_status_breakdown.interview,
                data.application_status_breakdown.selected,
                data.application_status_breakdown.rejected,
              ],
              backgroundColor: [
                "#6c757d", "#0d6efd", "#fd7e14", "#198754", "#dc3545",
              ],
            },
          ],
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
        },
      });

      this.charts.drive = new Chart(this.$refs.driveChart, {
        type: "doughnut",
        data: {
          labels: ["Pending", "Approved", "Rejected"],
          datasets: [
            {
              data: [
                data.drive_status_breakdown.pending,
                data.drive_status_breakdown.approved,
                data.drive_status_breakdown.rejected,
              ],
              backgroundColor: ["#ffc107", "#198754", "#dc3545"],
            },
          ],
        },
        options: { responsive: true },
      });

      this.charts.trend = new Chart(this.$refs.trendChart, {
        type: "line",
        data: {
          labels: data.placement_trend.map((p) => p.month),
          datasets: [
            {
              label: "Students Placed",
              data: data.placement_trend.map((p) => p.placed),
              yAxisID: "yPlaced",
              borderColor: "#0d6efd",
              backgroundColor: "#0d6efd",
              tension: 0.3,
            },
            {
              label: "Avg Package (CTC)",
              data: data.placement_trend.map((p) => p.avg_ctc),
              yAxisID: "yCtc",
              borderColor: "#198754",
              backgroundColor: "#198754",
              tension: 0.3,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            yPlaced: {
              type: "linear",
              position: "left",
              beginAtZero: true,
              ticks: { precision: 0 },
              title: { display: true, text: "Students Placed" },
            },
            yCtc: {
              type: "linear",
              position: "right",
              beginAtZero: true,
              grid: { drawOnChartArea: false },
              title: { display: true, text: "Avg CTC" },
            },
          },
        },
      });

      this.charts.topCompanies = new Chart(this.$refs.topCompaniesChart, {
        type: "bar",
        data: {
          labels: data.top_companies.map((c) => c.company),
          datasets: [
            {
              label: "Hires",
              data: data.top_companies.map((c) => c.hires),
              backgroundColor: "#0d6efd",
            },
          ],
        },
        options: {
          indexAxis: "y",
          responsive: true,
          plugins: { legend: { display: false } },
          scales: { x: { beginAtZero: true, ticks: { precision: 0 } } },
        },
      });
    },
  },
};
</script>