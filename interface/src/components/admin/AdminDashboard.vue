<template>
  <div>
    <ul class="nav nav-tabs mb-3">
      <li class="nav-item" v-for="tab in tabs" :key="tab.key">
        <a
          class="nav-link"
          :class="{ active: activeTab === tab.key }"
          href="#"
          @click.prevent="activeTab = tab.key"
        >
          {{ tab.label }}
          <span
            v-if="tab.key === 'companies' && pendingCompanyCount"
            class="badge bg-warning text-dark ms-1"
          >{{ pendingCompanyCount }}</span>
          <span
            v-if="tab.key === 'drives' && pendingDriveCount"
            class="badge bg-warning text-dark ms-1"
          >{{ pendingDriveCount }}</span>
        </a>
      </li>
    </ul>

    <PendingCompanies
      v-if="activeTab === 'companies'"
      @updated="refreshCounts"
    />
    <DriveApproval
      v-else-if="activeTab === 'drives'"
      @updated="refreshCounts"
    />
    <UserTable
      v-else-if="activeTab === 'students'"
      role="student"
    />
    <UserTable
      v-else-if="activeTab === 'company-users'"
      role="company"
    />
    <AnalyticsPanel
      v-else-if="activeTab === 'analytics-panel'"
    />
    <ReportsPanel
      v-else-if="activeTab === 'report'"
    />

  </div>
</template>

<script>
import PendingCompanies from './PendingCompanies.vue'
import DriveApproval from './DriveApproval.vue'
import UserTable from './UserTable.vue'
import adminService from '@/services/adminService'

import AnalyticsPanel from './AnalyticsPanel.vue';
import ReportsPanel from './ReportsPanel.vue';


export default {
  name: 'AdminDashboard',
  components: { PendingCompanies, DriveApproval, UserTable , AnalyticsPanel, ReportsPanel},
  data() {
    return {
      activeTab: 'companies',
      pendingCompanyCount: 0,
      pendingDriveCount: 0,
      tabs: [
        { key: 'companies', label: 'Pending Companies' },
        { key: 'drives', label: 'Drives' },
        { key: 'students', label: 'Students' },
        { key: 'company-users', label: 'Companies' },
        {key: 'analytics-panel', label: 'Analytics'},
        {key:'report', label: 'Reports'}
      ]
    }
  },
  created() {
    this.refreshCounts()
  },
  methods: {
    async refreshCounts() {
      try {
        const [companiesRes, drivesRes] = await Promise.all([
          adminService.getPendingCompanies(),
          adminService.getPendingDrives()
        ])
        this.pendingCompanyCount = companiesRes.data.length
        this.pendingDriveCount = drivesRes.data.length
      } catch (err) {
        // badge counts are non-critical; individual tabs surface their own errors
      }
    }
  }
}
</script>
