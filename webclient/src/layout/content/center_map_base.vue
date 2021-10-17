<template>
  <!--下部的巨幕-->
  <div id="mycontent" class="col-md-12 mycol_disPadding" style="width: 100%">
    <div id="basemap" style="height: 100%; width: 100%">
      <div class="leaflet-control-container">
        <div class="leaflet-top leaflet-left">
          <div class="leaflet-control-zoom leaflet-bar leaflet-control">
            <a
              class="leaflet-control-zoom-in"
              href="http://leafletjs.com/examples/choropleth/example.html#"
              title="Zoom in"
              role="button"
              aria-label="Zoom in"
              >+</a
            >
            <a
              class="leaflet-control-zoom-out"
              href="http://leafletjs.com/examples/choropleth/example.html#"
              title="Zoom out"
              role="button"
              aria-label="Zoom out"
              >−</a
            >
          </div>
        </div>
        <div class="leaflet-top leaflet-right"></div>
        <div class="leaflet-bottom leaflet-left"></div>
        <div class="leaflet-bottom leaflet-right">
          <div class="info legend leaflet-control">
            <i style="background: blue"></i> 2.5-3.5
            <br />
            <i style="background: yellow"></i> 3.5-4.5
            <br />
            <i style="background: orange"></i> 4.5-6
            <br />
            <i style="background: red"></i> 6-max
            <br />
          </div>
          <div class="leaflet-control-attribution leaflet-control">
            <a href="http://nmefc.com/">nmefc</a>版权所有 ©
            <a href="http://nmefc.com/"
              >nmefc&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a
            >
          </div>
        </div>
      </div>
    </div>
    <!-- 由下边的rightBar组件替代 -->
    <!-- <div id="mybar" style="height:400px"></div> -->

    <rightBar
      ref="rightBar"
      :arrValuesForecastextreme="arrValuesForecastextreme"
      :arrKeysForecastextreme="arrKeysForecastextreme"
    ></rightBar>
  </div>
</template>

<script>
// import '../../components/js/map/leaflet'
// import '../../components/js/map/shp.js'
// import '../../components/js/map/leaflet.shpfile'

// import '../../components/js/map/maptiles.js'
// import '../../components/js/map/shp'
// import 'shpjs'
// import 'shp.js'
import 'leaflet'
import shp from 'shpjs'
// import echarts from 'echarts'
// 引入 ECharts 主模块
var echarts = require('echarts/lib/echarts')
// 引入柱状图
require('echarts/lib/chart/bar')
// 引入提示框和标题组件
require('echarts/lib/component/tooltip')
require('echarts/lib/component/title')
// import '_shpjs@3.4.2@shpjs'
// import {
//   StormData,
//   loadStormLayer,
//   createStationIcon,
//   getStormData,
//   loadStationData,
//   getAlarmLevel,
//   addDiv2Marker,
//   loadStormData
// } from '../../comppnents/js/map/storm.js'
// import {loadStormData} from "../../comppnents/js/map/storm";
// import {area} from "../../components/js/map/mytest";
import {
  loadStation,
  getStormData,
  loadStormLayer,
  StormData,
  CreateStationIcon
} from '../../components/js/map/storm'

import { getColorbar } from '../api/api'

import {
  addshp,
  loadAreaMaxDataByDate,
  // addShape,
  dic2arr,
  compareForecast
} from '../../components/js/map/grid'

import { getDateStr } from '../api/moment_api'
// import maptiles from "../../components/js/map/maptiles"
import rightBar from './right_bar.vue'
// TODO:[-] 21-05-06 引入 东海的 grid wms
// import {WMSMidModel,WMSOptionsMidModel} from '../../middle_model/geo.ts'

