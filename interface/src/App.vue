<template>

  <div id="app">

    <nav 
      class="navbar navbar-expand-lg navbar-dark bg-dark"
    >

      <div class="container">

        <router-link 
          class="navbar-brand"
          to="/"
        >
          Niyukt-v2.0
        </router-link>


        <div>

          <router-link
            v-if="!isLoggedIn"
            class="btn btn-outline-light mr-2"
            to="/login"
          >
            Login
          </router-link>


          <router-link
            v-if="!isLoggedIn"
            class="btn btn-outline-light"
            to="/register"
          >
            Register
          </router-link>


          <button
            v-if="isLoggedIn"
            class="btn btn-danger"
            @click="logout"
          >
            Logout
          </button>


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
background-color : black;

}

</style>
