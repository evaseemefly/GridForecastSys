<template>
  <div>
    <!-- <p>{{mytest}}</p> -->
    <div id="main_chart"></div>
  </div>
</template>

<script>

import $ from 'jquery'

// const $ = require('jquery')
// window.$ = $
// require('jquery-confirm')

// import { loadRealtime } from '../../../api/api.js'
import { loadRealtime } from '../../api/api.js'
// var echarts = require('echarts')
export default {
  data () {
    return {
      mychart: null
    }
  },
  props: {
    // title
    title: String,
    // 列数据
    columns: Array,
    // values
    values: Array,
    factor: String
  },
  methods: {
    // 销毁echarts
    disposeCharts: function () {
      if (this.mychart != null) {
        this.mychart.dispose()
      }
    },
    // 初始化echarts表格    
    initCharts: function (params) {
      // 基于准备好的dom，初始化echarts图表
      var myself = this
      myself.mychart = null
      this.disposeCharts()
      if (myself.myChart === null) {

      }
      myself.myChart = echarts.init(document.getElementById('main_chart'))

      var option = {
        tooltip: {
          show: true
        },
        legend: {
          data: [myself.title]
        },
        xAxis: [{
          type: 'category',
          data: myself.columns,
          //使用以下方式实现显示全部x坐标上的点
          "axisLabel": {
            //interval: 0,
            textStyle: {
              color: '#FFFFFF'
            }
          },

          //                  interval:0   
        }],
        yAxis: [{
          // min: function () {
          //   let min = Math.min(myself.values)
          //   return min;
          // },
          type: 'value',
          "axisLabel": {
            //					interval: 0,
            textStyle: {
              color: '#FFFFFF'
            },
            // formatter: function (value, index) {
            //   return value.toFixed(2);
            // }
          },
        }],
        series: [{
          "name": myself.title, //需要与legend中的data相同
          "type": "line",
          smooth: true, //不是折线，是曲线
          itemStyle: {
            normal: {
              //设置折点的颜色
              color: 'rgb(189, 196, 56)',
              //注意lineStyle需要卸载normal里面
              //自定义折线颜色
              lineStyle: {
                color: '#00FF00'
              },
              //自定义折线下区域的颜色
              areaStyle: {
                color: 'rgb(56, 196, 147)'
              },

              label: {
                show: true //显示每个点的值
              }
            }

          }, //向下填充区域
          "data": myself.values,
          label: {
            normal: {
              show: true
            }
          }
        },]
      };

      // 加入是否为wd或ws的判断
      if (myself.factor === 'ws' || myself.factor === 'wd') {
        // option.series['symbol'] = 'triangle';
        option.series[0]['symbolSize'] = [40, 20];
        // option.series['symbol'] = 'image:../../../../../assets/common/arrows.png'
        // 注意由于此处已经嵌套了一级的路由，所以使用绝对路径，需要先返回上一级才是实际的public根目录
        option.series[0]['symbol'] = 'image://../common/arrows.png'
      } else {
        option.series[0]['symbol'] = 'circle';
        option.series[0]['symbolSize'] = 8;
      }

      // 为echarts对象加载数据 
      myself.myChart.setOption(option);

      this.slideDown();
    },
    //销毁echarts表格
    destroyCharts () {
      this.slideUp();
    },
    // 下拉
    slideDown: function () {
      $('#main_chart').slideDown("slow");
    },
    // 收起
    slideUp: function () {
      $('#main_chart').slideUp("slow");
    }
  },
  mounted: function () {
    this.slideUp();
  },
  watch: {
    values: function (newVal) {
      // console.log(newVal);
      var myself = this;
      if (newVal.length > 0) {
        this.initCharts();
      }
    }
  }
}

</script>

<style scoped>
#main_chart {
  height: 500px;
  width: 800px;
}
</style>
