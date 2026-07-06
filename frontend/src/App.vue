<template>

  <div class="auth-wrapper">
    <div class="card auth-card shadow-sm">
      <div class="card-body p-4">
        <ul class="nav nav-pills nav-fill mb-4">
          <li class="nav-item">
            <button
              class="nav-link"
              :class="{ active: mode === 'login' }"
              @click="mode = 'login'"
            >
              Login
            </button>
          </li>
          <li class="nav-item">
            <button
              class="nav-link"
              :class="{ active: mode === 'register' }"
              @click="mode = 'register'"
            >
              Register
            </button>
          </li>
        </ul>

        <LoginView v-if="mode === 'login'" />
        <RegisterView v-else />
      </div>
    </div>
  </div>
</template>

<script>
import LoginView from './components/LoginView.vue';
import RegisterView from './components/RegisterView.vue';

export default {
  name: 'App',
  components: {
    LoginView,
    RegisterView
  },
  data() {
    return {
      mode: 'login'
    };
  }
};
</script>

<style scoped>
.auth-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0d1117;
  padding: 1rem;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  border: none;
  border-radius: 18px;
}

.nav-pills{
  background-color : black;
  border-radius : 10px;
}

.nav-pills .nav-link {
  border-radius: 10px;
  font-weight: 600;
  color: white;
}

.nav-pills .nav-link.active {
  background-color: #0d6efd;
}
</style>
