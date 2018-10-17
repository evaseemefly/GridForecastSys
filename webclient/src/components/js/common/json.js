export function json2dict (data) {
    // 将返回的json，根据code转成dict
  var dict4json = {}
  $.each(data, function (index, value) {
    var obj = $.parseJSON(value)
    dict4json[obj.CODE] = obj
  })
  return dict4json
}
