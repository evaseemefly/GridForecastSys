<template>
  <div>
    <baseMap ref="baseMap" :basemap.sync='mymap'></baseMap>
    <!-- <dateModule @changeLayerIndex="changeLayerIndex"></dateModule> -->
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
import { getColorbar, loadFubStormData } from '../api/api'

import { getDateStr } from '../api/moment_api'
import rightBar from './right_bar.vue'
// map的base子组件
import baseMap from './center_map_base.vue'
// modal子组件
import modalFrame from '../module/modal.vue'

import {
  CreateFubIcon,
  loadFub
} from '../../components/js/map/fub.js'
// import dateModule from '../module/date_select_module.vue'
export default {
  data () {
    return {
      // 加载预报产品需要的data
      mymap: null,
      // forecastDict:[],
      fubArr: [],
      fubDict: {},
      fubObjArr: [],
      // 浮标的marker数组
      fubMarkerArr: [],
      // 浮标的IconDiv数组
      fubIconDivArr: [],

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
    modalFrame
    // dateModule
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
    }
    // wms_layer:function(){
    // }
  },
  methods: {
    addDiv2Marker: function (fubObj) {
      let myself = this
      // 1 添加marker至map
      var tempMarker = L.marker([fubObj.lat, fubObj.lon])
      tempMarker.addTo(myself.mymap)
      myself.fubMarkerArr.push(tempMarker)

      // 2 创建Icon至map
      let obj1 = new CreateFubIcon(
        fubObj.name,
        fubObj.surge_val,
        fubObj.surge_dt,
        fubObj.tide_val,
        fubObj.tide_dt
      )

      // 2018-10-16 为点击marker添加点击事件
      // 方式2
      // 此种方式，可以让点击时，获取点击的当前obj
      // 参考：https://blog.csdn.net/ShangQuan2012/article/details/72723734
      // https://leafletjs.com/reference-1.2.0.html#evented中的addEventListener
      // You can optionally specify the context of the listener (object the this keyword will point to)
      // 您可以选择指定侦听器的上下文（这个关键字将指向）
      tempMarker.addEventListener(
        'click',
        function () {
          console.log(obj1)
          // 在此处实现弹出modal窗口，并获取预报曲线
        },
        this
      )

      // 方式1 ：默认方式，只能传递默认的event进来
      let busIcon1 = L.divIcon({
        className: 'icon_default',
        html: obj1.toStr(),
        // 坐标，[相对于原点的水平位置（左加右减），相对原点的垂直位置（上加下减）]
        iconAnchor: [-20, 30]
      })
      // 秀英
      var tempDivIcon = L.marker([fubObj.lat, fubObj.lon], {
        icon: busIcon1
      })

      tempDivIcon.addTo(myself.mymap)
      // 将当前divIcon存起来
      myself.stormIconDivArr.push(tempDivIcon)
    },
    // 浮标图层
    loadFubLayer: function () {
      // 加载浮标图层
      var myself = this
      // var date = new Date()
      // 1 加载station info 存入data的stationArr中
      let fubData = loadFub()
      fubData.then(res => {
        console.log(res.data)
        myself.fubArr = res.data

        $.each(myself.fubArr, function (index, val) {
          myself.fubDict[val.code] = val
        })

        // 2 获取返回当日的极值数据
        let nowDate = new Date()
        let dateStr = getDateStr(nowDate)
        // 由于测试，此处的时间暂时改为"20180807"
        let par = { targetdate: '20180807' }
        myself.stormArr = getStormData(par).then(res => {
          myself.stormArr = res.data
          // 3 生成storm对象
          $.each(myself.stormArr, function (index, val) {
            let stationTemp = null
            if (val.CODE in myself.stationDict) {
              stationTemp = myself.stationDict[val.CODE]
            }
            if (stationTemp != null) {
              var obj = new StormData(
                val.CODE,
                stationTemp.name,
                stationTemp.Lat,
                stationTemp.Lon,
                stationTemp.area,
                val.Surge_VALUE,
                val.Surge_DATE,
                val.Tide_VALUE,
                val.Tide_DATE
              )
              myself.stormObjArr.push(obj)
            }
          })

          // 4 加入地图中
          $.each(myself.stormObjArr, function (index, val) {
            myself.addDiv2Marker(val)
          })
        })
      })
    },
    // 加载浮标图层
    fillFub: function () {
      // 提交给后台的参数
      let par = { targetdate: '20180807' }
      // 加载图层
      this.loadFubLayer()

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
    // this.fillWMS()
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
