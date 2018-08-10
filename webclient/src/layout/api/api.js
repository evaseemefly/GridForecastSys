import axios from 'axios'
// import cookie from '../common/js/cookie';

let host = 'http://127.0.0.1:8000'
// 允许跨域访问
axios.defaults.withCredentials = true

axios.defaults.headers = {
  'Access-Control-Allow-Headers': 'Authorization,Origin, X-Requested-With, Content-Type, Accept',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, PUT, PATCH, DELETE'
}
// http request 拦截器
// axios.interceptors.request.use(
//   config => {
//     let token = cookie.getCookie('token')
//     console.log(token)
//     if (token) {  // 判断是否存在token，如果存在的话，则每个http header都加上token
//       config.headers.authorization = `JWT ${token}`
//     }
//     return config
//   },
//   err => {
//     return Promise.reject(err)
//   })

// http response 拦截器
// 暂时去掉登陆拦截器
// axios.interceptors.response.use(
//   response => {
//     return response;
//   },
//   error => {
//     if (error.response) {
//       switch (error.response.status) {
//         case 401:
//           // 返回 401 清除token信息并跳转到登录页面
//           router.replace({
//             path: '/login'
//           });
//       }
//     }
//     return Promise.reject(error.response.data);   // 返回接口返回的错误信息
//   });
//   Vue.prototype.$http = axios;
// axios.defaults.withCredentials = true;

// 登录
// export const login = params => {
//     return axios.post(`${host}/api-token-auth/`, params)
// }

export const loadStormData = params => {
  return axios.get(`${host}/storm/daily/`, {
    targetdate: params
  })
}

export
/**
 *根据查询条件获取指定月份的全部值班信息
 *
 * @param {*} data
 * @returns
 */
const getScheduleList = data => {
  return axios.get(`${host}/duty/schedulelist/`, {
    params: data
  })
}

export const addSchedule = data => {
  return axios.post(`${host}/duty/schedulelist/creat/`, data)
}
