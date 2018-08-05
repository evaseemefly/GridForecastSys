function StormData(
  code,
  name,
  lat,
  lon,
  area,
  surge_val,
  surge_dt,
  tide_val,
  tide_dt,
  nowdate
) {
  this.code = code;
  this.name = name;
  this.lat = lat;
  this.lon = lon;
  this.area = area;
  this.surge_val = surge_val;
  this.surge_dt = surge_dt;
  this.tide_val = tide_val;
  this.tide_dt = tide_dt;
}

function loadStormLayer() {
  //加载海洋站格点
  /*
     ** 经测试此种方式可行：
          需要加入的流程还有：每次点击此方法时，需要清空layer，并清空加载grid的layer


    */
  //S1 删除现有图层
  clearLayer();

  //1 先加载station list
  station_arr = loadStationData();
  $.each(station_arr, function(index, val) {
    // console.log(val);
    station_dict[val.code] = val;
  });
  //2 获取返回的当日极值数据
  storm_arr = loadStormData();

  //3 生成storm对象
  $.each(storm_arr, function(index, val) {
    var station_temp = null;
    if (val.CODE in station_dict) {
      station_temp = station_dict[val.CODE];
    }
    if (station_temp != null) {
      var obj = new StormData(
        val.CODE,
        station_temp.name,
        station_temp.Lat,
        station_temp.Lon,
        station_temp.area,
        val.Surge_VALUE,
        val.Surge_DATE,
        val.Tide_VALUE,
        val.Tide_DATE
      );
      storm_obj_arr.push(obj);
    }
  });
  // add2Marker();
  $.each(storm_obj_arr, function(index, val) {
    addDiv2Marker(val);
  });
  alert("我是外部方法test2");
}

function createStationIcon(name, surge, surge_dt, tide, tide_dt) {
  /*
        name:海洋站名称
        surge:增水
        surge_dt:最大增水出现时间
        tide:最高潮位
        tide_dt：最高潮位出现时间
    */
  this.name = name;
  this.surge = surge;
  this.surge_dt = surge_dt;
  this.surge_cls = "";
  this.tide = tide;
  this.tide_dt = tide_dt;
  this.tide_cls = "";
  this.surge_cls = getAlarmLevel(this.surge);
  this.tide_cls = getAlarmLevel(this.tide);
  //需要根据传入的增水以及警戒潮位为添加不同的样式
  //
  /*
    自定义的等级共五种
        无警报：    norm
        蓝色：0-2   1st
        黄色：2-4   2nd
        橙色：4-8   3rd
        红色：8-12  4th
    */
  this.toStr = function() {
    var html_str = '<div class="myform"><table ><tr><td width="100" rowspan="2">{0}</td><td class="{1}" width="100">{2}</td><td class="{3}" width="100">{4} </td></tr><tr><td class="{5}" width="100">{6}</td><td class="{7}">{8}</td></tr></table></div>'.format(
      this.name,
      this.surge_cls,
      this.surge,
      this.surge_cls,
      this.surge_dt,
      this.tide_cls,
      this.tide,
      this.tide_cls,
      this.tide_dt
    );
    return html_str;
  };
}

function getStormData() {
  $.ajax({
    url: "./data/storm_data.json",
    type: "GET",
    dataType: "json",
    success: function(data) {
      console.log(data);
      return data;
    }
  });
}

function loadStationData() {
  //获取全部海洋站信息
  var station_data = null;
  $.ajax({
    url: "./data/station_data.json",
    type: "GET",
    dataType: "json",
    async: false,
    success: function(data) {
      // console.log(data);
      station_data = data;
    }
  });
  return station_data;
}

function getAlarmLevel(val) {
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
  var level = "norm";
  if (val < 2) {
    level = "least";
  } else if ((val < 4) & (val >= 2)) {
    level = "medium";
  } else if ((val < 8) & (val > 4)) {
    level = "more";
  } else if (val > 8) {
    level = "most";
  }
  return level;
}

function addDiv2Marker(storm_obj) {
  L.marker([storm_obj.lat, storm_obj.lon])
    .addTo(mymap)
    .bindPopup("");

  var obj_1 = new createStationIcon(
    storm_obj.name,
    storm_obj.surge_val,
    storm_obj.surge_dt,
    storm_obj.tide_val,
    storm_obj.tide_dt
  );

  var busIcon_1 = L.divIcon({
    className: "icon_default",
    html: obj_1.toStr(),
    //坐标，[相对于原点的水平位置（左加右减），相对原点的垂直位置（上加下减）]
    iconAnchor: [-20, 30]
  });

  //秀英
  L.marker([storm_obj.lat, storm_obj.lon], {
    icon: busIcon_1
  }).addTo(mymap);
}

function loadStormData() {
  var storm_data = [];
  //获取当日的风暴潮预报值
  $.ajax({
    url: "./data/storm_data.json",
    type: "GET",
    dataType: "json",
    async: false,
    success: function(data) {
      // console.log(data);
      storm_data = data;
    }
  });
  return storm_data;
}


