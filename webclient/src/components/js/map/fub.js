// 引入host变量
import { host } from '../../../layout/api/api'

function getAlarmLevel (val) {
  /*
        func:根据传入的值返回预警报等级
        params:
            val:增水或潮位值
        return:
            警报等级（str）
    */
  /*
    自定义的等级共五种
        无警报：    norm
        蓝色：0-2   info  least
        黄色：2-4   2nd   medium
        橙色：4-8   3rd   more
        红色：8-12  4th   most
    */
  var level = 'norm'
  if (val < 2) {
    level = 'least'
  } else if ((val < 4) & (val >= 2)) {
    level = 'medium'
  } else if ((val < 8) & (val > 4)) {
    level = 'more'
  } else if (val > 8) {
    level = 'most'
  }
  return level
}

function getClass (val) {

}

export function loadFub () {
// 获取全部浮标信息
  let stationData = null

  return loadFubData()
}

// 获取浮标相关信息
export const loadFubData = par => {
  // 获取海洋站相关信息
  let fubUrl = `${host}/fub/list/`
  return axios.get(fubUrl)
}

// 创建fub图标
export function CreateFubIcon (
  code,
  name,
  lat,
  lon,
  area,
  maxwave,
  period,
  date,
  direction
) {
  this.code = code
  this.name = name
  this.lat = lat
  this.lon = lon
  this.area = area
  this.maxwave = maxwave
  this.maxwaveCls = getAlarmLevel(thisl.maxwave)
  this.period = period
  this.periodCls = 'norm'
  this.date = date
  this.dateCls = 'norm'
  this.direction = direction
  this.directionCls = 'norm'

  this.toStr = function () {
    var htmlStr = `<div class="myform"><table ><tr><td width="100" rowspan="2">${
      this.name
    }</td><td class="${this.maxwaveCls}" width="100">${
      this.maxwave
    }</td><td class="${this.periodCls}" width="100">${
      this.period
    } </td></tr><tr><td class="${this.dateCls}" width="100">${
      this.date
    }</td><td class="${this.directionCls}">${
      this.direction
    }</td></tr></table></div>`

    return htmlStr
  }
}
