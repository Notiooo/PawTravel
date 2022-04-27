<template>
  <Header/>
  <div class="start">
    <h3>Travel Guides</h3>
  </div>
  <Footer/>
</template>

<script>

import Header from '@/components/HeaderComponent.vue'
import Footer from '@/components/FooterComponent.vue'

export default {
  name: "TravelGuides",
  components: {
    Header,
    Footer
  }
}
</script>

<style scoped>

</style>