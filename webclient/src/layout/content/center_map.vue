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

export default {
  data () {
    return {
      // forecastDict:[],
      stationArr: [],
      stationDict: {},
      stormArr: {},
      stormObjArr: [],
      // 海洋站的marker数组
      stormMarkerArr: [],
      // 海洋站的IconDiv数组
      stormIconDivArr: [],
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

    // grid.js中的代码移至此处
    random_forecast: function (key, count, max) {
      var forecastDict = {}
      for (var i = 0; i < count; i++) {
        var dictKey = key
        if (i < 10) {
          dictKey += '0' + i
        } else {
          dictKey += i
        }

        // forecastDict_test[dictKey] = parseInt(Math.random() * max, 10) + 1;
        forecastDict[dictKey] = parseInt(Math.random() * max, 10) + 1
      }
      return forecastDict
    },

    /*
根据设定好的色带根据传入的值返回对应的rgb颜色的值
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
      /*
data是读取的geoJson数据
此处已重新修改 2018-08-06
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
      this.$refs.rightBar.load(
        this.arrKeysForecastextreme,
        this.arrValuesForecastextreme
      )
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
      this.zoomView(code)
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
      this.mymap.on('click', function (e) {
        console.log(e)
        // 获取经纬度对象
        // var cornerStr=e.latlng.toBounds()

        var latLng = L.latLng(e.latlng.lat, e.latlng.lng)
        // var corner1=L.latlng(e.latlng.lat,e.latlng.lng)

        // var cornerStr=corner1.toBBoxString()
        console.log(cornerStr)
      })
    },
    loadStationInfo: function () {
      let myself = this
      let stationInfo = loadStation()
      stationInfo.then(res => {
        // console.log(res.data)
        myself.stationArr = res.data
      })
    },

    // 加载风暴潮增水图层
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

    // 创建海洋站的潮位数据的div显示框
    addDiv2Marker (stormObj) {
      let myself = this
      // 1 添加marker至map
      var tempMarker = L.marker([stormObj.lat, stormObj.lon])
      tempMarker.addTo(myself.mymap)
      // .bindPopup('')

      myself.stormMarkerArr.push(tempMarker)

      // 2 创建Icon至map
      let obj1 = new CreateStationIcon(
        stormObj.name,
        stormObj.surge_val,
        stormObj.surge_dt,
        stormObj.tide_val,
        stormObj.tide_dt
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
      // tempMarker.on('click', (e) => {
      //   console.log(e)
      //   console.log(obj)

      //   // alert('被点击了')
      // }, obj1)

      let busIcon1 = L.divIcon({
        className: 'icon_default',
        html: obj1.toStr(),
        // 坐标，[相对于原点的水平位置（左加右减），相对原点的垂直位置（上加下减）]
        iconAnchor: [-20, 30]
      })
      // 秀英
      var tempDivIcon = L.marker([stormObj.lat, stormObj.lon], {
        icon: busIcon1
      })

      tempDivIcon.addTo(myself.mymap)
      // 将当前divIcon存起来
      myself.stormIconDivArr.push(tempDivIcon)
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
          this.fillGrid(to.params.code)
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
    }
  },

  created: function () {
    // console.log('view created')
  },

  mounted: function () {
    let code = this.$route.params.code
    // 初始化地图引擎
    this.initMap()
    // 缩放至指定海区
    this.zoomView(code)
    // 对info初始化
    this.infoInit()

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
