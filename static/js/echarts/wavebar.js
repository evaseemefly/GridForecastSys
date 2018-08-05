/*
			 * 初始化echarts图标
			 */
function loadWaveData() {
  // 基于准备好的dom，初始化echarts图表
  var myChart = echarts.init(document.getElementById("wave_data"));

  var option = {
    tooltip: {
      show: true
    },
    legend: {
      //							data: ['波浪', '周期']
      //去掉周期
      data: ["波浪"]
    },
    xAxis: [
      {
        type: "category",
        data: [
          "2018-2-1 15:00",
          "2018-2-1 16:00",
          "2018-2-1 17:00",
          "2018-2-1 18:00",
          "2018-2-1 19:00",
          "2018-2-1 20:00",
          "2018-2-1 21:00",
          "2018-2-1 22:00",
          "2018-2-1 23:00",
          "2018-2-2 00:00",
          "2018-2-2 01:00",
          "2018-2-2 02:00"
        ],
        //使用以下方式实现显示全部x坐标上的点
        axisLabel: {
          //interval: 0,
          textStyle: {
            color: "#FFFFFF"
          }
        }
        //                  interval:0
      }
    ],
    yAxis: [
      {
        type: "value",
        axisLabel: {
          //					interval: 0,
          textStyle: {
            color: "#FFFFFF"
          }
        }
      }
    ],
    series: [
      {
        name: "波浪", //需要与legend中的data相同
        type: "line",
        smooth: true, //不是折线，是曲线
        itemStyle: {
          normal: {
            //设置折点的颜色
            color: "#FFFF00",
            //注意lineStyle需要卸载normal里面
            //自定义折线颜色
            lineStyle: {
              color: "#00FF00"
            },
            //自定义折线下区域的颜色
            areaStyle: {
              color: "#FFFF00"
            },

            label: {
              show: true //显示每个点的值
            }
          }
        }, //向下填充区域
        data: [
          0.37,
          0.52,
          0.32,
          0.12,
          0.32,
          0.49,
          0.61,
          0.46,
          0.35,
          0.24,
          0.12,
          0.35
        ],
        label: {
          normal: {
            show: true
          }
        }
      }
      //							{
      //								"name": "周期", //需要与legend中的data相同
      //								"type": "line",
      //								smooth: true, //不是折线，是曲线
      //								itemStyle: {
      //									normal: {
      //										areaStyle: {
      //											type: 'default'
      //										},
      //										//                    		label : {show: true}
      //									}
      //								}, //向下填充区域
      //								"data": [3.14, 3.21, 3.28, 3.35, 3.41, 3.47, 3.47, 3.55, 3.64, 3.73, 3.80, 3.86]
      //							},
    ]
  };

  // 为echarts对象加载数据
  myChart.setOption(option);
}
