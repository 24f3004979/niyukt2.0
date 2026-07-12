<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title text-capitalize">{{ role }}s</h5>

      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border spinner-border-sm text-primary" role="status"></div>
      </div>

      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <p v-else-if="users.length === 0" class="text-muted mb-0">No {{ role }}s found.</p>

      <table v-else class="table table-hover align-middle">
        <thead>
          <tr>
            <th>Username</th>
            <th>Email</th>
            <th>Status</th>
            <th class="text-end">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in users" :key="u.id">
            <td>{{ u.username }}</td>
            <td>{{ u.email }}</td>
            <td>
              <span class="badge" :class="statusBadgeClass(u.account_status)">
                {{ u.account_status }}
              </span>
            </td>
            <td class="text-end">
              <button
                v-if="u.account_status !== 'blocked'"
                class="btn btn-sm btn-outline-danger"
                :disabled="actionInProgress === u.id"
                @click="block(u.id)"
              >
                Block
              </button>
              <button
                v-else
                class="btn btn-sm btn-outline-success"
                :disabled="actionInProgress === u.id"
                @click="unblock(u.id)"
              >
                Unblock
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import adminService from '@/services/adminService'

export default {
  name: 'UserTable',
  props: {
    role: {
      type: String,
      required: true,
      validator: value => ['student', 'company'].includes(value)
    }
  },
  data() {
    return {
      users: [],
      loading: true,
      error: null,
      actionInProgress: null
    }
  },
  watch: {
    role() {
      this.fetchUsers()
    }
  },
  created() {
    this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      this.loading = true
      this.error = null
      try {
        const response = this.role === 'student'
          ? await adminService.getAllStudents()
          : await adminService.getAllCompanies()
        this.users = response.data
      } catch (err) {
        this.error = `Failed to load ${this.role}s.`
      } finally {
        this.loading = false
      }
    },
    async block(id) {
      this.actionInProgress = id
      try {
        await adminService.blockUser(id)
        const user = this.users.find(u => u.id === id)
        if (user) user.account_status = 'blocked'
      } catch (err) {
        this.error = err.response?.data?.error?.message || 'Failed to block user.'
      } finally {
        this.actionInProgress = null
      }
    },
    async unblock(id) {
      this.actionInProgress = id
      try {
        await adminService.unblockUser(id)
        const user = this.users.find(u => u.id === id)
        if (user) user.account_status = 'active'
      } catch (err) {
        this.error = err.response?.data?.error?.message || 'Failed to unblock user.'
      } finally {
        this.actionInProgress = null
      }
    },
    statusBadgeClass(status) {
      return {
        active: 'bg-success',
        pending: 'bg-warning text-dark',
        blocked: 'bg-danger',
        rejected: 'bg-secondary'
      }[status] || 'bg-secondary'
    }
  }
}
</script>
