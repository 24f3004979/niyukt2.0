<template>
  <div>
    <ul class="nav nav-tabs mb-3">
      <li class="nav-item">
        <a
          class="nav-link"
          :class="{ active: activeTab === 'drives' }"
          href="#"
          @click.prevent="activeTab = 'drives'"
        >
          Available Drives
        </a>
      </li>
      <li class="nav-item">
        <a
          class="nav-link"
          :class="{ active: activeTab === 'applications' }"
          href="#"
          @click.prevent="activeTab = 'applications'"
        >
          My Applications
        </a>
      </li>
    </ul>

    <AvailableDrives v-if="activeTab === 'drives'" @applied="activeTab = 'applications'" />
    <MyApplications v-else />
  </div>
</template>

<script>
import AvailableDrives from './AvailableDrives.vue'
import MyApplications from './MyApplications.vue'

export default {
  name: 'StudentDashboard',
  components: { AvailableDrives, MyApplications },
  data() {
    return {
      activeTab: 'drives'
    }
  }
}
</script>