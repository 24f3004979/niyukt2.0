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
      <li class="nav-item">
        <a
          class="nav-link"
          :class="{ active: activeTab === 'profile' }"
          href="#"
          @click.prevent="activeTab = 'profile'"
        >
          My Profile
        </a>
      </li>
    </ul>

    <AvailableDrives v-if="activeTab === 'drives'" @applied="activeTab = 'applications'" />
    <MyApplications v-else-if="activeTab === 'applications'" />
    <ResumeUpload v-else />
  </div>
</template>

<script>
import AvailableDrives from './AvailableDrives.vue'
import MyApplications from './MyApplications.vue'
import ResumeUpload from './ResumeUpload.vue'

export default {
  name: 'StudentDashboard',
  components: { AvailableDrives, MyApplications, ResumeUpload },
  data() {
    return {
      activeTab: 'drives'
    }
  }
}
</script>