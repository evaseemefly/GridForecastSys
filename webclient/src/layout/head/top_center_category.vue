<template>
    <div id="content" class="col-md-12 mycol_disPadding">
        <!--中间的导航栏-->
        <nav class="navbar navbar-default navbar-inverse" style="margin-bottom: 0px;">
            <div class="navbar-header" id="my_navbar">
                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse">
                    <span class="sr-only">Toggle navigation</span>
                </button>
                <a class="navbar-brand" href="#">沿海网格化显示系统</a>
            </div>
            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <ul id="top_nav_ul" class="nav navbar-nav">
                    <li v-for="item in items" :class="{'active':item.code===selected.code}">
                        <a href="#" v-on:click="seleccategory(item.code,item)">{{item.message}}
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
        </nav>
    </div>
</template>

<script>
    import bus from '../../assets/eventBus.js'
    export default {
        data() {
            return {
                items: [{
                        message: '近岸技术单元',
                        code: 'grid'
                    },
                    {
                        message: '风暴潮及增水',
                        code: 'storm'
                    }
                ],
                //注意selected是items中的obj
                selected: null,
                out_shape_layer: null,
                mylayer: "",
            }
        },
        watch: {
            mylayer: function (new_data, old_data) {
                var self = this;
                this.selected = this.findTarget(new_data);
            },
            selected: function (new_val, old_val) {
                console.log(new_val);
                bus.$emit('on-area',new_val);
            }
        },
        methods: {
            //选择图层
            selectlayer: function (value, item) {
                // self.selected=
                var self = this;
                this.mylayer = value;
                console.log(value, item);
            },
            seleccategory: function (value, item) {
                // alert(item);
                this.selected = item;
            },
            findTarget: function (value) {
                var myself = this;
                //根据当前的code找到items中的obj
                var target_obj = this.items.find((obj) => (obj.code == value));
                return target_obj;
            }
        },
        mounted: function () {
            this.mylayer = 'grid';
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