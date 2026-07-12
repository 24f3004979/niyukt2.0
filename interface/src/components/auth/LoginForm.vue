<template>

<div class="auth-wrapper">


<div class="card auth-card">


<div class="card-body">


<h3 class="text-center mb-4">
Welcome Back
</h3>



<div
v-if="error"
class="alert alert-danger"
>
{{error}}
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
Password
</label>


<input

type="password"

class="form-control"

placeholder="Enter password"

v-model="password"

/>


</div>




<button

class="btn btn-success btn-block"

@click="login"

>

Login

</button>




<p class="text-center mt-3">

Don't have an account?

<router-link to="/register">
Register
</router-link>

</p>



</div>


</div>


</div>


</template>



<script>

import api from "../../services/api"


export default{


data(){

return{

username:"",
password:"",
error:""

}

},


methods:{


async login(){


try{


const response =
await api.post(

"/auth/login",

{

username:this.username,

password:this.password

}

)



localStorage.setItem(

"token",

response.data.token

)



this.$router.push(
"/dashboard"
)


}

catch(error){


this.error =
error.response?.data?.message ||
"Invalid credentials"


}


}


}


}


</script>



<style scoped>


.auth-wrapper{

min-height:80vh;

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

height:42px;

border-radius:8px;

}


</style>
