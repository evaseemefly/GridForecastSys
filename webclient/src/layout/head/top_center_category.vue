<template>

  <div
    id="content"
    class="col-md-12 mycol_disPadding"
  >
    <!--中间的导航栏-->
    <nav
      class="navbar navbar-default navbar-inverse"
      style="margin-bottom: 0px;"
    >
      <div
        class="navbar-header"
        id="my_navbar"
      >
        <button
          type="button"
          class="navbar-toggle collapsed"
          data-toggle="collapse"
        >
          <span class="sr-only">Toggle navigation</span>
        </button>
        <a
          class="navbar-brand"
          href="#"
        >沿海网格化显示系统</a>
      </div>
      <div
        class="collapse navbar-collapse"
        id="bs-example-navbar-collapse-1"
      >
        <ul
          id="top_nav_ul"
          class="nav navbar-nav"
        >
          <li
            v-for="item in items"
            :class="{'active':item.code===selected.code}"
          >
            <a v-on:click="seleccategory(item.code,item)">{{item.message}}
              <span class="sr-only">(current)</span>
            </a>
          </li>
          <!-- <li v-for="item in items" :class="{'active':item.code===selected.code}">
                        {{item.message}}
                            <span class="sr-only">(current)</span>
                        
                    </li> -->
        </ul>
        <form class="navbar-form navbar-left">
          <div class="form-group">
            <input
              id="search_code"
              type="text"
              class="form-control"
              placeholder="网格编号"
            >
          </div>
          <button
            onclick="my_onclick()"
            class="btn btn-default"
          >搜索</button>
        </form>
        <!-- <button
          @click="showModal"
          class="btn btn-default"
        >加载警报单</button> -->
        <button
          @click="showModal"
          type="button"
          class="btn btn-default navbar-btn"
        >加载警报单</button>
      </div>
    </nav>
    <pageModule ref="paper"></pageModule>
  </div>

</template>

<script>
import bus from '../../assets/eventBus.js'
import pageModule from '../module/page_module.vue'
export default {
  data () {
    return {
      items: [
        {
          message: '浮标数据',
          code: 'fub'
        },
        {
          message: '风暴潮及增水',
          code: 'storm'
        },
        {
          message: '数值预报产品',
          code: 'forecast'
        },
        {
          message: '近岸技术单元',
          code: 'grid'
        }


      ],
      // 注意selected是items中的obj
      selected: null,
      out_shape_layer: null,
      mylayer: ''
    }
  },
  components: {
    pageModule
  },
  watch: {
    mylayer: function (newData, oldData) {
      var self = this
      this.selected = this.findTarget(newData)
    },
    selected: function (newVal, oldVal) {
      console.log(newVal)
      bus.$emit('on-area', newVal)
    }
  },
  methods: {
    // 选择图层
    selectlayer: function (value, item) {
      // self.selected=
      var self = this
      this.mylayer = value
      console.log(value, item)
    },
    seleccategory: function (value, item) {
      // alert(item);
      this.selected = item
    },
    findTarget: function (value) {
      //   var myself = this
      // 根据当前的code找到items中的obj
      var targetObj = this.items.find((obj) => (obj.code === value))
      return targetObj
    },
    // 显示预警报单module框
    showModal: function (value) {
      console.log("点击操作")
      this.$refs.paper.showModal()

    }
  },
  mounted: function () {
    this.mylayer = 'grid'
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
