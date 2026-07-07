<template>
  <div id="app">
    <!-- This tag checks the URL. If it's /auth, it injects AuthView. If it's /dashboard, it injects DashboardView -->
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

