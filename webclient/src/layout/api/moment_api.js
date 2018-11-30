export function getDateStr (date) {
  let mydataStr = ''
  // 注意此处可能获取到的是数字，所以不能直接相加，需要转换为str
  var year = date.getFullYear()
  var month = date.getMonth() + 1
  var day = date.getDate()
  if (month < 10) {
    month = '0' + month
  }
  if (day < 10) {
    day = '0' + day
  }
  mydataStr = String(year) + String(month) + String(day)
  return mydataStr
}
export function getYesterday (date) {
  date.setDate(date.getDate() - 1)
  return date
}
