export function getDateStr (date) {
  let mydataStr = ''
  var year = date.getFullYear()
  var month = date.getMonth() + 1
  var day = date.getDate()
  if (month < 10) {
    month = '0' + month
  }
  if (day < 10) {
    day = '0' + day
  }
  mydataStr = year + month + day
  return mydataStr
}
export function getYesterday (date) {
  date.setDate(date.getDate() - 1)
  return date
}
