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
      <div id="mybar" style="height:400px"></div>
    </div>
  </div>
</template>

<script>
import '../../components/js/map/leaflet'
import '../../components/js/map/leaflet.shpfile'
import '../../components/js/map/shp'
// import {StormData,loadStormLayer,createStationIcon,getStormData,loadStationData,getAlarmLevel,addDiv2Marker,loadStormData} "../../comppnents/js/map/storm.js";
// import {loadStormData} from "../../comppnents/js/map/storm";
// import {area} from "../../components/js/map/mytest";
import { loadStormData, getSotrmData } from '../../components/js/map/storm'
// import maptiles from "../../components/js/map/maptiles"

export default {
  data () {
    return {
      // forecast_dict:[],
      station_arr: [],
      station_dict: [],
      storm_arr: [],
      storm_obj_arr: [],
      my_shp_layer_arr: [],
      mymap: null,
      my_shp_layer: null,
      info: null
    }
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

    /*
			 * 叠加shp文件，以geoJson的方式读取
			 * data是读取的geoJson数据
			 * 此处已重新修改 2018-08-06
			 */
    addShape: function (dict, data, feature, layer, map) {
      // 注意此处需要注意判断在featrues_arr中是否已经存在了指定的值（若存在则不添加）
      $.each(data.features, function (index, obj) {
        if ($.inArray(obj, features_arr) < 0) {
          features_arr.push(obj)
        }
      })
      //! !!注意此处添加了shape文件后，由于是读取的geojson，文件，通过L.geoJSON后，需要将返回值赋值给geojson
      // 此处的temp_geojson与geojson相同
      var temp_geojson = L.geoJSON(data, {
        style: function (feature) {
          // 获取到当前的对象的code
          var code = feature.properties.Code
          var temp_color = null
          //							forecast_dict_test
          if (dict[code]) {
            temp_color = this.getColorbar(dict[code].HS_VALUE)
          }
          return {
            // 注意此处的填充颜色及宽度的api可参见
            fillColor: temp_color,
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.7
          }
        },
        // 注意此处必须要将OnEachFeature放在里面才可以
        onEachFeature: onEachFeature
      }).bindPopup(function (layer) {
        return layer.feature.properties.description
      })

      geojson = temp_geojson.addTo(map)
      return geojson
    },

    addshp: function (shp_path, dict_area, isremoveLay) {
      var shape_layer = null
      var myself = this
      // 为当天地图添加图层
      // 注意此处then是异步的，所以无法返回shape_layer;
      shp(shp_path)
        .then(function (temp_geojson) {
          geojson = temp_geojson
          // do something with your geojson
          // 当前图层不为空且删除图层的标记符为true都满足时，才清空当前图层
          if ((myself.my_shp_layer != null) & isremoveLay) {
            $.each(myself.my_shp_layer_arr, function (index, value) {
              myself.mymap.removeLayer(value)
            })
            myself.my_shp_layer_arr = []
            myself.mymap.removeLayer(myself.my_shp_layer)
          }
          var shp_layer = addShape(
            dict_area,
            temp_geojson,
            null,
            null,
            myself.mymap
          )

          // geojson = L.geoJson(temp_geojson, {
          //    style: mystyle,
          //    onEachFeature: onEachFeature
          // }).addTo(mymap);
          myself.my_shp_layer = shp_layer
          myself.my_shp_layer_arr.push(shp_layer)
        })
        .then(function () {
          return shape_layer
        })
      return shape_layer
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

      info.update(layer.feature.properties)
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
    fillarea: function (value, item) {
      // 此处的item是vm.data中的items
      //
      // console.log("执行填充操作：" + value);
      this.selected = item
      text_index += 1
      // 将字典转成arr
      var arr_keys_forecastextreme = []
      var arr_values_forecastextreme = []
      var arr_obj_forecastextreme = []

      var info = fillarea(value)
      dict_target = info[0]
      out_geo_layer = info[1]
      // 从当前地图中删除当前海区的layer，前提是当前海区的layer不为null，否则会报错
      if (dict_target != null) {
        var forecast_arr = dic2arr(dict_target)
        var forecast_arr_obj = []
        $.each(forecast_arr, function (index, obj) {
          forecast_arr_obj.push({
            code: obj.value.CODE,
            HS_VALUE: obj.value.HS_VALUE
          })
        })
        forecast_arr = forecast_arr_obj.sort(compare_forecast('HS_VALUE'))
        // 从数组中取出前10个值
        var forecast_top10 = forecast_arr.slice(0, 15)

        for (var i = 0; i < forecast_top10.length; i++) {
          arr_keys_forecastextreme.push(forecast_top10[i].code)

          arr_values_forecastextreme.push(forecast_top10[i].HS_VALUE)
        }

        var bar = initbar()
        loadbar(bar, arr_keys_forecastextreme, arr_values_forecastextreme)
      }
    },
    initMap: function () {
      var mymap = L.map('basemap').setView([30.09, 127.75], 5)
      // var mymap = L.map('basemap').setView([51.505, -0.09], 13)
      // mapLink = "../static/mapfiles/";

      L.tileLayer('../../static/img/mapfiles/{z}/{x}/{y}.jpg', {
        attribution: '',
        maxZoom: 8,
        minZoom: 2
      }).addTo(mymap)
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
          if (rectangleMeasure.rectangle) { rectangleMeasure.layer.removeLayer(rectangleMeasure.rectangle) }
          if (rectangleMeasure.tips) { rectangleMeasure.layer.removeLayer(rectangleMeasure.tips) }
        }
      }
    }
  },
  mounted: function () {
    this.initMap()
    // var index= area(123123);
    // alert(index);
    // var storm_data= getstorm('2018-08-02');

    // loadStormData("2018-08-02").then(function(res) {
    //   console.log(res);
    // });
    getSotrmData({targetdate: '20180807'})
    .then(function (res) {
      console.log(res)
    })

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
}
</style>