export default {
  data () {
    return {
      forecastArr: [],
      // info: null,
      my_shp_layer_arr: [],
      // mymap: null,
      my_shp_layer: null,
      info: null,
      geojson: null,
      mymap: this.basemap,
      latlng: null,
    //   gridEast : new WMSMidModel(
    //     'http://localhost:8082/geoserver/nmefc_common/wms?',
    //     new WMSOptionsMidModel('nmefc_common:grid_east')
    // )
    }
  },
  props: {
    basemap: Object,
  },
  components: {
    rightBar
  },
  methods: {
    // 清除所有的底图
    clear: function () {
      this.clearLayer()
      this.clearDivIcon()
    },
    // 清除grid的layer底图
    clearLayer: function () {
      var myself = this
      // 1 清除沿海基础网格底图
      $.each(myself.my_shp_layer_arr, function (index, value) {
        myself.mymap.removeLayer(value)
      })
      myself.my_shp_layer_arr = []
      if (myself.my_shp_layer != null) {
        myself.mymap.removeLayer(myself.my_shp_layer)
      }
    },
    // 清除storm 的 IconDiv以及Marker
    clearDivIcon: function () {
      var myself = this
      // myself.mymap.clearLayers()
      // 注意清除时，需要分别清除marker与IconDiv
      $.each(myself.stormIconDivArr, function (index, val) {
        myself.mymap.removeLayer(val)
      })
      $.each(myself.stormMarkerArr, function (index, val) {
        myself.mymap.removeLayer(val)
      })
      // 2 清除海洋站信息
      myself.stormObjArr = []

      // 3 从mapper中清除后，还需要清空两个arr
      myself.stormIconDivArr = []
      myself.stormMarkerArr = []
    },
    mystyle: function (feature) {
      return {
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7,
        fillColor: getColor(feature.properties.density)
      }
    },
    fillarea: function (area) {
      var date = new Date()
      // var date_str=getDateStr();
      var dictArea = null
      var newLayer = null
      let staticUrl = '../../../static/files/'
      const that=this
      switch (area) {
        // 北海
        case 'n':
          // dictArea = loadAreaMaxData_byDate(date, area)
          dictArea = loadAreaMaxDataByDate(date, area)
          // 缩放并定位到指定海区
          this.mymap.setView([38.3, 123], 7)

          // newLayer = this.addshp(`${staticUrl}north.zip`, dictArea, true)
          
          
          break
        // 东海
        case 'e':
          dictArea = loadAreaMaxDataByDate(date, area)
          this.mymap.setView([28.6, 125.35], 6)

          // newLayer = this.addshp(`${staticUrl}east.zip`, dictArea, true)
          // TODO:[-] 21-05-06 此处使用 加载 geoserver发布的 wms的方式实现
          // var eastGridWmsTitleLayer = L.tileLayer.wms(that.gridEast.url, {
          //     layers: that.gridEast.options.layer,
          //     format: that.gridEast.options.format,
          //     transparent: true,
          //     attribution: "Weather data © 2012 IEM Nexrad"
          // });
          // that.mymap.addLayer(eastGridWmsTitleLayer)
          break
        // 南海
        case 's':
          dictArea = loadAreaMaxDataByDate(date, area)
          this.mymap.setView([20.2, 113.04], 7)

          // newLayer = this.addshp(`${staticUrl}south.zip`, dictArea, true)
          break
        // 全国
        case 'a':
          dictArea = loadAreaMaxDataByDate(date, area)
          // this.addshp(`${staticUrl}north.zip`, dictArea, false)
          // this.addshp(`${staticUrl}east.zip`, dictArea, false)
          // this.addshp(`${staticUrl}south.zip`, dictArea, false)
          break
      }
      return [dictArea, newLayer]
    },
    // 读取本地的netcdf文件，并加载
    fillWMS: function () {
      var myself = this
      // var source=L.WMS.source('../../data/2018011420_08_24.nc',{
      //   'transparent':true
      // })
      var wmsLayer = L.tileLayer.wms(
        'http://localhost:8080/geoserver/gridraster/wms',
        {
          // gridraster:swh
          layers: 'gridraster:wave_area_northwest_hour_00',
          // layers: 'gridraster:storm_nc',
          format: 'image/png',
          transparent: true
        }
      )
      console.log(wmsLayer)
      wmsLayer.addTo(myself.mymap)
    },

    // 初始化加入监听点击事件
    InitOnClick: function () {
      var myself = this
      this.mymap.on('click', function (e) {

        // 获取经纬度对象
        // var cornerStr=e.latlng.toBounds()

        var latLng = L.latLng(e.latlng.lat, e.latlng.lng)
        // var corner1=L.latlng(e.latlng.lat,e.latlng.lng)

        // var cornerStr=corner1.toBBoxString()
        myself.$store.state.latlng = latLng
        console.log(myself.$store.state.latlng)
        // console.log(latLng)
      })
    },

    // infoInit: function () {
    //   // 右上角的消息显示区域初始化
    //   let myself = this
    //   this.info = L.control()
    //   this.info.onAdd = function (map) {
    //     // myself._div = L.DomUtil.create('div', 'info') // create a div with a class "info"
    //     // myself.update()
    //     this._div = L.DomUtil.create('div', 'info') // create a div with a class "info"
    //     this.update()
    //     return this._div
    //   }
    //   // method that we will use to update the control based on feature properties passed
    //   this.info.update = function (props) {
    //     // 此处使用了三元表达式
    //     /*
    //           由于使用了vue，此处的this应该为info
    //         */
    //     // myself.info._div.innerHTML = '<h4>网格概述</h4>' + (props
    //     //         ? '<b>网格编号：</b><br />' + props.Code
    //     //         : '未选中')
    //     this._div.innerHTML =
    //       '<h4>网格概述</h4>' +
    //       (props ? '<b>网格编号：</b><br />' + props.Code : '未选中')
    //   }
    //   this.info.addTo(myself.mymap)
    // },
    zoomView: function (code) {
      // 根据传入的code缩放至指定区域
      switch (code) {
        case 'n':
          // 北海
          this.mymap.setView([38.3, 123], 7)
          break
        case 'e':
          // 东海
          this.mymap.setView([28.6, 125.35], 6)
          break
        case 's':
          // 南海
          this.mymap.setView([20.2, 113.04], 7)
      }
    },

    // 初始化地图
    initMap: function () {
      var myself = this
      if (myself.mymap == null) {
        myself.mymap = L.map('basemap').setView([30.09, 127.75], 5)
        // var mymap = L.map('basemap').setView([51.505, -0.09], 13)
        // mapLink = "../static/mapfiles/";

        L.tileLayer('http://map.geoq.cn/arcgis/rest/services/ChinaOnlineStreetPurplishBlue/MapServer/tile/{z}/{y}/{x}', {
          attribution: '',
          maxZoom: 8,
          minZoom: 2
        }).addTo(myself.mymap)
        var status = 0
        var popup = L.popup()

        var rectangleMeasure = {
          startPoint: null,
          endPoint: null,
          rectangle: null,
          tips: null,
          layer: L.layerGroup(),
          color: '#0D82D7',
          addRectangle: function () {
            rectangleMeasure.destory()
            var bounds = []
            bounds.push(rectangleMeasure.startPoint)
            bounds.push(rectangleMeasure.endPoint)
            rectangleMeasure.rectangle = L.rectangle(bounds, {
              color: rectangleMeasure.color,
              weight: 1
            })
            rectangleMeasure.rectangle.addTo(rectangleMeasure.layer)

            var northWestPoint = rectangleMeasure.rectangle
              .getBounds()
              .getNorthWest(),
              southEastPoint = rectangleMeasure.rectangle
                .getBounds()
                .getSouthEast()
            rectangleMeasure.layer.addTo(map)
          },
          mousedown: function (e) {
            rectangleMeasure.rectangle = null
            rectangleMeasure.tips = null
            map.dragging.disable()
            rectangleMeasure.startPoint = e.latlng
            map.on('mousemove', rectangleMeasure.mousemove)
          },
          mousemove: function (e) {
            rectangleMeasure.endPoint = e.latlng
            rectangleMeasure.addRectangle()
            map
              .off('mousedown ', rectangleMeasure.mousedown)
              .on('mouseup', rectangleMeasure.mouseup)
          },
          mouseup: function (e) {
            map.dragging.enable()
            map
              .off('mousemove', rectangleMeasure.mousemove)
              .off('mouseup', rectangleMeasure.mouseup)
              .off('mousedown', rectangleMeasure.mousedown)
          },
          destory: function () {
            if (rectangleMeasure.rectangle) {
              rectangleMeasure.layer.removeLayer(rectangleMeasure.rectangle)
            }
            if (rectangleMeasure.tips) {
              rectangleMeasure.layer.removeLayer(rectangleMeasure.tips)
            }
          }
        }

        this.$emit('update:basemap', myself.mymap)
      }

    }
  },

  // 监听路由的变化写在watch中，当路由发生变化时，判断传入的种类是风暴潮还是网格
  watch: {
    $route (to, from) {
      // 当每次路由发生变化时，route会发生变化
      console.log(`to:${to},from:${from}`)
      console.log(`${to.params}`)
      // 执行加载 风暴潮/站点 的相关操作
      // 在加载之前，需要先清除当前的图层
      // 此处需要判断要执行的加载内容
      let category = to.params.category
      switch (category) {
        case 'storm':
          console.log('storm')
          // this.clearLayer()
          // this.clearDivIcon()
          this.clear()
          // this.fillWMS()

          this.fillStorm(to.params.code)
          break
        case 'grid':
          console.log('grid')
          // 统一写在clear方法中
          // this.clearLayer()
          // this.clearDivIcon()
          this.clear()
          // this.fillGrid(to.params.code)
          break
        case 'forecast':
          // 注意此处还需要获取传过来的一些其他参数（1、时间；2、种类、3、是否只显示当前时间的）
          console.log('叠加显示forecast')
          // 清除全部已叠加的图层
          this.clear()
          // 填充数值预报
          this.fillWMS()
        case 'all':
          // 不用清除图层，加载全部图层
          console.log('all')
          // 待补充相应的操作
          break
      }
    },
    mymap (newVal, oldVal) {
      this.$emit('update:basemap', newVal)
    }
  },

  created: function () {
    console.log('view created')
  },

  mounted: function () {
    let code = this.$route.params.code
    // 初始化地图引擎
    this.initMap()
    // 缩放至指定海区
    this.zoomView(code)
    // 对info初始化
    // 将其写在父组件中
    // this.infoInit()

    this.InitOnClick()
  }
}
</script>

<style>
#mycontent {
  position: absolute;
  top: 188px;
  bottom: 0px;
  width: 100%;
  overflow: hidden;
}
</style>
