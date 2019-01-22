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
import shp from 'shpjs'

import { mapGetters } from 'vuex'
// 引入 ECharts 主模块
var echarts = require('echarts/lib/echarts')
// 引入柱状图
require('echarts/lib/chart/bar')
// 引入提示框和标题组件
require('echarts/lib/component/tooltip')
require('echarts/lib/component/title')

import {
  loadStation,
  getStormData,
  loadStormLayer,
  StormData,
  CreateStationIcon
} from '../../components/js/map/storm'

import { getDateStr } from '../api/moment_api'

// map的base子组件
import baseMap from './center_map_base.vue'
// modal子组件
import modalFrame from '../module/modal.vue'
export default {
  data () {
    return {
      stationArr: [],
      stationDict: {},
      stormArr: {},
      stormObjArr: [],
      my_shp_layer_arr: [],
      mymap: null,
      my_shp_layer: null,
      info: null
    }
  },
  components: {
    baseMap,
    modalFrame
    // dateModule
  },
  methods: {
    loadStormLayer: function (targetDate) {
      // 加载海洋站格点
      /*
       ** 经测试此种方式可行：
            需要加入的流程还有：每次点击此方法时，需要清空layer，并清空加载grid的layerßß
      */
      // S1 删除现有图层
      var myself = this
      // this.clearLayer()

      // 以下为storm.js中的代码，放在此处
      // 1 先加载station list
      // this.loadStationData()
      // $.each(myself.stationArr, function (index, val) {
      //   // console.log(val);
      //   myself.station_dict[val.code] = val
      // })

      // 1 加载station info 存入data的stationArr中
      // this.loadStationInfo()
      let stationInfo = loadStation()
      stationInfo.then(res => {
        console.log(res.data)
        myself.stationArr = res.data

        $.each(myself.stationArr, function (index, val) {
          myself.stationDict[val.code] = val
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
        // 2 获取返回的当日极值数据
        // var dateStr = myself.getDateStr(target_date)
        // var stormArr = myself.loadStormData(dateStr)

        // // 3 生成storm对象
        // $.each(stormArr, function (index, val) {
        //   var stationTemp = null
        //   if (val.CODE in myself.station_dict) {
        //     stationTemp = myself.station_dict[val.CODE]
        //   }
        //   if (stationTemp != null) {
        //     var obj = new StormData(
        //       val.CODE,
        //       stationTemp.name,
        //       stationTemp.Lat,
        //       stationTemp.Lon,
        //       stationTemp.area,
        //       val.Surge_VALUE,
        //       val.Surge_DATE,
        //       val.Tide_VALUE,
        //       val.Tide_DATE
        //     )
        //     myself.storm_obj_arr.push(obj)
        //   }
        // })
        // $.each(myself.storm_obj_arr, function (index, val) {
        //   myself.addDiv2Marker(val)
        // })
      })
    },
    clearLayer: function () {
      var myself = this
      $.each(myself.my_shp_layer_arr, function (index, value) {
        myself.mymap.removeLayer(value)
      })
      myself.my_shp_layer_arr = []
      myself.mymap.removeLayer(myself.my_shp_layer)
    },
    createStationIcon: function (name, surge, surgeDt, tide, tideDt) {
      /*
          name:海洋站名称
          surge:增水
          surgeDt:最大增水出现时间
          tide:最高潮位
          tideDt：最高潮位出现时间
      */
      this.name = name
      this.surge = surge
      this.surgeDt = surgeDt
      this.surge_cls = ''
      this.tide = tide
      this.tideDt = tideDt
      this.tide_cls = ''
      this.surge_cls = getAlarmLevel(this.surge)
      this.tide_cls = getAlarmLevel(this.tide)
      // 需要根据传入的增水以及警戒潮位为添加不同的样式
      //
      /*
      自定义的等级共五种
          无警报：    norm
          蓝色：0-2   1st
          黄色：2-4   2nd
          橙色：4-8   3rd
          红色：8-12  4th
      */
      this.toStr = function () {
        var htmlStr = '<div class="myform"><table ><tr><td width="100" rowspan="2">{0}</td><td class="{1}" width="100">{2}</td><td class="{3}" width="100">{4} </td></tr><tr><td class="{5}" width="100">{6}</td><td class="{7}">{8}</td></tr></table></div>'.format(
          this.name,
          this.surge_cls,
          this.surge,
          this.surge_cls,
          this.surgeDt,
          this.tide_cls,
          this.tide,
          this.tide_cls,
          this.tideDt
        )
        return htmlStr
      }
    },
    getStormData: function () {
      $.ajax({
        url: './data/storm_data.json',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
          console.log(data)
          return data
        }
      })
    },

    loadStationData: function () {
      // 获取全部海洋站信息
      // var stationData = null
      // var stationUrl = '/station/list/'
      // $.ajax({
      //   url: stationUrl,
      //   type: 'GET',
      //   dataType: 'json',
      //   async: false,
      //   success: function (data) {
      //     // console.log(data);
      //     stationData = data
      //   }
      // })
      // return stationData
      var myself = this
      loadStation().then(res => {
        myself.stationArr = res.data
      })
    },

    getAlarmLevel: function (val) {
      /*
          func:根据传入的值返回预警报等级
          params:
              val:增水或潮位值
          return:
              警报等级（str）
      */
      /*
      自定义的等级共五种
          无警报：    norm
          蓝色：0-2   info  least
          黄色：2-4   2nd   medium
          橙色：4-8   3rd   more
          红色：8-12  4th   most
      */
      var level = 'norm'
      if (val < 2) {
        level = 'least'
      } else if ((val < 4) & (val >= 2)) {
        level = 'medium'
      } else if ((val < 8) & (val > 4)) {
        level = 'more'
      } else if (val > 8) {
        level = 'most'
      }
      return level
    },

    addDiv2Marker: function (stormObj) {
      var myself = this
      // L.marker([stormObj.lat, stormObj.lon])
      //   .addTo(myself.mymap)
      //   .bindPopup('')
      // 1 添加marker至map
      var tempMarker = L.marker([stormObj.lat, stormObj.lon])
      tempMarker.addTo(myself.mymap)
      var obj_1 = new CreateStationIcon(
        stormObj.name,
        stormObj.surge_val,
        stormObj.surge_dt,
        stormObj.tide_val,
        stormObj.tide_dt
      )
      var busIcon_1 = L.divIcon({
        className: 'icon_default',
        html: obj_1.toStr(),
        // 坐标，[相对于原点的水平位置（左加右减），相对原点的垂直位置（上加下减）]
        iconAnchor: [-20, 30]
      })

      // 秀英
      L.marker([stormObj.lat, stormObj.lon], {
        icon: busIcon_1
      }).addTo(myself.mymap)
    },

    loadStormData: function (getData) {
      var stormData = []
      var stormUrl = '/storm/daily/'
      // 获取当日的风暴潮预报值
      $.ajax({
        url: stormUrl,
        type: 'GET',
        dataType: 'json',
        data: { targetdate: getData },
        async: false,
        success: function (data) {
          // console.log(data);
          stormData = data
        }
      })
      return stormData
    },
    // 加载风暴潮及增水
    fillStorm: function (code) {
      /*
        新写的方法：
          加载风暴潮及增水的相关操作（入口方法）
          根据传入的code：
            1）聚焦到指定海区
            2）
          remark：
            第一次加载该页面时，已经加载了全部的海洋站信息（statinInfo）
            以及
            风暴潮及增水的极值数据（stormData）
            所以此处先只执行zoom操作
      */
      let par = { targetdate: '20180807' }
      getStormData(par)
      this.loadStormLayer()
      // this.zoomView(code)
    }
  },
  mounted: function () {
    let code = this.$route.params.code
    console.log('view mounted')
    // 以下部分在子组件中
    // 初始化地图引擎 
    // 清除全部已叠加的图层
    // 注意此处需要调用子组件中的方法
    // this.clear()
    this.$refs.baseMap.clear()
    // 填充数值预报
    this.fillStorm(code)
  }
}
</script>

<style>
</style>
