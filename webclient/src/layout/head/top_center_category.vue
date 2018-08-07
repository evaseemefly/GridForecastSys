<template>
    <div id="content" class="col-md-12 mycol_disPadding">
        <!--中间的导航栏-->
        <div class="col-md-12 mycol_disPadding">
            <nav class="navbar navbar-default" style="margin-bottom: 0px;">
                <div class="container-fluid">
                    <!-- Brand and toggle get grouped for better mobile display -->
                    <div class="navbar-header">
                        <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1"
                            aria-expanded="false">
                            <span class="sr-only">Toggle navigation</span>
                            <span class="icon-bar"></span>
                            <span class="icon-bar"></span>
                            <span class="icon-bar"></span>
                        </button>
                        <a class="navbar-brand" href="#">位置</a>
                    </div>
                    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                        <!-- 顶部切换不同图层 -->
                        <ul id="top_select_ul" class="nav navbar-nav">
                            <li v-for="item in items" class="{'active':item.code==selected.code}">
                                <a href="#" v-on:click="selectlayer(item.code,item)">{{item.message}}
                                    <span class="sr-only">(current)</span>
                                </a>
                            </li>
                        </ul>
                        <ul class="nav navbar-nav navbar-right">
                            <li>
                                <a href="#">
                                    <span class="glyphicon glyphicon-zoom-in"></span>放大</a>
                            </li>
                            <li>
                                <a href="#">
                                    <span class="glyphicon glyphicon-zoom-out"></span>缩小</a>
                            </li>
                        </ul>
                    </div>
                    <!-- /.navbar-collapse -->
                </div>
                <!-- /.container-fluid -->
            </nav>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                items: [{
                        message: '沿海网格',
                        code: 'grid'
                    },
                    {
                        message: '风暴潮及增水',
                        code: 'storm'
                    }
                ],
                mylayer: "",
            }
        },
        watch: {
            mylayer: function (new_data, old_data) {
                var self = this;
                // self.fillarea(null,new_data);
                if (new_data === "grid") {
                    loadGridLayer();
                } else if (new_data === "storm") {
                    var date = new Date();
                    loadStormLayer(date);
                }
            }
        },
        methods: {
            //选择图层
            selectlayer: function (value, item) {
                // self.selected=
                this.mylayer = value;
                console.log(value, item);
            }
        },
        mounted:function(){
            this.mylayer='grid';
        }
    }
</script>

<style>
    .mycol_disPadding {
        /* 由于与col-md-12冲突，设置优先级 */
        padding: 0px !important;
        padding-left: 0px !important;
        padding-right: 0px !important;

    }
</style>