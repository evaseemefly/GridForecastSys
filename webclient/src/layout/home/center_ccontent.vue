<template>
    <!--下部的巨幕-->
    <div id="mycontent" class="col-md-12 mycol_disPadding" style="width: 100%;">
        <div id="basemap" style="height: 100%; width: 100%;">
            <div class="leaflet-control-container">
                <div class="leaflet-top leaflet-left">
                    <div class="leaflet-control-zoom leaflet-bar leaflet-control">
                        <a class="leaflet-control-zoom-in" href="http://leafletjs.com/examples/choropleth/example.html#" title="Zoom in" role="button"
                            aria-label="Zoom in">+</a>
                        <a class="leaflet-control-zoom-out" href="http://leafletjs.com/examples/choropleth/example.html#" title="Zoom out" role="button"
                            aria-label="Zoom out">−</a>
                    </div>
                </div>
                <div class="leaflet-top leaflet-right">
                    <!--<div class="info leaflet-control">
                            <h4>网格概述</h4>未选择网格
                        </div>-->
                </div>
                <div class="leaflet-bottom leaflet-left"></div>
                <div class="leaflet-bottom leaflet-right">
                    <div class="info legend leaflet-control">
                        <i style="background:blue"></i> 2.5-3.5
                        <br>
                        <i style="background:yellow"></i> 3.5-4.5
                        <br>
                        <i style="background:orange"></i> 4.5-6
                        <br>
                        <i style="background:red"></i> 6-max
                        <br>
                    </div>
                    <div class="leaflet-control-attribution leaflet-control">
                        <!--<a href="http://leafletjs.com/" title="A JS library for interactive maps">Leaflet</a> | Map data ©
                            <a href="http://openstreetmap.org/">OpenStreetMap</a> contributors,
                            <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery ©-->
                        <a href="http://nmefc.com/">nmefc</a>版权所有 ©
                        <a href="http://nmefc.com/">nmefc&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a>

                    </div>
                </div>
            </div>
            <div id="mybar" style="height:400px"></div>
        </div>
    </div>
</template>

<script>
    export default {

    }
</script>

<style>
</style>