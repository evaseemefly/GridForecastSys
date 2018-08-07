<template>
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
    </nav>
</template>

<script>
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
            }
        },
        watch: {
            selected: function (new_data, old_data) {
                //console.log('修改为：' + new_data);
                var self = this;
                // self.fillarea(new_data.code, self.selected);
            }
        },
        mounted:function(){
            this.selected={message:'全国',code:'a'};
        }
    }
</script>

<style>
</style>