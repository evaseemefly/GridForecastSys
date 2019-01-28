import axios from 'axios'
// import cookie from '../common/js/cookie';

// let host = 'http://127.0.0.1:8000'
export const host = 'http://127.0.0.1:8000'
// 允许跨域访问
axios.defaults.withCredentials = true

axios.defaults.headers = {
  // 'Access-Control-Allow-Headers': 'Authorization,Origin, X-Requested-With, Content-Type, Accept,access-control-allow-methods,access-control-allow-origin',
  // 'Access-Control-Allow-Headers': 'Content-Type',
  // 'Content-Type': 'application/json;charset=UTF-8',
  // 'Content-Type': 'application/x-www-form-urlencoded',
  // 'Access-Control-Allow-Origin': '*',
  // 'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, PATCH, DELETE'
}

export const loadStormData = par => {
  // 获取指定日期的风暴潮及增水的极值

  // var storm_data = []
  let stormUrl = `${host}/storm/daily/`
  // 获取当日的风暴潮预报值
  // $.ajax({
  //   url: storm_url,
  //   type: "GET",
  //   dataType: "json",
  //   data: params,
  //   async: false,
  //   success: function (data) {
  //     // console.log(data);
  //     storm_data = data;
  //   }
  // });
  // axios.get(`${host}/storm/daily/`, {
  //   targetdate: params
  // })
  // axios.get(`${host}/storm/daily/`, params).then(function (res) {
  //   console.log(res)
  // })

  // 以下此种方式可行
  // axios.get(`${host}/storm/daily/`, {
  //   params: par
  // }).then(function (res) {
  //   console.log(res)
  // })
  // 降axios.get对象返回
  return axios.get(stormUrl, {
    params: par
  })
}

// 获取海洋站相关信息
export const loadStationData = par => {
  // 获取海洋站相关信息
  let statinUrl = `${host}/station/list/`
  return axios.get(statinUrl)
}

// 获取浮标相关信息
export const loadFubData = par => {
  // 获取浮标相关信息
  // let fubUrl = `${host}/fub/list/`
  let fubUrl = `${host}/fub/lastdata/`
  return axios.get(fubUrl)
}

// 获取指定日期的浮标风暴潮及增水的极值
export const loadFubStormData = par => {
  // 获取指定日期的风暴潮及增水的极值

  // var storm_data = []
  // let fubUrl = `${host}/fub/filterlist/`
  let fubUrl = `${host}/fub/lastdata/`
  // 降axios.get对象返回
  return axios.get(fubUrl, {
    params: par
  })
}

// 获取指定日期以及指定浮标的72小时时间序列对应值
export const loadFubDetailStormData = par => {
  // 获取指定日期的风暴潮及增水的极值

  let fubUrl = `${host}/fub/daily/`
  // 降axios.get对象返回
  return axios.get(fubUrl, {
    params: par
  })
}

export const loadTargetAreaMaxData = (date, area) => {
  if (area != null) {
    let targetUrl = `${host}/forecast/daily/${date}/${area}/`
    // 使用上面的方式替代下面的方式
    // var targetUrl = '/'
    // var url_arr = new Array()
    // url_arr.push('forecast')
    // url_arr.push('daily')
    // url_arr.push(date)
    // url_arr.push(area)
    // targetUrl += url_arr.join('/')
    // targetUrl += '/'
    console.log(targetUrl)
    // 根据传入的area请求后返回字典
    let dataCheckarea = null
    let result = null
    // return new Promise(function (resolve, reject) {
    //   axios.get(targetUrl).then((res) => {
    //     result = res
    //     resolve(result)
    //   })
    // })
    // return result

    // 以下内容用上面的代码实现
    $.ajax({
      url: targetUrl,
      async: false, // 同步请求时页面锁死
      success: function (data) {
        result = data
      }
    })
    return result
  }
}

// 根据指定时间，及经纬度，读取该时间的海浪nc文件中的10天的数据
export const loadForecastWavebyNc = (date, lat, lng) => {
  let wavebyNcUrl = `${host}/gis/waveforcedetial/`
  var par = {
    date: date,
    lat: lat,
    lng: lng
  }
  return axios.get(wavebyNcUrl, {
    params: par
  })
}

/*
	根据设定好的色带根据传入的值返回对应的rgb颜色的值
 */
export const getColorbar = value => {
  // 根据传入的数值（int类型），判断其所属的区件并获取区件的颜色
  var valueColor = ''
  if (value >= 2 && value < 4) {
    valueColor = 'rgb(0,0,255)'
  } else if (value >= 4 && value < 8) {
    valueColor = 'rgb(255,242,0)'
  } else if (value >= 8 && value < 12) {
    valueColor = 'rgb(255,127,19)'
  } else if (value >= 12) {
    valueColor = 'rgb(255,0,0)'
  }
  return valueColor
}
