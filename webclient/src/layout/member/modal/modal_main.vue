<template>
  <div
    id="mymodal"
    class="modal fade"
    tabindex="-1"
    role="dialog"
  >
    <div
      id="modal_content"
      class="modal-dialog"
      role="document"
    >
      <div class="modal-content">
        <div class="modal-header">
          <button
            type="button"
            class="close"
            data-dismiss="modal"
            aria-label="Close"
          ><span aria-hidden="true">&times;</span></button>
          <h4 class="modal-title">浮标编号{{bbxCode}}</h4>
        </div>
        <div class="modal-body my-content-primary">
          <div>
            <fubDetailTable
              :fid="fid"
              :code="fubCode"
            ></fubDetailTable>
            <ul
              id="mytabs"
              class="nav nav-tabs"
            >
              <li
                v-for="(item,index) in menulist"
                role="presentation"
                :class="{actiove:index===indexMenu}"
              >
                <a
                  href="#"
                  @click="active(index)"
                >{{item.name}}</a>
              </li>
            </ul>
            <!-- <div
              id="main"
              style=""
            ></div> -->
            <fubObservation
              :columns="childColumns"
              :values="childVals"
              :title="childTitle"
              :factor="childFactor"
              ref="fubObs"
            ></fubObservation>
          </div>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-default"
            data-dismiss="modal"
          >关闭</button>
          <button
            type="button"
            class="btn btn-primary"
          >确定</button>
        </div>
      </div>
      <!-- /.modal-content -->
    </div>
    <!-- /.modal-dialog -->
  </div>
</template>

<script>
import fubObservation from '../charts/fub_observation_charts.vue'
import fubDetailTable from '../table/fub_detail_table.vue'
import { loadFubRealtime } from '../../api/api.js'
import { strategyAppendRealtimeData } from '../../../module/search/ws_strategies.js'
import { menulist } from '../../../module/search/menu_list.js'
// 重构后的modal框
export default {
  data () {
    return {
      menulist: menulist,
      indexMenu: 0,
      facotr: null,
      fubCode: null,
      fid: -1,
      targetDate: null,
      kind: null,
      childVals: [],
      childColumns: []
    }
  },
  methods: {
    // 由fub_Base调用的显示modal的方法
    /*
      加载modal窗
      并获取fub的基础信息并加载
    */
    showModal: function (code) {
      this.fubCode = code
      $('#mymodal').modal()
      // 每次加载modal框时需要销毁echarts子组件
      this.$refs.fubObs.destroyCharts()
    },
    // 点击 tab 时触发的操作
    active: function (index) {
      this.indexMenu = index
    },
    // 加载指定fub的观测数据
    loadDetailData: function (code, fid, factor, date, kind) {
      var myself = this
      let params = {
        code: code,
        targetdate: date,
        factor: factor,
        fid: fid,
        kind: kind
      }
      this.childVals = []
      this.childColumns = []
      this.childFactor = factor
      loadFubRealtime(params).then(res => {

        // 暂时注释掉真正读取的操作
        // 父组件将由后台返回的vals与columns赋值为要传递给子组件的data中

        // 使用方式1，会导致子组件中的columns与values更新在initCharts之后
        var factor = (myself.factor == 'ws' || myself.factor == 'wd') ? 'w' : 'default'
        var obj = strategyAppendRealtimeData(factor, res.data)
        myself.childVals = obj['values']
        myself.childColumns = obj['columns']

      })
    }
  },
  watch: {
    indexMenu: function (newVal, oldVal) {
      // 获取当前选中的菜单中对应的code
      var factor = this.menulist[newVal].code
      // 修改当前的factor
      this.factor = factor
      // 修改子组件的title
      this.childTitle = this.menulist[newVal].name
      // console.log(nowCode);
      var code = this.fubCode
      var fid = this.fid
      var targetdate = this.targetDate
      var kind = this.kind

      this.childFactor = factor
      // 
      this.loadDetailData(code, fid, factor, targetdate, kind)

    }
  },
  components: {
    fubObservation,
    fubDetailTable
  }
}
</script>

<style scoped>
#modal_content {
  width: 850px;
}
.my-content-primary {
  background: #143b4d;
}
.my-th-normal {
  color: #4154de;
}
.my-th-warm {
  color: rgba(255, 0, 0, 0.838);
}
/* 带一个阴影 */
.boxshadow {
  box-shadow: 2px 2px 10px grey;
}
/* 顶部字体加粗加大 */
.panel-heading {
  font-weight: bolder;
  font-size: large;
}
</style>
