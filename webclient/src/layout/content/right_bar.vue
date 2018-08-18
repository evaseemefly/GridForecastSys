<template>
  <div id="whole_bar" class="whole_bar_hidden">
        <div id="show_btn" class="show_btn_hidden" @click="test()">
            <span>隐藏</span>
        </div>
        <div id="echarts_bar" ></div>
    </div>
</template>

<script>
var echarts = require('echarts/lib/echarts')
import {
  getColorbar
  } from '../api/api'
export default {
  props: {
    // 父组件传入的是否显示
    isShow: Boolean,
    arrKeysForecastextreme: Array,
    arrValuesForecastextreme: Array
  },
  data () {
    return {
      isShow: null
    }
  },
  methods: {
    initbar: function () {
      var myBar = echarts.init(document.getElementById('echarts_bar'))
      return myBar
    },
    loadbar: function (bar, keysArr, valuesArr) {
      let optionMybar = {
        title: {
          text: '波浪72小时预报',
          subtext: '测试数据',
          textStyle: {
            fontWeight: 'bolder',
            color: '#FFFFFF'
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['波浪']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          boundaryGap: [0, 0.01],
          axisLabel: {
            interval: 0,
            textStyle: {
              color: '#ddd'
            }
          },
          axisLine: {
            show: false,
            lineStyle: {
              color: '#ddd'
            }
          },
          splitLine: {
            show: false // 不显示网格线
          }
        },
        yAxis: {
          type: 'category',
          splitLine: {
            show: false // 不显示网格线
          },
          axisLabel: {
            interval: 0,
            textStyle: {
              color: '#FFFFFF',
              fontWeight: 'bold'
            }
          },
          data: keysArr
        },
        series: [
          {
            name: '波浪',
            type: 'bar',
            data: valuesArr,
            itemStyle: {
          // 通常情况下：
              normal: {
            //	color: '#EEC900'
            // 每个柱子的颜色即为colorList数组里的每一项，如果柱子数目多于colorList的长度，则柱子颜色循环使用该数组
                color: function (params) {
                  var mycolor = getColorbar(params.data)

                  return mycolor
                }
              },
          // 鼠标悬停时：
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
  // 为echarts对象加载数据
      bar.setOption(optionMybar)
    },
    test: function () {
      this.isShow = !this.isShow
        // var bar = document.getElementById('mybar');
        // var bar = document.getElementById('whole_bar');
      var btn = document.getElementById('show_btn')
      var whole = document.getElementById('whole_bar')
        // var icon = document.getElementById('circle-span');
        // more.style.height = display ? "100px" : "0px";
        // more.style.width = display ? "100px" : "0px";
        // bar.className = display ? "mybar_right_in" : "mybar_right_out";
      btn.className = this.isShow ? 'show_btn_show' : 'show_btn_hidden'
      whole.className = this.isShow ? 'whole_bar_show' : 'whole_bar_hidden'
      return false
    },
    load: function (arrKeysForecastextreme, arrValuesForecastextreme) {
      let bar = this.initbar()
      this.arrKeysForecastextreme = arrKeysForecastextreme
      this.arrValuesForecastextreme = arrValuesForecastextreme
      this.loadbar(bar, this.arrKeysForecastextreme, this.arrValuesForecastextreme)
    }
  },
  mounted: function () {
    this.isShow = false
    // if (this.isShow) {
    //   // 加载bar
    //   let bar = this.initbar()
    //   this.loadbar(bar, this.arrKeysForecastextreme, this.arrValuesForecastextreme)
    // }

      // 加载bar
      // 不在mounted中初始化echarts，放在load方法中
    // let bar = this.initbar()
    // this.loadbar(bar, this.arrKeysForecastextreme, this.arrValuesForecastextreme)
  }

}
</script>

<style>
#whole_bar {
  z-index: 999;
  top: 100px;
  /* background: blue; */
  height: 400px;
  width: 400px;
  float: right;
  text-align: right;
  
}

#echarts_bar {
  background: #34495E;
  height: 400px;
  width: 350px;
  float: right;
}
#show_btn span{
  font-size: 18px;
}
#show_btn {
  /* float: right; */
  display: inline-block;
  width: 50px;
  height: 100%;
  /* 文字垂直排列 */
  writing-mode: vertical-rl;
  /* 垂直排列居中 */
  text-align: center;
  color: white;
  /* background: red; */
  font-weight: bolder;
  font-family: 'Microsoft YaHei';
  /* 设置左上及左下边角圆滑处理 */
  border-top-left-radius: 2em;
  border-bottom-left-radius: 2em;
}
.show_btn_hidden {
  background-color: #34495E;
  transition: background-color 1.5s;
}
.show_btn_show {
  background-color: #1ABC9C;
  transition: background-color 1.5s;
}
.whole_bar_hidden {
  position: absolute;
  height: 400px;
  width: 400px;
  animation-name: move-out;
  /*动画名称*/
  animation-duration: 1.5s;
  /* 设定动画完成后的状态 */
  animation-fill-mode: forwards;
}
.whole_bar_show {
  position: absolute;
  height: 400px;
  width: 400px;
  animation-name: move-in;
  /*动画名称*/
  animation-duration: 1.5s;
  /* 设定动画完成后的状态 */
  animation-fill-mode: forwards;
}
/* 移出效果：从左边向外部移出 */

@keyframes move-out {
  0% {
    right: 0px;
  }
  100% {
    right: -350px;
  }
}

/* 渐入效果：从左边外侧移入 */

@keyframes move-in {
  0% {
    right: -350px;
  }
  100% {
    right: 0px;
  }
}
</style>
