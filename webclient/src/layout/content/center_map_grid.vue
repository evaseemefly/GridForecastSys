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
import '../../components/js/map/leaflet'
import '../../components/js/map/leaflet.shpfile'
import shp from 'shpjs'
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
  addshp,
  loadAreaMaxDataByDate,
  // addShape,
  dic2arr,
  compareForecast
} from '../../components/js/map/grid'

import { getDateStr } from '../api/moment_api'
// import maptiles from "../../components/js/map/maptiles"
// map的base子组件
import baseMap from './center_map_base.vue'
export default {
  data () {
    return {
      // forecast_dict:[],
      stationArr: [],
      stationDict: {},
      stormArr: {},
      stormObjArr: [],
      my_shp_layer_arr: [],
      featuresArr: [],
      mymap: null,
      my_shp_layer: null,
      info: null,
      area: 'a'
    }
  },
  components: {
    baseMap
  },
  methods: {
    clearLayer: function () {
      var myself = this
      $.each(myself.my_shp_layer_arr, function (index, value) {
        myself.mymap.removeLayer(value)
      })
      myself.my_shp_layer_arr = []
      myself.mymap.removeLayer(myself.my_shp_layer)
    },

    // grid.js中的代码移至此处
    random_forecast: function (key, count, max) {
      var forecast_dict = {}
      for (var i = 0; i < count; i++) {
        var dict_key = key
        if (i < 10) {
          dict_key += '0' + i
        } else {
          dict_key += i
        }

        //						forecast_dict_test[dict_key] = parseInt(Math.random() * max, 10) + 1;
        forecast_dict[dict_key] = parseInt(Math.random() * max, 10) + 1
      }
      return forecast_dict
    },

    /*
			 * 根据设定好的色带根据传入的值返回对应的rgb颜色的值
			 */

    getColorbar: function (value) {
      // 根据传入的数值（int类型），判断其所属的区件并获取区件的颜色
      var value_color
      if (value >= 2 && value < 4) {
        value_color = 'rgb(0,0,255)'
      } else if (value >= 4 && value < 8) {
        value_color = 'rgb(255,242,0)'
      } else if (value >= 8 && value < 12) {
        value_color = 'rgb(255,127,19)'
      } else if (value >= 12) {
        value_color = 'rgb(255,0,0)'
      }
      return value_color
    },
    addShape: function (dict, data, feature, layer, map) {
      /*
data是读取的geoJson数据
此处已重新修改 2018-08-06
      */

      // 注意此处需要注意判断在featrues_arr中是否已经存在了指定的值（若存在则不添加）
      let myself = this
      $.each(data.features, function (index, obj) {
        if ($.inArray(obj, myself.featuresArr) < 0) {
          myself.featuresArr.push(obj)
        }
      })
      //! !!注意此处添加了shape文件后，由于是读取的geojson，文件，通过L.geoJSON后，需要将返回值赋值给geojson
      // 此处的temp_geojson与geojson相同
      // myself.geojson
      let tempGeoJson = L.geoJSON(data, {
        style: function (feature) {
          // 获取到当前的对象的code

          var code = feature.properties.Code
          // console.log(`color:${code}`)
          let tempColor = null

          if (dict[code]) {
            tempColor = getColorbar(dict[code].HS_VALUE)
          }
          return {
            // 注意此处的填充颜色及宽度的api可参见
            fillColor: tempColor,
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.7
          }
        },
        // 注意此处必须要将OnEachFeature放在里面才可以
        onEachFeature: myself.onEachFeature
      }).bindPopup(function (layer) {
        return layer.feature.properties.description
      })
      // 此处v1版本已经不确定geoJson是否为外侧的geoJson
      let geoJson = tempGeoJson.addTo(map)
      // 需要将genJson赋值给全局geojson
      myself.geojson = geoJson
      return geoJson
    },
    infoInit: function () {
      // 右上角的消息显示区域初始化
      let myself = this
      this.info = L.control()
      this.info.onAdd = function (map) {
        // myself._div = L.DomUtil.create('div', 'info') // create a div with a class "info"
        // myself.update()
        this._div = L.DomUtil.create('div', 'info') // create a div with a class "info"
        this.update()
        return this._div
      }
      // method that we will use to update the control based on feature properties passed
      this.info.update = function (props) {
        // 此处使用了三元表达式
        /*
              由于使用了vue，此处的this应该为info
            */
        // myself.info._div.innerHTML = '<h4>网格概述</h4>' + (props
        //         ? '<b>网格编号：</b><br />' + props.Code
        //         : '未选中')
        this._div.innerHTML =
          '<h4>网格概述</h4>' +
          (props ? '<b>网格编号：</b><br />' + props.Code : '未选中')
      }
      this.info.addTo(myself.mymap)
    },
    // 加载网格化的shp格式文件
    addshp: function (shpPath, dictArea, isremoveLay) {
      var shapeLayer = null
      var myself = this
      // 为当天地图添加图层
      // 注意此处then是异步的，所以无法返回shape_layer;
      shp(shpPath)
        .then(function (tempGeojson) {
          myself.geojson = tempGeojson
          // do something with your geojson
          // 当前图层不为空且删除图层的标记符为true都满足时，才清空当前图层
          if ((myself.my_shp_layer != null) & isremoveLay) {
            $.each(myself.my_shp_layer_arr, function (index, value) {
              myself.mymap.removeLayer(value)
            })
            myself.my_shp_layer_arr = []
            myself.mymap.removeLayer(myself.my_shp_layer)
          }
          var shpLayer = myself.addShape(
            dictArea,
            tempGeojson,
            null,
            null,
            myself.mymap
          )

          // geojson = L.geoJson(temp_geojson, {
          //    style: mystyle,
          //    onEachFeature: onEachFeature
          // }).addTo(mymap);
          myself.my_shp_layer = shpLayer
          myself.my_shp_layer_arr.push(shpLayer)
        })
        .then(function () {
          return shapeLayer
        })
      return shapeLayer
    },
    // 对于每一个feature
    onEachFeature: function (feature, layer) {
      let myself = this
      layer.on({
        mouseover: myself.highlightFeature,
        mouseout: myself.resetHighlight,
        click: myself.zoomToFeature
      })
    },
    // 鼠标划出时恢复正常
    resetHighlight: function (e) {
      this.geojson.resetStyle(e.target)
      this.info.update()
    },
    // 鼠标划入时高亮
    highlightFeature: function (e) {
      var layer = e.target

      layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
      })

      if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront()
      }

      this.info.update(layer.feature.properties)
    },

    readShape: function (file, func) {
      shp('file').then(function (geojson) {
        // do something with your geojson
        func(geojson)
      })
    },

    // 注意加载页面时，需要执行加载全国的事件
    fillGrid: function (value, item) {
      // 此处的item是vm.data中的items
      //
      // console.log("执行填充操作：" + value);
      this.selected = item
      let textIndex = 1
      textIndex += 1

      // 将字典转成arr
      this.arrKeysForecastextreme = []
      this.arrValuesForecastextreme = []
      // var arrObjForecastextreme = []

      var info = this.fillarea(value)
      let dictTarget = info[0]
      // let outGeoLayer = info[1]
      // 从当前地图中删除当前海区的layer，前提是当前海区的layer不为null，否则会报错
      if (dictTarget != null) {
        var forecastArr = dic2arr(dictTarget)
        var forecastArrObj = []
        $.each(forecastArr, function (index, obj) {
          forecastArrObj.push({
            code: obj.value.CODE,
            HS_VALUE: obj.value.HS_VALUE
          })
        })
        this.forecastArr = forecastArrObj.sort(compareForecast('HS_VALUE'))
        // 从数组中取出前10个值
        let forecastTop10 = forecastArr.slice(0, 15)

        for (var i = 0; i < forecastTop10.length; i++) {
          this.arrKeysForecastextreme.push(forecastTop10[i].code)

          this.arrValuesForecastextreme.push(forecastTop10[i].value.HS_VALUE)
        }

        // var bar = this.initbar()
        // this.loadbar(bar, this.arrKeysForecastextreme, this.arrValuesForecastextreme)
      }
      // 传递给子组件
      // 暂时不加载右侧的top10
      // this.$refs.rightBar.load(
      //   this.arrKeysForecastextreme,
      //   this.arrValuesForecastextreme
      // )
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
    }
  },

  watch: {
    '$route' (to, from) {
      // 当每次路由发生变化时，route会发生变化
      console.log(`to:${to},from:${from}`)
      console.log(`${to.params}`)
      // 执行加载风暴潮的相关操作
      // this.fillStorm(to.params.code)
      this.area = to.params.code

    }

  },
  created: function () {
    console.log('view created')
  },
  // created () {
  //   console.log('view created')
  // },
  mounted: function () {
    let code = this.$route.params.code
    // 初始化地图引擎
    // this.initMap()
    // 调用父组件中的初始化地图引擎的方法
    // 注意此处是调用base子组件中的方法，而非父组件
    // this.$emit('initMap')
    this.$refs.baseMap.clear()
    this.infoInit()
    // this.$refs.baseMap.initMap()
    // 缩放至指定海区
    this.$refs.baseMap.zoomView(code)
    this.fillGrid(code)
  }
}
</script>

<style>
#mycontent {
  position: absolute;
  top: 188px;
  bottom: 0px;
  width: 100%;
}
</style>
