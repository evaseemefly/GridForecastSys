<template>
    <div id="topmain">
        <sitemap></sitemap>
        <category></category>
        <centerarea></centerarea>        
    </div>
</template>

<script>
    import centerarea from './top_center_area.vue'
import sitemap from './top_sitemap.vue'
import category from './top_center_category.vue'
export default {
      components: {
        centerarea,
        sitemap,
        category
      }
    }
</script>

<style>
</style>
