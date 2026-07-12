<template>

<div class="container mt-5">

<h3>
Create Account
</h3>


<input
class="form-control mb-2"
placeholder="Username"
v-model="username"
/>


<input
class="form-control mb-2"
placeholder="Email"
v-model="email"
/>


<input
class="form-control mb-2"
type="password"
placeholder="Password"
v-model="password"
/>


<button
class="btn btn-primary"
@click="register"
>
Register
</button>


</div>

</template>



<script>

import api from "../services/api"


export default{


data(){

return{

username:"",
email:"",
password:""

}

},


methods:{


async register(){


await api.post(
"/auth/register",
{

username:this.username,
email:this.email,
password:this.password

}
)


alert(
"Registered"
)


this.$router.push("/login")


}


}


}


</script>
