<!-- src/App.vue -->
<template>
  <div id="app" class="auth-container">
    <div class="toggle-buttons">
      <button :class="{ active: currentView === 'login' }" @click="currentView = 'login'">Login</button>
      <button :class="{ active: currentView === 'register' }" @click="currentView = 'register'">Register</button>
    </div>

    <!-- Switch components seamlessly based on active tab -->
    <LoginView v-if="currentView === 'login'" @registration-success="currentView = 'login'" />
    <RegisterView v-else />
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
      currentView: 'login'
    };
  }
};
</script>

<style>
.auth-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-family: Arial, sans-serif;
}
.toggle-buttons {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}
.toggle-buttons button {
  padding: 10px 20px;
  cursor: pointer;
  border: none;
  background: #eee;
  flex-grow: 1;
}
.toggle-buttons button.active {
  background: #42b983;
  color: white;
}
form div {
  margin-bottom: 15px;
}
label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}
input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
button[type="submit"] {
  width: 100%;
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}
.error-msg { color: red; margin-top: 10px; }
.success-msg { color: green; margin-top: 10px; }
</style>

