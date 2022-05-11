<template>

   <div class="uk-grid-collapse uk-child-width-expand@s uk-margin-large-top" uk-grid>
    <div class="uk-width-3-5">
        <div class="pt-background-lightblue pt.textcolor-white m-font uk-padding">The best deal of the best

        </div>
    </div>
    <div class="uk-width-2-5">
      <div class="pt-background-white" uk-slideshow="animation: push">
        <div class="uk-position-relative uk-visible-toggle uk-light" tabindex="-1">
          <ul class="uk-slideshow-items">
            <li>
              <p class="uk-padding">A</p>
            </li>
            <li>
              <p>A</p>
            </li>
            <li>
              <p>A</p>
            </li>
          </ul>
          <a class="uk-position-center-left uk-position-small uk-hidden-hover" href="#" uk-slidenav-previous uk-slideshow-item="previous"></a>
          <a class="uk-position-center-right uk-position-small uk-hidden-hover" href="#" uk-slidenav-next uk-slideshow-item="next"></a>
        </div>
        <ul class="uk-light uk-slideshow-nav uk-dotnav uk-flex-center uk-margin uk-padding"></ul>
      </div>
    </div>
  </div>

</template>

<script>
export default {
  name: "TopOffersComponent"
}
</script>

<style scoped>
</style>