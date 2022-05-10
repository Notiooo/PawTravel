<template>
  <header>
    <div class="uk-grid">
      <!--<div class="uk-width-1-6"/> -->
      <div class="uk-width-5-6 uk-align-center">
        <nav class="uk-navbar-container uk-margin uk-navbar">
          <div class="uk-navbar-left">
            <div class="uk-navbar-item">
              <a class="uk-navbar-item uk-logo">
                <img src="../assets/static/img/PawTravel-icon.png" alt="PawTravel">
                PawTravel
              </a>
            </div>
            </div>
          <div class="uk-navbar-center">
            <div class="uk-navbar-item">
              <form action="javascript:void(0)">
                <input class="uk-input uk-form-width-large m-font pk-button-primary" type="text" placeholder="Lorem Ipsum">
              </form>
            </div>
          </div>
              <div class="uk-navbar-right">
            <div class="uk-navbar-item">
              <button class="uk-button uk-button-default pk-button-primary">
                <span uk-icon="icon: check"></span>Add</button>
            </div>
            <div class="uk-navbar-item">
              <a class="uk-icon-link">
                <img src="../assets/static/img/Notification_icon.png" alt="Notification">
              </a>
            </div>
            <div class="uk-navbar-item">
              <a class="uk-icon-link">
                <img src="../assets/static/img/Urgent_Message_icon.png" alt="Urgent Message">
              </a>
            </div>
            <div class="uk-navbar-item">
              <a class="uk-icon-link">
                <img src="../assets/static/img/User_icon.png" alt="User">
              </a>
              </div>
          </div>
        </nav>
      </div>
<!--      <div class="uk-width-1-6"/>-->
    </div>
  </header>
</template>
<script>

import 'uikit'
import 'uikit/dist/css/uikit.min.css'
import 'uikit/dist/js/uikit.min.js'
import 'uikit/dist/js/uikit-icons.min.js'

export default {
  data () {
    return {
      title: 'PawTravel Header'
    }
  }
}
</script>

<style scoped>
@import 'uikit/dist/css/uikit.min.css';
@import './../assets/static/css/pawtravel.css';
</style>