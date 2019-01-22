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
      this.initData()

      // 基于准备好的dom，初始化echarts图表
      var myChart = echarts.init(document.getElementById('modalframe'))
      // 为echarts对象加载数据
      myChart.setOption(myself.options)
      // 显示modal框
      $('#errorModal').modal()
    },
    initData: function () {
      // 需要的变量：
      /*
        value的题注：colums_title            
      */
      var myself = this
      myself.options = {
        tooltip: {
          show: true
        },
        legend: {
          // 题注样式修改
          // 2018 06 14
          orient: 'horizontal',
          x: 'center',
          y: 'top',
          textStyle: { color: 'white', fontWeigth: 'normal', fontSize: 16 },
          borderWidth: 2,
          data: [myself.title]
        },
        xAxis: [{
          type: 'category',
          data: myself.columns,
          // 使用以下方式实现显示全部x坐标上的点
          'axisLabel': {
            // interval: 0,
            textStyle: {
              color: '#FFFFFF'
            },
            formatter: function (val) {
              return val + '时'
            }
          }
          //                  interval:0
        }],
        yAxis: [{
          type: 'value',
          'axisLabel': {
            // interval: 0,
            textStyle: {
              color: '#FFFFFF'
            }
          }
        }],
        series: [{
          name: myself.title, // 需要与legend中的data相同
          type: 'bar',
          smooth: true, // 不是折线，是曲线
          itemStyle: {
            normal: {
              // 设置折点的颜色
              lineStyle: {
                color: '#00FFFF'
              },
              // 注意lineStyle需要卸载normal里面
              // 自定义折线颜色

              // 自定义折线下区域的颜色
              // areaStyle: {
              //   color: '#00FFFF'
              // }
              color: function (params) {
                // 获取当前的hs的值
                // var hs_value = params.series.data[params.seriesIndex]
                var hsValue = params.data
                var hsColor = myself.getColorbar(hsValue)
                return hsColor
              }
            }

          }, // 向下填充区域
          'data': myself.values,
          markPoint: {
            symbolSize: 4,
            // 使用markPoint显示最大值及最小值
            data: [{
              type: 'max',
              name: '最大值'
            },
            {
              type: 'min',
              name: '最小值'
            }
            ],
            // 注意设置itemStyle：不需要再加[]，相当于itemStyle中的noraml对象中的lable。。。
            itemStyle: {
              normal: {
                label: {
                  show: true,
                  textStyle: {
                    color: '#000080'
                  }
                }
              }

            }
            // effect:show,
          },
          markLine: {
            data: [{
              type: 'max',
              name: '最大值'
            }, // 最大值水平线或垂直线
            // {
            // type: 'min',
            // name: '最小值'
            // }, // 最小值水平线或垂直线
            {
              type: 'average',
              name: '平均值'
            }
            ]
          },
          label: {
            normal: {
              // 每个点的值是否显示
              show: false,
              interval: 'auto'
            }
          }
        }]
      }
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
  height: 500px;
  width: 850px;
}
.modal-title {
  font-size: 29px;
  font-weight: 700;
  color: black;
}
</style>