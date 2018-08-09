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
import maptiles from "../../components/js/map/maptiles.js";

export default {
  data() {
    return {
      station_arr: [],
      station_dict: [],
      storm_arr: [],
      storm_obj_arr: [],
      my_shp_layer_arr: [],
      mymap: null
    };
  },
  methods: {
    loadStormLayer: function(targetDate) {
      // 加载海洋站格点
      /*
       ** 经测试此种方式可行：
            需要加入的流程还有：每次点击此方法时，需要清空layer，并清空加载grid的layer

      */
      // S1 删除现有图层
      var myself = this;
      this.clearLayer();

      // 以下为storm.js中的代码，放在此处
      // 1 先加载station list
      this.station_arr = this.loadStationData();
      $.each(station_arr, function(index, val) {
        // console.log(val);
        myself.station_dict[val.code] = val;
      });
      // 2 获取返回的当日极值数据
      var date_str = myself.getDateStr(target_date);
      storm_arr = myself.loadStormData(date_str);

      // 3 生成storm对象
      $.each(storm_arr, function(index, val) {
        var station_temp = null;
        if (val.CODE in myself.station_dict) {
          station_temp = myself.station_dict[val.CODE];
        }
        if (station_temp != null) {
          var obj = new StormData(
            val.CODE,
            station_temp.name,
            station_temp.Lat,
            station_temp.Lon,
            station_temp.area,
            val.Surge_VALUE,
            val.Surge_DATE,
            val.Tide_VALUE,
            val.Tide_DATE
          );
          myself.storm_obj_arr.push(obj);
        }
      });
      // add2Marker();
      $.each(myself.storm_obj_arr, function(index, val) {
        myself.addDiv2Marker(val);
      });
      // alert("我是外部方法test2");
    },

    clearLayer: function() {
      $.each(myself.my_shp_layer_arr, function(index, value) {
        mymap.removeLayer(value);
      });
      myself.my_shp_layer_arr = [];
      mymap.removeLayer(my_shp_layer);
    },
    createStationIcon: function(name, surge, surge_dt, tide, tide_dt) {
      /*
          name:海洋站名称
          surge:增水
          surge_dt:最大增水出现时间
          tide:最高潮位
          tide_dt：最高潮位出现时间
      */
      this.name = name;
      this.surge = surge;
      this.surge_dt = surge_dt;
      this.surge_cls = "";
      this.tide = tide;
      this.tide_dt = tide_dt;
      this.tide_cls = "";
      this.surge_cls = getAlarmLevel(this.surge);
      this.tide_cls = getAlarmLevel(this.tide);
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
      this.toStr = function() {
        var html_str = '<div class="myform"><table ><tr><td width="100" rowspan="2">{0}</td><td class="{1}" width="100">{2}</td><td class="{3}" width="100">{4} </td></tr><tr><td class="{5}" width="100">{6}</td><td class="{7}">{8}</td></tr></table></div>'.format(
          this.name,
          this.surge_cls,
          this.surge,
          this.surge_cls,
          this.surge_dt,
          this.tide_cls,
          this.tide,
          this.tide_cls,
          this.tide_dt
        );
        return html_str;
      };
    },
    getStormData: function() {
      $.ajax({
        url: "./data/storm_data.json",
        type: "GET",
        dataType: "json",
        success: function(data) {
          console.log(data);
          return data;
        }
      });
    },

    loadStationData: function() {
      // 获取全部海洋站信息
      var station_data = null;
      var station_url = "/station/list/";
      $.ajax({
        url: station_url,
        type: "GET",
        dataType: "json",
        async: false,
        success: function(data) {
          // console.log(data);
          station_data = data;
        }
      });
      return station_data;
    },

    getAlarmLevel: function(val) {
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
      var level = "norm";
      if (val < 2) {
        level = "least";
      } else if ((val < 4) & (val >= 2)) {
        level = "medium";
      } else if ((val < 8) & (val > 4)) {
        level = "more";
      } else if (val > 8) {
        level = "most";
      }
      return level;
    },

    addDiv2Marker: function(storm_obj) {
      var myself = this;
      L.marker([storm_obj.lat, storm_obj.lon])
        .addTo(myself.mymap)
        .bindPopup("");

      var obj_1 = new myself.createStationIcon(
        storm_obj.name,
        storm_obj.surge_val,
        storm_obj.surge_dt,
        storm_obj.tide_val,
        storm_obj.tide_dt
      );

      var busIcon_1 = L.divIcon({
        className: "icon_default",
        html: obj_1.toStr(),
        // 坐标，[相对于原点的水平位置（左加右减），相对原点的垂直位置（上加下减）]
        iconAnchor: [-20, 30]
      });

      // 秀英
      L.marker([storm_obj.lat, storm_obj.lon], {
        icon: busIcon_1
      }).addTo(myself.mymap);
    },

    loadStormData: function(get_data) {
      var storm_data = [];
      var storm_url = "/storm/daily/";
      // 获取当日的风暴潮预报值
      $.ajax({
        url: storm_url,
        type: "GET",
        dataType: "json",
        data: { targetdate: get_data },
        async: false,
        success: function(data) {
          // console.log(data);
          storm_data = data;
        }
      });
      return storm_data;
    },

    //grid.js中的代码移至此处
    random_forecast: function(key, count, max) {
      var forecast_dict = {};
      for (var i = 0; i < count; i++) {
        var dict_key = key;
        if (i < 10) {
          dict_key += "0" + i;
        } else {
          dict_key += i;
        }

        //						forecast_dict_test[dict_key] = parseInt(Math.random() * max, 10) + 1;
        forecast_dict[dict_key] = parseInt(Math.random() * max, 10) + 1;
      }
      return forecast_dict;
    },

    /*
			 * 根据设定好的色带根据传入的值返回对应的rgb颜色的值
			 */
    getColorbar: function(value) {
      //根据传入的数值（int类型），判断其所属的区件并获取区件的颜色
      var value_color;
      if (value >= 2 && value < 4) {
        value_color = "rgb(0,0,255)";
      } else if (value >= 4 && value < 8) {
        value_color = "rgb(255,242,0)";
      } else if (value >= 8 && value < 12) {
        value_color = "rgb(255,127,19)";
      } else if (value >= 12) {
        value_color = "rgb(255,0,0)";
      }
      return value_color;
    },

    /*
			 * 叠加shp文件，以geoJson的方式读取
			 * data是读取的geoJson数据
			 * 此处已重新修改 2018-08-06
			 */
    addShape: function(dict, data, feature, layer, map) {
      //注意此处需要注意判断在featrues_arr中是否已经存在了指定的值（若存在则不添加）
      $.each(data.features, function(index, obj) {
        if ($.inArray(obj, features_arr) < 0) {
          features_arr.push(obj);
        }
      });
      //!!!注意此处添加了shape文件后，由于是读取的geojson，文件，通过L.geoJSON后，需要将返回值赋值给geojson
      //此处的temp_geojson与geojson相同
      var temp_geojson = L.geoJSON(data, {
        style: function(feature) {
          //获取到当前的对象的code
          var code = feature.properties.Code;
          var temp_color = null;
          //							forecast_dict_test
          if (dict[code]) {
            temp_color = getColorbar(dict[code].HS_VALUE);
          }

          return {
            //							注意此处的填充颜色及宽度的api可参见

            fillColor: temp_color,
            weight: 2,
            opacity: 1,
            color: "white",
            dashArray: "3",
            fillOpacity: 0.7
          };
        },
        //注意此处必须要将OnEachFeature放在里面才可以
        onEachFeature: onEachFeature
      }).bindPopup(function(layer) {
        return layer.feature.properties.description;
      });

      geojson = temp_geojson.addTo(map);
      return geojson;
    },

    addshp: function(shp_path, dict_area, isremoveLay) {
      var shape_layer = null;
      //为当天地图添加图层
      //注意此处then是异步的，所以无法返回shape_layer;
      shp(shp_path)
        .then(function(temp_geojson) {
          geojson = temp_geojson;
          //do something with your geojson
          //当前图层不为空且删除图层的标记符为true都满足时，才清空当前图层
          if ((my_shp_layer != null) & isremoveLay) {
            $.each(my_shp_layer_arr, function(index, value) {
              mymap.removeLayer(value);
            });
            my_shp_layer_arr = [];
            mymap.removeLayer(my_shp_layer);
          }
          var shp_layer = addShape(dict_area, temp_geojson, null, null, mymap);

          //geojson = L.geoJson(temp_geojson, {
          //    style: mystyle,
          //    onEachFeature: onEachFeature
          //}).addTo(mymap);
          my_shp_layer = shp_layer;
          my_shp_layer_arr.push(shp_layer);
        })
        .then(function() {
          return shape_layer;
        });
      return shape_layer;
    },

    highlightFeature: function(e) {
      var layer = e.target;

      layer.setStyle({
        weight: 5,
        color: "#666",
        dashArray: "",
        fillOpacity: 0.7
      });

      if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
      }

      info.update(layer.feature.properties);
    },

    resetHighlight: function(e) {
      geojson.resetStyle(e.target);
      info.update();
    },

    readShape: function(file, func) {
      shp("file").then(function(geojson) {
        //do something with your geojson
        func(geojson);
      });
    },

    mystyle: function(feature) {
      return {
        weight: 2,
        opacity: 1,
        color: "white",
        dashArray: "3",
        fillOpacity: 0.7,
        fillColor: getColor(feature.properties.density)
      };
    }
  }
};
</script>

<style>
#mycontent {
  position: absolute;
  top: 188px;
  bottom: 0px;
  width: 100%;
}
</style>
