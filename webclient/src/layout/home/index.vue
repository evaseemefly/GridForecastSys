<template>
    <div id="app">
        <topmain></topmain>
        <router-view></router-view>
        <!-- <centerarea></centerarea> -->
    </div>
</template>

<script>
    import topmain from "../head/top_main.vue";
    import centerarea from "../head/top_center_area.vue";
    export default {
        components:{
            topmain
        }
    }
</script>

<style>
    /*对于使用了bootstrap的navbar并固定在顶部时下面的div填充满整个屏幕的解决办法*/

    html,
    body {
        height: 100%;
        margin: 0px;
        padding: 0px;
        background-color: #BBBBBB;
    }

    #main {
        position: absolute;
        top: 132px;
        bottom: 0px;
        width: 100%;
    }

   

    #nav {
        height: 100%;
        background: #00B83F;
    }

    #content {
        background-color: #F5E79E;
        height: 100%;
    }

    #ul_nav {
        position: absolute;
        height: 100%;
    }

    .row-margin-top {
        margin-top: 10px;
    }

    .form-horizontal .form-group {
        margin-left: 0px;
    }

    .col-padding-2 {
        padding-left: 2px;
        padding-right: 2px;
    }

    .col-padding-left-2 {
        padding-left: 2px;
    }

    .mycol_disPadding {
        padding-left: 0px;
        padding-right: 0px;
    }

    .info {
        padding: 6px 8px;
        font: 14px/16px Arial, Helvetica, sans-serif;
        background: white;
        background: rgba(255, 255, 255, 0.8);
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
        border-radius: 5px;
    }

    .info h4 {
        margin: 0 0 5px;
        color: #777;
    }

    .legend {
        text-align: left;
        line-height: 18px;
        color: #555;
    }

    .legend i {
        width: 18px;
        height: 18px;
        float: left;
        margin-right: 8px;
        opacity: 0.7;
    }

    #basemap {
        position: relative;
    }

    #mybar {
        position: absolute;
        z-index: 999;
        /*top:-500px;*/
        top: 100px;
        right: 10px;
        width: 400px;
    }
</style>
</style>