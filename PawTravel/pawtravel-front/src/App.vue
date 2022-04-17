<template>
  <SamplePage msg="Welcome to PawTravel"/>
</template>

<script>
import SamplePage from './components/SamplePage.vue'

export default {
  name: 'App',
  components: {
    SamplePage
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
