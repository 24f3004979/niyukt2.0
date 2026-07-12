<template>


<div class="container mt-5">


<h3>
Login
</h3>


<input
class="form-control mb-2"
placeholder="Username"
v-model="username"
/>


<input
class="form-control mb-2"
type="password"
placeholder="Password"
v-model="password"
/>


<button
class="btn btn-success"
@click="login"
>

Login

</button>


</div>


</template>


<script>


import api from "../services/api"



export default{


data(){

return{

username:"",
password:""

}

},



methods:{


async login(){


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


}



}


</script>
