<template>
  <form class="form-horizontal">
    <div class="col-sm-12">
      <div class="panel panel-default boxshadow">
        <div class="panel-heading">浮标基础信息</div>
        <div class="panel-body table-responsive ">
          <table class=" table table-striped table-hover table-bordered">
            <thead>
              <th>编号</th>
              <th>名称</th>
              <th>所属海区</th>
              <th>状态</th>
            </thead>
            <tbody>
              <tr>
                <td>{{code}}</td>
                <td>{{name}}</td>
                <td class="my-th-normal">{{area}}</td>
                <td class="my-th-warm">{{remark}}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </form>
</template>

<script>
import { loadFubDetail } from '../../api/api.js'
// import { } from '../../../components/js/common/'
// import { areaDict } from '../../../components/js/common/area.js'
export default {
  data () {
    return {
      // fub名称
      name: null,
      // 海区
      area: null,
      // 编号
      code: null,
      // 备注
      remark: null

    }
  },
  props: {
    // 组件传递来的fub基础信息
    detailInfo: Object,
    // fid
    fid: Number,
    code: String
  },
  methods: {
    // 加载详情table信息
    initTable: function (code) {
      var myself = this
      var params = {
        code: code
      }
      // 根据fid加载fub的详情信息
      loadFubDetail(params).then(res => {
        // console.log(res);
        myself.code = res.data[0].code
        myself.name = res.data[0].name
        myself.area = res.data[0].area
        // myself.area = areaDict[res.data.area];
        // myself.ton = res.data[0].shipton
      })
    }
  },
  mounted: function () {
    // 根据bid加载
    // this.initTable();
  },
  watch: {
    // 当bid修改时重新加载表格
    code: function (newVal) {
      // console.log(newVal)
      this.initTable(newVal)
    }
  }

}
</script>

<style scoped>
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
