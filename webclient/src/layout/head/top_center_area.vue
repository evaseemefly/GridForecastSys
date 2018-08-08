<template>
    <!-- <nav class="navbar navbar-default navbar-inverse" style="margin-bottom: 0px;">
        <div class="navbar-header" id="my_navbar">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse">
                <span class="sr-only">Toggle navigation</span>
            </button>
            <a class="navbar-brand" href="#">沿海网格化显示系统</a>
        </div>
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
            <ul id="top_nav_ul" class="nav navbar-nav">
                <li v-for="item in items" :class="{'active':item.code===selected.code}">

                    <a href="#" v-on:click="selectarea(item.code,item)">{{item.message}}
                        <span class="sr-only">(current)</span>
                    </a>
                </li>
            </ul>
            <form class="navbar-form navbar-left">
                <div class="form-group">
                    <input id="search_code" type="text" class="form-control" placeholder="网格编号">
                </div>
                <button onclick="my_onclick()" class="btn btn-default">搜索</button>
            </form>
        </div>
    </nav> -->
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
                            <router-link :to="{name:'content',path:'content',params:{code:item.code}}" >
                            {{item.message}}
                                <span class="sr-only">(current)</span>
                            </router-link>
                            <!-- 使用router-link的方式实现 -->
                            <!-- <a href="#" v-on:click="selectlayer(item.code,item)">{{item.message}}
                                <span class="sr-only">(current)</span>
                            </a> -->
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
</template>

<script>
    import bus from '../../assets/eventBus.js'
    export default {
        data() {
            return {
                items: [{
                        message: '北海',
                        code: 'n'
                    },
                    {
                        message: '东海',
                        code: 'e'
                    },
                    {
                        message: '南海',
                        code: 's'
                    },
                    {
                        message: '全国',
                        code: 'a'
                    }
                ],
                //注意selected是items中的obj
                selected: null,
                out_shape_layer: null,
                selected_category: '',
                mylayer: "",
            }
        },
        methods: {
            selectlayer: function (val) {
                console.log(val);
            }
        },
        watch: {
            selected: function (new_data, old_data) {
                //console.log('修改为：' + new_data);
                var self = this;
                // self.fillarea(new_data.code, self.selected);
            }
        },
        mounted: function () {
            this.selected = {
                message: '全国',
                code: 'a'
            };
            bus.$on('on-area', (msg) => {
                //当切换预报种类是，切换区域
                console.log('有区域组件传过来的值为' + msg.code + ':' + msg.message);
                this.selected_category = msg.code;

            })
        }
    }
</script>

<style>
</style>