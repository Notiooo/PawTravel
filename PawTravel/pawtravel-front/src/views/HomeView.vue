<template>
  <Header/>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>
  <Footer/>
</template>
<script>
// @ is an alias to /src
import HelloWorld from '@/components/SamplePage.vue'
import Header from '@/components/HeaderComponent.vue'
import Footer from '@/components/FooterComponent.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld,
    Header,
    Footer
  }
}
</script>
