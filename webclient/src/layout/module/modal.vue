<template>
    <div class="modal fade" id="errorModal" tabindex="-1" role="dialog" aria-labelledby="myProgressLabel">
        <div class="modal-dialog modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    <h4 class="modal-title" style="font-size:29px;font-weight: 700;color:black" id="mymsgtitle">请稍后</h4>
                </div>
                <div class="modal-body">
                    <form class="form-horizontal">
                        <!--<div class="container">-->
                        <div class="bg-primary col-md-12">
                            <div id="wave_data" style="height:500px;width: 850px;">
                            </div>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-success" data-dismiss="modal">确定</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        props:{

        },
        methods:{
            loadModal:function(code,columns,values){
                var targetUrl="/"
    var url_arr=new Array();
    url_arr.push("forecast");
    url_arr.push("detial");
    url_arr.push(date);
    url_arr.push(code);
    targetUrl+=url_arr.join("/");
    targetUrl+="/";
    var targetUrl_code="/";
    var url_arr_code=new Array();
    url_arr_code.push("grid");
    url_arr_code.push("station");
    url_arr_code.push(code);
    targetUrl_code+=url_arr_code.join("/");
    targetUrl_code+="/";
    //获取该code对应的名字
    $.ajax({
        url: targetUrl_code, //json文件位置
        type: "GET", //请求方式为get
        dataType: "json", //返回数据格式为json
        async:false,
        success: function (res) {
            //2018 06 14
            //修改modal框的题目
            $("#mymsgtitle").text("当前网格："+res[0].name);
        }
    });

    $.ajax({
        url: targetUrl, //json文件位置
        type: "GET", //请求方式为get
        dataType: "json", //返回数据格式为json
        success: function (data) { //请求成功完成后要执行的方法
            //					console.log(data);
            var hs_values = [];
            var hs_date = [];
            $.each(data, function (index, value) {
                //						console.log(index+value);
                hs_values.push(value.hs);
                {#console.log(value.hs);#}
                hs_date.push(value.tdate);
                {#console.log(value.tdate);#}
            });
            var option = {
                tooltip: {
                    show: true
                },
                legend: {
                    //题注样式修改
                    //2018 06 14
                    orient:'horizontal',
                    x:'center',
                    y:'top',
                    textStyle: {color: 'white',fontWeigth:'normal',fontSize:16},
                    borderWidth:2,
                    data: ['波浪']
                },
                xAxis: [{
                    type: 'category',
                    data: hs_date,
                    //使用以下方式实现显示全部x坐标上的点
                    "axisLabel": {
                        //interval: 0,
                        textStyle: {
                            color: '#FFFFFF'
                        },
                        formatter:function(val){
                            return val+"时";
                        }
                    }


                    //                  interval:0
                }],
                yAxis: [{
                    type: 'value',
                    "axisLabel": {
                        //					interval: 0,
                        textStyle: {
                            color: '#FFFFFF'
                        }
                    },
                }],
                series: [{
                    "name": "波浪", //需要与legend中的data相同
                    "type": "bar",
                    smooth: true, //不是折线，是曲线
                    itemStyle: {
                        normal: {
                            //设置折点的颜色
                            lineStyle: {
                                color: '#00FF00'
                            },
                            //注意lineStyle需要卸载normal里面
                            //自定义折线颜色

                            //自定义折线下区域的颜色
                            //areaStyle: {
                            //    color: '#FFFF00'
                            //},
                            color: function(params) {
                                var color_arr = [];
                                //获取当前的hs的值
                                //var hs_value = params.series.data[params.seriesIndex];
                                var hs_value = params.data;
                                var hs_color = getColorbar(hs_value);
                                {#console.log(hs_value);#}
                                return hs_color;
                            },
                            //label: {
                            //    show: true //显示每个点的值
                            //}
                        }

                    }, //向下填充区域
                    "data": hs_values,
                    markPoint: {
                        symbolSize: 4,
                        //使用markPoint显示最大值及最小值
                        data: [{
                            type: 'max',
                            name: '最大值'
                        },
                            {
                                type: 'min',
                                name: '最小值'
                            }
                        ],
                        //注意设置itemStyle：不需要再加[]，相当于itemStyle中的noraml对象中的lable。。。
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
                        //								effect:show,
                    },
                    markLine: {
                        data: [{
                            type: 'max',
                            name: '最大值'
                        }, // 最大值水平线或垂直线
//									{
//										type: 'min',
//										name: '最小值'
//									}, // 最小值水平线或垂直线
                            {
                                type: 'average',
                                name: '平均值'
                            }
                        ]
                    },
                    label: {
                        normal: {
                            show: true
                        }
                    }
                },]
            };
            // 基于准备好的dom，初始化echarts图表
            var myChart = echarts.init(document.getElementById('wave_data'));
            // 为echarts对象加载数据
            myChart.setOption(option);
            //显示modal框
            $("#errorModal").modal();
        }
    });
            }
        }
    }
</script>

<style>
</style>