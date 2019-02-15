<template>
  <div>
    <baseMap
      ref="baseMap"
      :basemap.sync='mymap'
    ></baseMap>
    <!-- <dateModule @changeLayerIndex="changeLayerIndex"></dateModule> -->
    <modalFrame
      ref="modal"
      :columns='modalColumns'
      :values='modalValues'
    ></modalFrame>
  </div>
</template>

<script>
import 'leaflet'
import 'leaflet-rotatedmarker'
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
import {
  getColorbar,
  loadFubStormData,
  loadFubDetailStormData} from '../api/api'

import { getDateStr } from '../api/moment_api'
import rightBar from './right_bar.vue'
// map的base子组件
import baseMap from './center_map_base.vue'
// modal子组件
import modalFrame from '../member/modal/modal_main.vue'
// import modalFrame from '../module/modal.vue'

import {
  CreateFubIcon,
  FubStormData,
  loadFub,
  getFubData
} from '../../components/js/map/fub.js'
// import dateModule from '../module/date_select_module.vue'
export default {
  data () {
    return {
      // 加载预报产品需要的data
      mymap: null,
      // forecastDict:[],
      fubArr: [],
      fubids: [],
      fubStormArr: [],
      fubDict: {},
      fubObjArr: [],
      // 浮标的marker数组
      fubMarkerArr: [],
      // 浮标的IconDiv数组
      fubIconDivArr: [],
      selectFubId: null,
      targetDate: null,
      // wms_lng,
      latlng: null,
      modalTitle: '',

      // 传递给modal框的columns以及values的数组
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

    // 当vuex中的latlng修改后，也修改此处的latlng，并展示modal框
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
    // 在地图上加入qf的divIcon
    addDiv2Marker: function (fubObj) {
      let myself = this
      // 1 添加marker至map
      var tempMarker = L.marker([fubObj.lat, fubObj.lon])
      tempMarker.addTo(myself.mymap).on('click', function (e) {
        // alert(fubObj)
        console.log(fubObj)
        myself.showModal(fubObj.code)
      })

      myself.fubMarkerArr.push(tempMarker)

      // 2 创建Icon至map
      let obj1 = new CreateFubIcon(
        fubObj.code,
        fubObj.name,
        fubObj.lat,
        fubObj.lon,
        fubObj.area,
        fubObj.maxwave,
        fubObj.period,
        fubObj.date,
        fubObj.direction
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

      // 对于需要加载方向的
      this.addDirIcon(fubObj.lat, fubObj.lon, fubObj.direction)

      // 将当前divIcon存起来
      myself.fubIconDivArr.push(tempDivIcon)
    },
    // 添加带箭头的icon
    addDirIcon: function (lat, lon, dir) {
      var myself = this
      var dirIcon = L.icon({
        iconUrl: '../../../static/img/icon/arrows.png',
        iconSize: [24.6, 20],
        iconAnchor: [0, 0],
        popupAnchor: [-3, -76]
      })
      L.marker([lat, lon], {
        icon: dirIcon,
        rotationAngle: dir - 90
      }).addTo(myself.mymap)
    },
    // 浮标图层
    loadFubLayer: function () {
      // 加载浮标图层
      var myself = this
      // var date = new Date()
      // 1 加载station info 存入data的stationArr中
      let fubData = loadFub()
      myself.fubArr = []
      fubData.then(res => {
        // 判断状态是否正确
        if (res.status === 200) {
          // 若正确取出里面的data
          myself.fubArr = res.data
          $.each(myself.fubArr, function (index, val) {
            myself.fubDict[val.code] = val
            myself.fubids.push(val.fid)
            var fubTemp = new FubStormData(
              val.code,
              val.code,
              val.lat,
              val.lon,
              null,
              val.wv,
              val.wvperiod,
              val.timestamp,
              val.wvd
            )
            myself.fubObjArr.push(fubTemp)
          })

          // 2 获取返回当日的极值数据
          let nowDate = new Date()
          let dateStr = getDateStr(nowDate)
          // 由于测试，此处的时间暂时改为"20180807"
          // let par = { nowdate: '2018-11-18', ids: myself.fubids }
          // getFubData(par).then(res => {
          //   console.log(res)
          //   myself.fubStormArr = res.data

          //   // 3 生成storm对象
          //   $.each(myself.fubStormArr, function (index, val) {
          //     let fubTemp = null
          //     if (val.fid.code in myself.fubDict) {
          //       // fubTemp = myself.fubDict[val.fid.code]
          //       fubTemp = val
          //     }
          //     let fubInfoTemp = fubTemp.fid
          //     if (fubTemp != null) {
          //       var obj = new FubStormData(
          //         fubInfoTemp.code,
          //         fubInfoTemp.name,
          //         fubInfoTemp.Lat,
          //         fubInfoTemp.Lon,
          //         fubInfoTemp.area,
          //         fubTemp.wv,
          //         fubTemp.period,
          //         fubTemp.tdate,
          //         fubTemp.wvc
          //       )
          //       myself.fubObjArr.push(obj)
          //     }
          //   })

          // $.each(myself.fubStormArr, function (index, val) {
          //   let fubTemp = null
          //   if (val.fid.code in myself.fubDict) {
          //     // fubTemp = myself.fubDict[val.fid.code]
          //     fubTemp = val
          //   }
          //   let fubInfoTemp = fubTemp.fid
          //   if (fubTemp != null) {
          //     var obj = new FubStormData(
          //       fubInfoTemp.code,
          //       fubInfoTemp.name,
          //       fubInfoTemp.Lat,
          //       fubInfoTemp.Lon,
          //       fubInfoTemp.area,
          //       fubTemp.wv,
          //       fubTemp.period,
          //       fubTemp.tdate,
          //       fubTemp.wvc
          //     )
          //     myself.fubObjArr.push(obj)
          //   }
          // })

          // 4 加入地图中
          $.each(myself.fubObjArr, function (index, val) {
            myself.addDiv2Marker(val)
          })        }
      })
    },
    // 加载浮标图层
    fillFub: function () {
      // 提交给后台的参数
      let par = { targetdate: '20180807' }
      // 加载图层
      this.loadFubLayer()
    },
    // 加载modal框，调用modal框组件并显示
    showModal: function (code) {
      var myself = this
      // 以下为测试使用，生产环境下仍需修改
      myself.selectFubId = 1
      myself.targetDate = '2018-11-18 19:00'
      this.$refs.modal.showModal(code)
      // loadFubDetailStormData({ id: myself.selectFubId, nowdate: myself.targetDate }).then(res => {
      //   console.log(res.data)
      //   var columns = []
      //   var values = []
      //   $.each(res.data, function (index, val) {
      //     columns.push(val.tdate)
      //     values.push(val.wv)
      //   })
      //   myself.modalColumns = columns
      //   myself.modalValues = values
      //   // 调用modal子组件的showModal方法，打开modal框
      //   this.$refs.modal.showModal()
      // })
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
    this.loadFubLayer()
    // 填充数值预报
    // this.fillWMS()
    console.log('view mounted')
  }
}
</script>

<style scoped>
#mycontent {
  position: absolute;
  top: 188px;
  bottom: 0px;
  width: 100%;
  overflow: hidden;
}
.fub_name {
  background-color: #2f4154;
}
#fub_name {
  background-color: #2f4154;
}
</style>
