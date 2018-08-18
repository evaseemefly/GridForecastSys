<template>
  <!--下部的巨幕-->
  <div id="mycontent" class="col-md-12 mycol_disPadding" style="width: 100%;">
    <div id="basemap" style="height: 100%; width: 100%;">
      <div class="leaflet-control-container">
        <div class="leaflet-top leaflet-left">
          <div class="leaflet-control-zoom leaflet-bar leaflet-control">
            <a class="leaflet-control-zoom-in" href="http://leafletjs.com/examples/choropleth/example.html#" title="Zoom in" role="button" aria-label="Zoom in">+</a>
            <a class="leaflet-control-zoom-out" href="http://leafletjs.com/examples/choropleth/example.html#" title="Zoom out" role="button" aria-label="Zoom out">−</a>
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
      
    </div>
    <!-- 由下边的rightBar组件替代 -->
      <!-- <div id="mybar" style="height:400px"></div> -->
      
    <rightBar ref="rightBar" :arrValuesForecastextreme="arrValuesForecastextreme" :arrKeysForecastextreme="arrKeysForecastextreme"></rightBar>
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

import {
  getColorbar
  } from '../api/api'

import {
  addshp,
  loadAreaMaxDataByDate,
  // addShape,
  dic2arr,
  compareForecast
} from '../../components/js/map/grid'

import {getDateStr} from '../api/moment_api'
// import maptiles from "../../components/js/map/maptiles"
import rightBar from './right_bar.vue'

