import axios from 'axios'
// import cookie from '../common/js/cookie';

let host = 'http://127.0.0.1:8000'
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

export const loadStationData = par => {
  // 获取海洋站相关信息
  let statinUrl = `${host}/station/list/`
  return axios.get(statinUrl)
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
      async: false,    // 同步请求时页面锁死
      success: function (data) {
        result = data
      }
    })
    return result
  }
}
