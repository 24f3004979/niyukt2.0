<template>
  <div class="auth-form">
    <h3>Create Account</h3>
    <form @submit.prevent="submitRegister">
      <div>
        <label>Username</label> <input type="text" v-model="username" required /> </div>
      <div>
        <label>Password</label>
        <input type="password" v-model="password" required />
      </div>
       <div>
        <label>Confirm Password</label>
        <input type="password" v-model="confirm-password" required />
      </div>

      <div>
        <label>
          <input type="radio" :value="company" v-model="selected_role" />
          company
        </label>

      </div>
      <button type="submit">Register Now</button>
    </form>
    <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>
    <p v-if="successMessage" class="success-msg">{{ successMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';
import ref from 'vue';

const selected_role = ref('student');
const password = ref("password");
const confirm_password = ref("confirm-password");

export default {
  data() {
    return {
      username: '',
      password: '',
      role: selected_role,
      errorMessage: '',
      successMessage: ''
    };
  },
  methods: {
    async submitRegister() {
      this.errorMessage = '';
      this.successMessage = '';
      
      try {
        if (confirm_password != password){
          throw Error('Check your password confirmation');
        }
        await axios.post('api/register', {
          username: this.username,
          password: this.password,
          role: 'student' // Sets default role according to service specifications
        }, {
          headers: { 'Content-Type': 'application/json' }
        });
        
        this.successMessage = 'Registration complete! You can switch tabs to log in.';
        this.username = '';
        this.password = '';
      } catch (err) {
        this.errorMessage = err.response?.data?.error || 'Registration service unreachable.';
        console.log(`Registration failed with error : ${err}`)
      }
    }
  }
};
</script>
