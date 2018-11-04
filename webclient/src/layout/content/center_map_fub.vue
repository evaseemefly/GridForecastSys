<template>
  <div>
    <baseMap ref="baseMap" :basemap.sync='mymap'></baseMap>
    <dateModule @changeLayerIndex="changeLayerIndex"></dateModule>
    <modalFrame ref="modal" :columns='modalColumns' :values='modalValues'></modalFrame>
  </div>
</template>

<script>
import 'leaflet'
import shp from 'shpjs'

import { mapGetters } from 'vuex'
// import echarts from 'echarts'
// 引入 ECharts 主模块
var echarts = require('echarts/lib/echarts')
// 引入柱状图
require('echarts/lib/chart/bar')
// 引入提示框和标题组件
require('echarts/lib/component/tooltip')
require('echarts/lib/component/title')
import { getColorbar, loadForecastWavebyNc } from '../api/api'

import { getDateStr } from '../api/moment_api'
import rightBar from './right_bar.vue'
// map的base子组件
import baseMap from './center_map_base.vue'
// modal子组件
import modalFrame from '../module/modal.vue'
import dateModule from '../module/date_select_module.vue'
export default {
  data () {
    return {
      // 加载预报产品需要的data
      mymap: null,
      wms_layer: null,
      // '000','006'
      wms_layer_index: String,
      // 预报产品的种类
      wms_kinds: null,
      // 预报产品的日期
      wms_date: null,
      // 预报产品的间隔
      wms_interval: null,
      // 需要加载的经纬度
      wms_latlng: null,
      // wms_lng,
      latlng: null,
      modalTitle: '',
      modalColumns: [],
      modalValues: []
    }
  },
  components: {
    rightBar,
    baseMap,
    modalFrame,
    dateModule
  },
  computed: {
    ...mapGetters(['getlatlng']),

    // 当vuex中的latlng修改后，也修改此处的latlng
    getlatlngTest: function () {
      var myself = this
      // 第一次加载时，store.state.latlng中没有lat属性
      // 此处需要加一个判断
      if (myself.$store.state.latlng.hasOwnProperty('lat')) {
        console.log('computed' + myself.$store.state.latlng)
        this.latlng = this.$store.state.latlng
        // 经纬度改变后加载子组件2（modal）
        this.showModal()
      }
      // return this.$store.state.latlng
    },
    // wms_layer:function(){

    // }
  },
  methods: {
    fillarea: function (area) {
      var date = new Date()
      // var date_str=getDateStr();
      var dictArea = null
      var newLayer = null
      let staticUrl = '../../../static/files/'
      switch (area) {
        // 北海
        case 'n':
          // dictArea = loadAreaMaxData_byDate(date, area)
          dictArea = loadAreaMaxDataByDate(date, area)
          // 缩放并定位到指定海区
          this.mymap.setView([38.3, 123], 7)

          newLayer = this.addshp(`${staticUrl}north.zip`, dictArea, true)
          break
        // 东海
        case 'e':
          dictArea = loadAreaMaxDataByDate(date, area)
          this.mymap.setView([28.6, 125.35], 6)

          newLayer = this.addshp(`${staticUrl}east.zip`, dictArea, true)
          break
        // 南海
        case 's':
          dictArea = loadAreaMaxDataByDate(date, area)
          this.mymap.setView([20.2, 113.04], 7)

          newLayer = this.addshp(`${staticUrl}south.zip`, dictArea, true)
          break
        // 全国
        case 'a':
          dictArea = loadAreaMaxDataByDate(date, area)
          this.addshp(`${staticUrl}north.zip`, dictArea, false)
          this.addshp(`${staticUrl}east.zip`, dictArea, false)
          this.addshp(`${staticUrl}south.zip`, dictArea, false)
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
          // layers: 'gridraster:wave_area_northwest_hour_00',
          layers: myself.wms_layer,
          // layers: 'gridraster:storm_nc',
          format: 'image/png',
          transparent: true
        }
      )
      console.log(wmsLayer)
      wmsLayer.addTo(myself.mymap)
    },
    showModal: function () {
      var myself = this
      loadForecastWavebyNc('2018082112', myself.latlng.lat, myself.latlng.lng).then(res => {
        console.log(res.data)
        var columns = []
        var values = []
        $.each(res.data, function (index, val) {
          columns.push(val.date)
          values.push(val.value)
        })
        myself.modalColumns = columns
        myself.modalValues = values
        // 调用modal子组件的showModal方法，打开modal框
        this.$refs.modal.showModal()
      })
    },

    // 接受由子组件传递过来的的layer的index（eg：000，006）
    changeLayerIndex: function (val) {
      this.wms_layer_index = val
    }
  },

  // 监听路由的变化写在watch中，当路由发生变化时，判断传入的种类是风暴潮还是网格
  watch: {
    $route (to, from) {
      // 当每次路由发生变化时，route会发生变化
      console.log(`to:${to},from:${from}`)
      console.log(`${to.params}`)
    },
    // latlng(newVal, oldVal) {
    //   console.log(oldVal, newVal)
    // },
    // '$store.state.latlng': function(oldval, oldval) {
    //   console.log(oldval, oldval)
    // },
    getlatlng: function (newVal, oldVal) {
      console.log(oldVal, newVal)
    },
    getlatlngTest: function (val) { },
    wms_layer_index: function (val) {
      this.wms_layer = 'gridraster:wave_area_northwest_hour_' + val
    },
    wms_layer: function (val) {
      this.fillWMS()
    }
  },

  created: function () {
    console.log('view created')
  },

  mounted: function () {
    let code = this.$route.params.code
    // 以下部分在子组件中
    // 初始化地图引擎
    // this.initMap()
    // // 缩放至指定海区
    // this.zoomView(code)
    // // 对info初始化
    // this.infoInit()

    // this.InitOnClick()
    // 清除全部已叠加的图层
    // 注意此处需要调用子组件中的方法
    // this.clear()
    this.$refs.baseMap.clear()
    // 填充数值预报
    this.fillWMS()
    console.log('view mounted')
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
