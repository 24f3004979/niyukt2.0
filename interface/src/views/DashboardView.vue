<template>

<div class="container mt-5">


<h1>
Placement Portal Dashboard
</h1>


<p>
Welcome User
</p>


<button
class="btn btn-danger"
@click="logout"
>
Logout
</button>


</div>

</template>



<script>


export default{


methods:{


logout(){

localStorage.removeItem(
"token"
)

this.$router.push(
"/login"
)

}


}


}


</script>
