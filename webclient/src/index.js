import Vue from 'vue'
import App from './app.vue'
import VueRouter from 'vue-router'
import Routers from './router/router'

import $ from 'jquery'

// 引入vuex
import Vuex from 'vuex'
import store from './store/index'

// 引入全局 iviews
import iview from 'iview'
import 'iview/dist/styles/iview.css'

import 'bootstrap/dist/css/bootstrap.css'
import './components/css/bootstrapExt/table/bootstrap-table.css'
import './components/css/bootstrapExt/editable/bootstrap-editable.css'
import 'bootstrap/dist/js/bootstrap.js'

import './components/css/datetimepicker/bootstrap-datetimepicker.min.css'
import './components/js/datetimepicker/bootstrap-datetimepicker.js'
import './components/js/datetimepicker/bootstrap-datetimepicker.zh-CN.js'

// import './components/js/map/leaflet'
// import './components/js/map/shp.js'
// import './components/js/map/leaflet.shpfile.js'
// 下面两个暂时去掉
import moment from 'moment'

import './components/js/bootstrapExt/table/bootstrap-table.js'
import './components/js/bootstrapExt/editable/bootstrap-editable.js'

// import './components/js/map/leaflet'
// import './components/js/map/leaflet.shpfile'
// import './components/js/map/shp'

import './components/css/style.css'
import './components/css/map/leaflet.css'
import './components/css/flatui/flat-ui.css'
import './components/css/base/base.css'
import './components/css/base/clearfix.css'
import './components/css/storm/storm.css'

Vue.prototype.moment = moment
Vue.config.devtools = true
Vue.use(VueRouter)
// 引入iview
Vue.use(iview)

// Vue.use(Vuex)
const root = document.createElement('div')
document.body.appendChild(root)

// 路由配置
const RouterConfig = {
  // 使用 HTML5 的 History 路由模式
  mode: 'history',
  routes: Routers
}

const router = new VueRouter(RouterConfig)

new Vue({
  // 使用箭头语法等同于下面的写法
  render: h => h(App),
  router: router,
  store: store
}).$mount(root) // $mount为vue中的手动挂载
