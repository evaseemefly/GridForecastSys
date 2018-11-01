<template>
  <div class='dateDiv'>
    <div class='row'>
      <div class='title'>日期</div>
      <!-- <DatePicker type="datetime" format="yyyy-MM-dd HH:mm" placeholder="选择日期" style="width: 200px"></DatePicker>
    <TimePicker format="MM-dd" placeholder="选择时间" :steps="[6]" style="width: 112px"></TimePicker> -->
      <Cascader :data="data" :element-id='date' v-model="value1" style="width:130px"></Cascader>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      value1: [],
      data: [{
        value: '01',
        label: '01日',
        children: [
          {
            value: '00',
            label: '00时'
          },
          {
            value: '06',
            label: '06时'
          }
        ]
      }]
    }
  }
}
</script>

<style scoped>
.dateDiv {
  position: absolute;
  bottom: 100px;
  left: 50px;
  z-index: 999;
  background: #29242168;
  /* width:  */
  box-shadow: 0 20px 10px -11px #35312e68;
  border-radius: 2.5px;

  display: flex;
  /* 主轴对其方式 */
  justify-content: center;
  /* 交叉轴对其方式 */
  align-items: center;
  height: 50px;
}
#date {
  width: 150px;
}
.row{
  margin-right: 0px;
  margin-left: 0px;
  display: flex;
  /* 主轴对其方式 */
  justify-content: center;
  /* 交叉轴对其方式 */
  align-items: center;
}
.row>div{
  margin-right: 3px;
  margin-left: 3px;
}
.dateDiv>.row>.title {
  color: rgb(175, 184, 191);
  font-size: 2em;
  font-weight: bold;
  text-shadow: 2px 2px 10px #000;
  border-radius: 2px;
}
</style>
