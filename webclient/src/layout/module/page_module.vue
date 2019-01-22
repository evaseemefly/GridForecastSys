<template>
  <div
    class='modal fade'
    id='errorModal'
    tabindex='-1'
    role='dialog'
    aria-labelledby='myProgressLabel'
  >
    <div
      class='modal-dialog modal-lg'
      role='document'
    >
      <div class='modal-content'>
        <div class='modal-header'>
          <button
            type='button'
            class='close'
            data-dismiss='modal'
            aria-label='Close'
          >
            <span aria-hidden='true'></span>
          </button>
          <h4
            class='modal-title'
            id='mymsgtitle'
          >{{title}}</h4>
        </div>
        <div class='modal-body'>
          <form class='form-horizontal'>
            <!--<div class='container'>-->
            <div class='bg-primary col-md-12'>
              <div id='modalframe'>
                <img src="../../../static/img/pager.png">
              </div>
            </div>
          </form>
        </div>
        <div class='modal-footer'>
          <button
            type='button'
            class='btn btn-success'
            data-dismiss='modal'
          >确定</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
var echarts = require('echarts')
// var echarts = require('echarts/lib/echarts')
export default {
  data () {
    return {
      options: null
    }
  },
  props: {
    title: String,
    // 列标签
    columns: Array,
    // value值
    values: Array
    // options: Object
  },
  methods: {
    // 显示modal框
    showModal: function () {
      // 初始化echarts组件
      var myself = this
      // this.initData()

      // 基于准备好的dom，初始化echarts图表
      // var myChart = echarts.init(document.getElementById('modalframe'))
      // 为echarts对象加载数据
      // myChart.setOption(myself.options)
      // 显示modal框
      $('#errorModal').modal()
    },
    initData: function () {
      // 需要的变量：
      /*
        value的题注：colums_title            
      */
      var myself = this
    },
    getColorbar: function (value) {
      // 根据传入的数值（int类型），判断其所属的区件并获取区件的颜色
      var valueColor = ''
      if (value < 6) {
        valueColor = 'rgb(255,250,240)'
      } else if (value >= 6 && value < 9) {
        valueColor = 'rgb(255,242,0)'
      } else if (value >= 9 && value < 14) {
        valueColor = 'rgb(255,127,19)'
      } else if (value >= 14) {
        valueColor = 'rgb(255,0,0)'
      }
      return valueColor
    }
  },
  mounted: function () {

  }
}
</script>

<style scoped>
#modalframe {
  /* height: 500px; */
  height: 100%;
  /* width: 850px; */
  /* width: 100%; */
  width: 540px;
}
.modal-dialog {
  width: 580px;
}
.modal-title {
  font-size: 29px;
  font-weight: 700;
  color: black;
}
.modal-body {
  height: 700px;
}
</style>