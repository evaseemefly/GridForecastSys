/*
			 * 根据code从features_arr中找到指定的Feature，并聚焦到指定区域
			 * 
			 * 
			 */
function search(code) {
  var target_feature = null;
  $.map(features_arr, function(obj, index) {
    if (obj.properties.Code == code) {
      target_feature = obj;
    }
  });
  //将feature转成LatLngBounds

  var corner1 = L.latLng(40.712, -74.227),
    corner2 = L.latLng(40.774, -74.125),
    bounds = L.latLngBounds(corner1, corner2);

  mymap.fitBounds(bounds);
}

/*
			 * 根据指定的code的key找到对应的code，并打点
			 * 
			 */
function showAndPointTargetArea(code) {
  //每次打点之前，需要先判断point_marker是否为空，为空需要先去掉
  if (point_marker != null) {
    mymap.removeLayer(point_marker);
  }

  var target_area = null;
  $.each(features_arr, function(index, val) {
    if (val.properties.Code == code) {
      target_area = val;
    }
    //						index;
  });
  if (target_area != null) {
    var latlon_arr = target_area.geometry.bbox;
    /*
         * 119.12344000000051
            25.263725000000193
            119.5140380859375
            25.621950149536133
         * lon：经度
         * lat：维度
         */
    //计算中位点
    var point_lat = (latlon_arr[1] + latlon_arr[3]) / 2;
    var point_lon = (latlon_arr[0] + latlon_arr[2]) / 2;
    //						point_marker=L.marker([point_lon, point_lat]).addTo(mymap).bindPopup("I am a green leaf.");
    point_marker = L.marker([point_lat, point_lon])
      .addTo(mymap)
      .bindPopup("I am a green leaf.");
    mymap.setView([point_lat, point_lon], 8);
  }
}
