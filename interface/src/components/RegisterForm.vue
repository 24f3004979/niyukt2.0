<template>

<div class="auth-wrapper">

  <div class="card auth-card">

    <div class="card-body">


      <h3 class="text-center mb-4">
        Create Account
      </h3>


      <div
      v-if="error"
      class="alert alert-danger"
      >
        {{ error }}
      </div>



      <div class="form-group">

        <label>
          Username
        </label>

        <input
        class="form-control"
        placeholder="Enter username"
        v-model="username"
        />

      </div>



      <div class="form-group">

        <label>
          Email
        </label>

        <input
        type="email"
        class="form-control"
        placeholder="Enter email"
        v-model="email"
        />

      </div>



      <div class="form-group">

        <label>
          Password
        </label>

        <input
        type="password"
        class="form-control"
        placeholder="Create password"
        v-model="password"
        />

      </div>



      <label class="mb-2">
        Register as
      </label>


      <div class="role-selector mb-4">


        <label
        class="role-option"
        :class="{active: role==='student'}"
        >

          <input
          type="radio"
          value="student"
          v-model="role"
          >

          Student

        </label>



        <label
        class="role-option"
        :class="{active: role==='company'}"
        >

          <input
          type="radio"
          value="company"
          v-model="role"
          >

          Company

        </label>


      </div>



      <button
      class="btn btn-primary btn-block"
      @click="submit"
      >

        Create Account

      </button>



      <p class="text-center mt-3 mb-0">

        Already have an account?

        <router-link to="/login">
          Login
        </router-link>

      </p>


    </div>

  </div>


</div>


</template>



<script>

import api from "../services/api"


export default {


data(){

return{

username:"",
email:"",
password:"",
role:"student",
error:""

}

},



methods:{


async submit(){


try{


await api.post(
"/api/auth/register",
{
username:this.username,
email:this.email,
password:this.password,
role:this.role
}
)


this.$router.push("/login")


}

catch(error){


this.error =
error.response?.data?.message ||
"Registration terminated"


}


}


}


}

</script>



<style scoped>


.auth-wrapper{

min-height:85vh;

display:flex;

justify-content:center;
align-items:center;

}



.auth-card{

width:380px;

border:none;
border-radius:12px;

box-shadow:
0 5px 20px rgba(0,0,0,0.12);

}



.form-control{

height:42px;

border-radius:8px;

}



.btn{

border-radius:8px;

height:42px;

}



.role-selector{

display:flex;

gap:12px;

}



.role-option{

flex:1;

border:1px solid #ddd;

padding:10px;

border-radius:8px;

text-align:center;

cursor:pointer;

transition:0.2s;

}



.role-option input{

display:none;

}

.role-option.active{

border-color:#007bff;

background:#eaf3ff;

color:#007bff;

font-weight:500;

}



</style>
