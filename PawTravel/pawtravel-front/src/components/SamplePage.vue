<template>
  <div class="pt-background-darkblue">
    <h1 class="title">SAMPLE PAGE</h1>

    <hr>

    <div class="columns">
      <div class="column is-half">
        <h2 class="subtitle">Users</h2>

        <div class="api-fetcher">
          <div class="card" v-for="user in users" :key="user.id">
            <div class="card-content">

              <div class="content">
            Username : {{ user.username }} <br>
            Email : {{ user.email }} <br>
            Administrator account : {{ user.is_staff }} <br> <br>
              </div>

            </div>
          </div>
        </div>

        <hr>

        <div class="pt-background-lightblue">
          <button class="pk-button-primary" @click="go_to_TravelGuides">
            Go to Travel Guides
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios'

export default {
  name: 'SamplePage',
  title () {
    return 'SamplePage'
  },
  data () {
    return {
      users: []
    }
  },
  mounted () {
    this.get_Users()
  },
  methods: {
    get_Users() {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/users/'
      }).then(response => {
        this.users = response.data
      })
    },
    go_to_TravelGuides() {
      this.$router.push('/travel-guides')
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
