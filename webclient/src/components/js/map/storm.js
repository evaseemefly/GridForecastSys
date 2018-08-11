import axios from 'axios'
// import cookie from '../common/js/cookie';
import {
  loadStormData,
  loadStationData
} from '../../../layout/api/api'

import {
  getDateStr
} from '../../../layout/api/moment_api'
let host = 'http://127.0.0.1:8000'
axios.defaults.withCredentials = true

export function StormData (
  code,
  name,
  lat,
  lon,
  area,
  surgeVal,
  surgeDt,
  tideVal,
  tideDt,
  nowdate
) {
  this.code = code
  this.name = name
  this.lat = lat
  this.lon = lon
  this.area = area
  this.surge_val = surgeVal
  this.surge_dt = surgeDt
  this.tide_val = tideVal
  this.tide_dt = tideDt
}

export function loadStormLayer (targetDate) {
  // 加载海洋站格点
  /*
     ** 经测试此种方式可行：
          需要加入的流程还有：每次点击此方法时，需要清空layer，并清空加载grid的layer

    */
  // S1 删除现有图层
  clearLayer()

  // 1 先加载station list
  stationArr = loadStationData()
  $.each(stationArr, function (index, val) {
    // console.log(val);
    station_dict[val.code] = val
  })

  // 2 获取返回的当日极值数据
  let dateStr = getDateStr(targetDate)
  storm_arr = loadStormData(date_str)

  // 3 生成storm对象
  $.each(storm_arr, function (index, val) {
    var station_temp = null
    if (val.CODE in station_dict) {
      station_temp = station_dict[val.CODE]
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
      )
      storm_obj_arr.push(obj)
    }
  })
  // add2Marker();
  $.each(storm_obj_arr, function (index, val) {
    addDiv2Marker(val)
  })
  // alert("我是外部方法test2");
}

export function getStormData (params) {
  // 获取指定日期的风暴潮及增水的极值

  // let host = 'http://127.0.0.1:8000'
  // var storm_data = [];
  // var storm_url = `${host}/storm/daily/`
  // //获取当日的风暴潮预报值
  // $.ajax({
  //     url: storm_url,
  //     type: "GET",
  //     dataType: "json",
  //     data: params,
  //     async: false,
  //     success: function (data) {
  //         // console.log(data);
  //         storm_data = data;
  //     }
  // });

  // 改造成如下方式
  // 从后台获取风暴潮及增水的每日极值
  let stormData = loadStormData(params)
  return stormData
  // stormData.then(res => {
  //   console.log(res)
  // })
}

export function loadStation () {
  // 获取全部海洋站信息
  let stationData = null

  return loadStationData()
  //   loadStationData().then(res => {
  //     stationData = res
  //   })
  //   return stationData
}

function getAlarmLevel (val) {
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
}

export function CreateStationIcon (name, surge, surgeDt, tide, tideDt) {
  /*
        name:海洋站名称
        surge:增水
        surge_dt:最大增水出现时间
        tide:最高潮位
        tide_dt：最高潮位出现时间
    */
  this.name = name
  this.surge = surge
  this.surge_dt = surgeDt
  this.surge_cls = ''
  this.tide = tide
  this.tide_dt = tideDt
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
    var htmlStr = `<div class="myform"><table ><tr><td width="100" rowspan="2">${this.name}</td><td class="${this.surge_cls}" width="100">${this.surge}</td><td class="${this.surge_cls}" width="100">${this.surge_dt} </td></tr><tr><td class="${this.tide_cls}" width="100">${this.tide}</td><td class="${this.tide_cls}">${this.tide_dt}</td></tr></table></div>`
    // var htmlStr = '<div class="myform"><table ><tr><td width="100" rowspan="2">{0}</td><td class="{1}" width="100">{2}</td><td class="{3}" width="100">{4} </td></tr><tr><td class="{5}" width="100">{6}</td><td class="{7}">{8}</td></tr></table></div>'.format(
    //       this.name,
    //       this.surge_cls,
    //       this.surge,
    //       this.surge_cls,
    //       this.surge_dt,
    //       this.tide_cls,
    //       this.tide,
    //       this.tide_cls,
    //       this.tide_dt
    //   )
    return htmlStr
  }
}

function addDiv2Marker (stormObj) {
  L.marker([storm_obj.lat, storm_obj.lon])
    .addTo(mymap)
    .bindPopup('')

  var obj1 = new CreateStationIcon(
    stormObj.name,
    stormObj.surge_val,
    stormObj.surge_dt,
    stormObj.tide_val,
    stormObj.tide_dt
  )

  var busIcon1 = L.divIcon({
    className: 'icon_default',
    html: obj1.toStr(),
    // 坐标，[相对于原点的水平位置（左加右减），相对原点的垂直位置（上加下减）]
    iconAnchor: [-20, 30]
  })

  // 秀英
  L.marker([stormObj.lat, stormObj.lon], {
    icon: busIcon1
  }).addTo(mymap)
}

// export function loadStormData(get_data) {
//     var storm_data = [];
//     var storm_url = "/storm/daily/";
//     //获取当日的风暴潮预报值
//     $.ajax({
//         url: storm_url,
//         type: "GET",
//         dataType: "json",
//         data: {
//             targetdate: get_data
//         },
//         async: false,
//         success: function (data) {
//             // console.log(data);
//             storm_data = data;
//         }
//     });
//     return storm_data;
// }

// export function loadStormData(params) {
//     return axios.get(`${host}/storm/daily/`, {
//         targetdate: params
//     })
// }

// return loadStormData(data);
// return axios.get(`${host}/storm/daily/`, {
//     params: data
// });
// }

// export const getstorm = data => {
//     return axios.get(`${host}/storm/daily/`, { params: data });
//   }

// export {
//     StormData,
//     loadStormLayer,
//     createStationIcon,
//     getStormData,
//     loadStationData,
//     getAlarmLevel,
//     addDiv2Marker,
//     loadStormData
// }
