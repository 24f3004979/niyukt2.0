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
          My Drives
        </a>
      </li>
      <li class="nav-item">
        <a
          class="nav-link"
          :class="{ active: activeTab === 'create' }"
          href="#"
          @click.prevent="activeTab = 'create'"
        >
          Create Drive
        </a>
      </li>
    </ul>

    <MyDrives v-if="activeTab === 'drives'" ref="myDrives" />
    <CreateDriveForm v-else @created="onDriveCreated" />
  </div>
</template>

<script>
import MyDrives from './MyDrives.vue'
import CreateDriveForm from './CreateDriveForm.vue'

export default {
  name: 'CompanyDashboard',
  components: { MyDrives, CreateDriveForm },
  data() {
    return {
      activeTab: 'drives'
    }
  },
  methods: {
    onDriveCreated() {
      this.activeTab = 'drives'
    }
  }
}
</script>