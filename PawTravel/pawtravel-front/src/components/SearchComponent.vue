<template>
  <form>
<div class="uk-child-width-expand@s uk-text-center uk-grid-small uk-margin-large-top" uk-grid>
  <div>
    <div class="uk-inline">
      <span class="uk-form-icon" uk-icon="icon: location"></span>
      <input class="uk-input" type="text" placeholder="DESTINATION">
    </div>
  </div>
  <div>
    <div class="uk-inline">
      <span class="uk-form-icon" uk-icon="icon: info"></span>
      <input class="uk-input" type="text" placeholder="CATEGORY">
    </div>
  </div>
  <div>
    <div class="uk-inline">
      <span class="uk-form-icon" uk-icon="icon: credit-card"></span>
      <input class="uk-input" type="text" placeholder="BUDGET">
    </div>
  </div>
    <div>
    <div class="uk-inline">
      <span class="uk-form-icon" uk-icon="icon: calendar"></span>
      <input class="uk-input" type="text" placeholder="DATE">
    </div>
  </div>
  <div>
    <div class="uk-inline">
      <span class="uk-form-icon" uk-icon="icon: Cat_Footprint_icon_2"></span>
      <input class="uk-input pk-button-primary" type="submit" value="SEARCH" placeholder="SEARCH">
    </div>
    <!--
    <button class="searchbt uk-button uk-button-default pk-button-primary">
      <img class="search" src="../assets/static/img/Cat_Footprint_icon_2.png" alt="Search"> SEARCH
    </button>
    -->
  </div>


</div>
     </form>
</template>

<script>
export default {
  name: "SearchComponent"
}
</script>

<style scoped>
.search{
  padding-right: 10px;
}
.searchbt{
  padding-left: 10px;
}

@import 'uikit/dist/css/uikit.min.css';
@import './../assets/static/css/pawtravel.css';

</style>