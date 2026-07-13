<template>

  <div id="app">

    <nav 
      class="navbar navbar-expand-lg navbar-dark bg-dark"
    >

      <div class="container">

        <div
          class="navbar-brand"
          to="/"
        >
          Niyukt-v2.0

        </div>


      </div>


    </nav>

    <!-- All views render here -->
    <router-view />

  </div>


</template>



<script>

export default {


computed:{


isLoggedIn(){

return !!localStorage.getItem(
"token"
)

}


},



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



<style>

#app {

min-height:100vh;

}

</style>
