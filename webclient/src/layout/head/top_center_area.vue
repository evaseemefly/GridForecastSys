<template>
  <div class="col-md-12 mycol_disPadding">
    <nav class="navbar navbar-default" style="margin-bottom: 0px;">
      <div class="container-fluid">
        <!-- Brand and toggle get grouped for better mobile display -->
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
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
            <!-- <li v-for="item in items" :class="{item.code==selected.code}?'active':''"> -->
            <li v-for="item in items" :class="item.code==selected.code?'active':''">
              <!-- <router-link :to="{name:childUrl,path:childUrl,params:{code:item.code}}" @click.native='selectlayer'>
                            {{item.message}} -->
              <!-- <router-link :to="{name:childUrl,path:childUrl,params:{code:item.code}}" @click.native='selectlayer'>
                            {{item.message}}
                                <span class="sr-only">(current)</span>
                            </router-link> -->
              <!-- 2018-10-29 可用版本 -->
              <!-- <router-link :to="{name:'content',path:'content',params:{code:item.code,category:selected_category}}"
                            @click.native="selectlayer"> {{item.message}}
                                <span class="sr-only">(current)</span>
                            </router-link> -->

              <router-link :to="{name:selected_category,path:selected_category,params:{code:item.code,category:selected_category}}" @click.native="selectlayer"> {{item.message}}
                <span class="sr-only">(current)</span>
              </router-link>

              <!-- 使用router-link的方式实现 -->
              <!-- <a href="#" v-on:click="selectlayer(item.code,item)">{{item.message}}
                                <span class="sr-only">(current)</span>
                            </a> -->
            </li>
            <!-- <li v-show="selected_show">显示</li> -->
            <li v-show="selected_show" id="selectmarker">
              <select v-show="selected_show" class="selectpicker" data-style="btn-success" title="数值预报产品种类">
                <option value="1">西北太</option>
                <option value="2">测试</option>
              </select>
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
import '../../components/js/select/bootstrap-select.js'
import '../../components/css/select/bootstrap-select.css'
export default {
  data () {
    return {
      items: [
        {
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

      // 注意selected是items中的obj
      selected: null,
      out_shape_layer: null,
      selected_category: 'forecast',
      selected_show: true,
      // route_url: '',
      mylayer: '',
      childUrl: ''
    }
  },
  methods: {
    selectlayer: function (val) {
      // 鼠标点击区域操作，点击区域视角拉近到某个区域
      console.log(val)
    }
  },
  watch: {
    selected: function (newData, oldData) {
      // console.log('修改为：' + new_data);
      var myself = this
      //   this.childUrl = 'content/' + this.selected_category
      // self.fillarea(new_data.code, self.selected);
    },
    // 监听选择种类的变化（近岸技术单元、风暴潮、数值预报产品、浮标）
    selected_category: function (newData, oldData) {
      var myself = this
      this.childUrl = 'content/' + this.selected_category
      // 只有切换为数值预报产品时，才显示下拉框
      if (this.selected_category === 'forecast') {
        this.selected_show = true
      } else {
        this.selected_show = false
      }
    }
  },
  created: function () {
    this.selected = {
      message: '全国',
      code: 'a'
    }
    $('.selectpicker').selectpicker('val', '1')
    $('.selectpicker').selectpicker('val')
    $('.selectpicker').on('changed.bs.select', function (e, index, val) {
      //思路
      /*
						由于获取不到选中的值，只能通过$('.selectpicker').selectpicker('val')取到当前选中的select的val，
						所以每次点击时，获取当前选中的值
						并执行其响应操作

					*/
      // console.log(e);
      // console.log(index);
      var select_val = $('.selectpicker').selectpicker('val')
      console.log(select_val)
    })
  },
  mounted: function () {
    // this.selected = {
    //   message: '全国',
    //   code: 'a'
    // }
    bus.$on('on-area', msg => {
      // 当切换预报种类是，切换区域
      console.log('由区域组件传过来的值为' + msg.code + ':' + msg.message)
      this.selected_category = msg.code

      // 2018-09-10
      // 在此处执行清除当前底图的操作
      // 例如当前为网格，切换为站点，则清除网格的底图
      // 清除底图的操作不写在此处了，写在center_map组件的route中
    })
  }
}
</script>

<style>
#selectmarker {
  margin-top: 5px;
}
</style>
