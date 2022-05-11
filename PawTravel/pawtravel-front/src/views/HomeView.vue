<template>
  <div class="uk-grid">
    <div class="uk-width-5-6 uk-align-center">
      <Header/>
      <Search/>
      <TopOffers/>
    </div>
  </div>
</template>

<script>
import Header from '@/components/HeaderComponent.vue'
import Search from '@/components/SearchComponent.vue'
import TopOffers from '@/components/TopOffersComponent.vue'
export default {
  name: 'HomeView',
  components: {
    Header,
    Search,
    TopOffers
  }
}
</script>