export default {
  data () {
    return {
      // forecast_dict:[],
      stationArr: [],
      stationDict: {},
      stormArr: {},
      stormObjArr: [],
      forecastArr: [],
      // info: null,
      my_shp_layer_arr: [],
      features_arr: [],
      mymap: null,
      my_shp_layer: null,
      info: null,
      geojson: null,
      // 将forecast_top10字典转成数组的keys
      arrKeysForecastextreme: [],
      // 将forecast_top10字典转成数组的values
      arrValuesForecastextreme: []
    }
  },
  components: {
    rightBar
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

    // getColorbar: function (value) {
    //   // 根据传入的数值（int类型），判断其所属的区件并获取区件的颜色
    //   var value_color
    //   if (value >= 2 && value < 4) {
    //     value_color = 'rgb(0,0,255)'
    //   } else if (value >= 4 && value < 8) {
    //     value_color = 'rgb(255,242,0)'
    //   } else if (value >= 8 && value < 12) {
    //     value_color = 'rgb(255,127,19)'
    //   } else if (value >= 12) {
    //     value_color = 'rgb(255,0,0)'
    //   }
    //   return value_color
    // },

    addShape: function (dict, data, feature, layer, map) {
      /* 叠加shp文件，以geoJson的方式读取
			 * data是读取的geoJson数据
			 * 此处已重新修改 2018-08-06
       */
      // 注意此处需要注意判断在featrues_arr中是否已经存在了指定的值（若存在则不添加）
      let myself = this
      $.each(data.features, function (index, obj) {
        if ($.inArray(obj, myself.features_arr) < 0) {
          myself.features_arr.push(obj)
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
    onEachFeature: function (feature, layer) {
      let myself = this
      layer.on({
        mouseover: myself.highlightFeature,
        mouseout: myself.resetHighlight,
        click: myself.zoomToFeature
      })
    },
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
    resetHighlight: function (e) {
      this.geojson.resetStyle(e.target)
      this.info.update()
    },
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
      this.$refs.rightBar.load(this.arrKeysForecastextreme, this.arrValuesForecastextreme)
    },

    // 加载右侧的柱状图top15
  //   loadbar: function (bar, keys_arr, values_arr) {
  //     let option_mybar = {
  //       title: {
  //         text: '波浪72小时预报',
  //         subtext: '测试数据',
  //         textStyle: {
  //           fontWeight: 'bolder',
  //           color: '#FFFFFF'
  //         }
  //       },
  //       tooltip: {
  //         trigger: 'axis',
  //         axisPointer: {
  //           type: 'shadow'
  //         }
  //       },
  //       legend: {
  //         data: ['波浪']
  //       },
  //       grid: {
  //         left: '3%',
  //         right: '4%',
  //         bottom: '3%',
  //         containLabel: true
  //       },
  //       xAxis: {
  //         type: 'value',
  //         boundaryGap: [0, 0.01],
  //         axisLabel: {
  //           interval: 0,
  //           textStyle: {
  //             color: '#ddd'
  //           }
  //         },
  //         axisLine: {
  //           show: false,
  //           lineStyle: {
  //             color: '#ddd'
  //           }
  //         },
  //         splitLine: {
  //           show: false // 不显示网格线
  //         }
  //       },
  //       yAxis: {
  //         type: 'category',
  //         splitLine: {
  //           show: false // 不显示网格线
  //         },
  //         axisLabel: {
  //           interval: 0,
  //           textStyle: {
  //             color: '#FFFFFF',
  //             fontWeight: 'bold'
  //           }
  //         },
  //         data: keys_arr
  //       },
  //       series: [
  //         {
  //           name: '波浪',
  //           type: 'bar',
  //           data: values_arr,
  //           itemStyle: {
  //         // 通常情况下：
  //             normal: {
  //           //	color: '#EEC900'
  //           // 每个柱子的颜色即为colorList数组里的每一项，如果柱子数目多于colorList的长度，则柱子颜色循环使用该数组
  //               color: function (params) {
  //                 var mycolor = this.getColorbar(params.data)

  //                 return mycolor
  //               }
  //             },
  //         // 鼠标悬停时：
  //             emphasis: {
  //               shadowBlur: 10,
  //               shadowOffsetX: 0,
  //               shadowColor: 'rgba(0, 0, 0, 0.5)'
  //             }
  //           }
  //         }
  //       ]
  //     }
  // // 为echarts对象加载数据
  //     bar.setOption(option_mybar)
  //   },

  //   initbar: function () {
  //     var myBar = echarts.init(document.getElementById('mybar'))
  //     return myBar
  //   },
    // addshp: function (shpPath, dict_area, isremoveLay) {
    //   let shapeLayer = null
    // // 为当天地图添加图层
    // // 注意此处then是异步的，所以无法返回shape_layer;
    //   shp(shpPath).then(function (tempGeojson) {
    //     // geojson = temp_geojson
    //     // do something with your geojson
    //     // 当前图层不为空且删除图层的标记符为true都满足时，才清空当前图层
    //     if (my_shp_layer != null & isremoveLay) {
    //       $.each(my_shp_layer_arr, function (index, value) {
    //         mymap.removeLayer(value)
    //       })
    //       my_shp_layer_arr = []
    //       mymap.removeLayer(my_shp_layer)
    //     }
    //     var shp_layer = addShape(dict_area, tempGeojson, null, null, mymap)

    //     // geojson = L.geoJson(temp_geojson, {
    //     //    style: mystyle,
    //     //    onEachFeature: onEachFeature
    //     // }).addTo(mymap);
    //     my_shp_layer = shp_layer
    //     my_shp_layer_arr.push(shp_layer)
    //   }).then(function () {
    //     return shapeLayer
    //   })
    //   return shape_layer
    // },
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
      this.zoomView(code)
    },
    loadStationInfo: function () {
      let myself = this
      let stationInfo = loadStation()
      stationInfo.then(res => {
        console.log(res.data)
        myself.stationArr = res.data
      })
    },

    loadStormLayer: function () {
      // 加载风暴潮图层
      var myself = this
      // var date = new Date()
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
      })
    },

    addDiv2Marker (stormObj) {
      let myself = this
      L.marker([stormObj.lat, stormObj.lon])
      .addTo(myself.mymap)
      .bindPopup('')

      let obj1 = new CreateStationIcon(
    stormObj.name,
    stormObj.surge_val,
    stormObj.surge_dt,
    stormObj.tide_val,
    stormObj.tide_dt
      )

      let busIcon1 = L.divIcon({
        className: 'icon_default',
        html: obj1.toStr(),
    // 坐标，[相对于原点的水平位置（左加右减），相对原点的垂直位置（上加下减）]
        iconAnchor: [-20, 30]
      })

  // 秀英
      L.marker([stormObj.lat, stormObj.lon], {
        icon: busIcon1
      }).addTo(myself.mymap)
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
        this._div.innerHTML = '<h4>网格概述</h4>' + (props
                ? '<b>网格编号：</b><br />' + props.Code
                : '未选中')
      }
      this.info.addTo(myself.mymap)
    },
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

    initMap: function () {
      var myself = this
      myself.mymap = L.map('basemap').setView([30.09, 127.75], 5)
      // var mymap = L.map('basemap').setView([51.505, -0.09], 13)
      // mapLink = "../static/mapfiles/";

      L.tileLayer('../../../static/img/mapfiles/{z}/{x}/{y}.jpg', {
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
    }
  },

  watch: {
    '$route' (to, from) {
      // 当每次路由发生变化时，route会发生变化
      console.log(`to:${to},from:${from}`)
      console.log(`${to.params}`)
      // 执行加载风暴潮的相关操作
      // 此处需要判断要执行的加载内容
      let category = to.params.category
      switch (category) {
        case 'storm':
          console.log('storm')
          this.fillStorm(to.params.code)
          break
        case 'grid':
          console.log('grid')
          this.fillGrid(to.params.code)
          break
      }
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
    this.initMap()
    // 缩放至指定海区
    this.zoomView(code)
    // 对info初始化
    this.infoInit()
    let par = { targetdate: '20180807' }
    getStormData(par)
    this.loadStormLayer()
    // .then(function (res) {
    //   console.log(res)
    // })

    // alert(get_data);
    // var myself = this;
    // this.info = L.control();
    // info.onAdd = function(map) {
    //   this._div = L.DomUtil.create("div", "info"); // create a div with a class "info"
    //   this.update();
    //   return this._div;
    // };
    // info.update = function(props) {
    //   //此处使用了三元表达式
    //   this._div.innerHTML =
    //     "<h4>网格概述</h4>" +
    //     (props ? "<b>网格编号：</b><br />" + props.Code : "未选中");
    // };
    // //此处有个问题
    // this.info.addTo(myself.mymap);
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
