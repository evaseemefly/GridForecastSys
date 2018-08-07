//加载右侧的柱状图top15
function loadbar(bar, keys_arr, values_arr) {
  option_mybar = {
    title: {
      text: "波浪72小时预报",
      subtext: "测试数据",
      textStyle: {
        fontWeight: "bolder",
        color: "#FFFFFF"
      }
    },
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "shadow"
      }
    },
    legend: {
      data: ["波浪"]
    },
    grid: {
      left: "3%",
      right: "4%",
      bottom: "3%",
      containLabel: true
    },
    xAxis: {
      type: "value",
      boundaryGap: [0, 0.01],
      axisLabel: {
        interval: 0,
        textStyle: {
          color: "#ddd"
        }
      },
      axisLine: {
        show: false,
        lineStyle: {
          color: "#ddd"
        }
      },
      splitLine: {
        show: false //不显示网格线
      }
    },
    yAxis: {
      type: "category",
      splitLine: {
        show: false //不显示网格线
      },
      axisLabel: {
        interval: 0,
        textStyle: {
          color: "#FFFFFF",
          fontWeight: "bold"
        }
      },
      data: keys_arr
    },
    series: [
      {
        name: "波浪",
        type: "bar",
        data: values_arr,
        itemStyle: {
          //通常情况下：
          normal: {
            //									color: '#EEC900'
            //每个柱子的颜色即为colorList数组里的每一项，如果柱子数目多于colorList的长度，则柱子颜色循环使用该数组
            color: function(params) {
              var mycolor = getColorbar(params.data);

              return mycolor;
            }
          },
          //鼠标悬停时：
          emphasis: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: "rgba(0, 0, 0, 0.5)"
          }
        }
      }
    ]
  };
  // 为echarts对象加载数据
  bar.setOption(option_mybar);
}
