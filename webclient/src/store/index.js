import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    stormMarkerArr: [],
    stormIconDivArr: [],
    mymap: Object,
    latlng: Object
  },
  getters: {
    getlatlng: state => {
      return state.latlng
    }
  },
  // 涉及改变数据的
  mutations: {
    clearDivIcon() {
      $.each(state.stormIconDivArr, function(index, val) {
        state.mymap.removeLayer(val)
      })
      $.each(state.stormMarkerArr, function(index, val) {
        state.mymap.removeLayer(val)
      })
      // 2 清除海洋站信息
      state.stormObjArr = []
    },
    clearLayer() {
      // 1 清除沿海基础网格底图
      $.each(state.my_shp_layer_arr, function(index, value) {
        state.mymap.removeLayer(value)
      })
      state.my_shp_layer_arr = []
      if (state.my_shp_layer != null) {
        state.mymap.removeLayer(state.my_shp_layer)
      }
    }
  },
  // 涉及业务逻辑的，以及异步操作
  actions: {}
})

export default store
