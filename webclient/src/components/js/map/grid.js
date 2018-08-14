import {
    getDateStr, getYesterday
  } from '../../../layout/api/moment_api'

import {
    loadTargetAreaMaxData
  } from '../../../layout/api/api'

import {
    json2dict
  } from '../../js/common/json'
function random_forecast (key, count, max) {
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
}

/*
			 * 根据设定好的色带根据传入的值返回对应的rgb颜色的值
			 */
function getColorbar (value) {
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
}

/*
			 * 叠加shp文件，以geoJson的方式读取
			 * data是读取的geoJson数据
			 * 此处已重新修改 2018-08-06
			 */
export function addShape (dict, data, feature, layer, map) {
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
        temp_color = getColorbar(dict[code].HS_VALUE)
      }

      return {
                //							注意此处的填充颜色及宽度的api可参见

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
}
export function compareForecast (prop) {
  return function (a, b) {
    var valueA = a[prop]
    var valueB = b[prop]
    return valueB - valueA
  }
}
// 将字典转为arr
export function dic2arr (dict) {
  var arr = []
  for (temp in dict) {
    arr.push({
      code: temp,
      value: dict[temp]
    })
  }
  return arr
}

export function loadAreaMaxDataByDate (date, area) {
    // 从后台获取指定时间，指定海区的极值数据，并以dict的方式返回
  var dataCheckarea = []
  var index = 0
  var targetDate = date
  while (dataCheckarea.length < 1 && index < 6) {
    index += 1
    let dateStr = getDateStr(targetDate)
        // alert(date_str);
    dataCheckarea = loadTargetAreaMaxData(dateStr, area)

        // 讲当前日期往前推一天
    date = getYesterday(targetDate)
    if (dataCheckarea != 0) {
      break
    }
  }

    // var data_checkarea= load_targetAreaMaxData(date_str,area);
  let dictArea = json2dict(dataCheckarea)
  return dictArea
}

export function addshp (shp_path, dict_area, isremoveLay) {
  var shape_layer = null
    // 为当天地图添加图层
    // 注意此处then是异步的，所以无法返回shape_layer;
  shp(shp_path).then(function (temp_geojson) {
    geojson = temp_geojson
        // do something with your geojson
        // 当前图层不为空且删除图层的标记符为true都满足时，才清空当前图层
    if (my_shp_layer != null & isremoveLay) {
      $.each(my_shp_layer_arr, function (index, value) {
        mymap.removeLayer(value)
      })
      my_shp_layer_arr = []
      mymap.removeLayer(my_shp_layer)
    }
    var shp_layer = addShape(dict_area, temp_geojson, null, null, mymap)

        // geojson = L.geoJson(temp_geojson, {
        //    style: mystyle,
        //    onEachFeature: onEachFeature
        // }).addTo(mymap);
    my_shp_layer = shp_layer
    my_shp_layer_arr.push(shp_layer)
  }).then(function () {
    return shape_layer
  })
  return shape_layer
}

function highlightFeature (e) {
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
}

function resetHighlight (e) {
  geojson.resetStyle(e.target)
  info.update()
}

function readShape (file, func) {
  shp('file').then(function (geojson) {
        // do something with your geojson
    func(geojson)
  })
}

function mystyle (feature) {
  return {
    weight: 2,
    opacity: 1,
    color: 'white',
    dashArray: '3',
    fillOpacity: 0.7,
    fillColor: getColor(feature.properties.density)
  }
}
