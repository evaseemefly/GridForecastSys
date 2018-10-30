
var mymap = L.map('basemap').setView([30.09, 127.75], 5);
// var mymap = L.map('basemap').setView([51.505, -0.09], 13)
        mapLink = '../static/mapfiles/';
        L.tileLayer(
            '../../static/mapfiles/{z}/{x}/{y}.jpg', {
            attribution: '',
            maxZoom: 8,
			minZoom: 2			
            }).addTo(mymap);
  var status = 0;
  
//L.marker([25, 120]).addTo(mymap);
//L.circle([25, 122], {
//				color: 'red',
//				fillColor: '#f03',
//				fillOpacity: 0.5,
//				radius: 500
//			}).addTo(mymap);
//	L.polygon([
//		[25, 122],
//		[26, 122],
//		[28, 130]
//	]).addTo(mymap);
//polygon.bindPopup("I am a polygon.");
	
  var popup = L.popup();

	var rectangleMeasure = {
            startPoint: null,
            endPoint: null,
            rectangle:null,
            tips:null,
            layer: L.layerGroup(),
            color: "#0D82D7",
            addRectangle:function(){
                rectangleMeasure.destory();
                var bounds = [];
                bounds.push(rectangleMeasure.startPoint);
                bounds.push(rectangleMeasure.endPoint);
                rectangleMeasure.rectangle = L.rectangle(bounds, {color: rectangleMeasure.color, weight: 1});
                rectangleMeasure.rectangle.addTo(rectangleMeasure.layer);        
                
                var northWestPoint = rectangleMeasure.rectangle.getBounds().getNorthWest(),
                    southEastPoint = rectangleMeasure.rectangle.getBounds().getSouthEast();                
                rectangleMeasure.layer.addTo(map);
            },               
            mousedown: function(e){
                rectangleMeasure.rectangle = null;
                rectangleMeasure.tips = null;
                map.dragging.disable();
                rectangleMeasure.startPoint = e.latlng;
                map.on('mousemove',rectangleMeasure.mousemove)
            },
            mousemove:function(e){
                rectangleMeasure.endPoint = e.latlng;
                rectangleMeasure.addRectangle();
                map.off('mousedown ', rectangleMeasure.mousedown).on('mouseup', rectangleMeasure.mouseup);
            },
            mouseup: function(e){                        
                map.dragging.enable();
                map.off('mousemove',rectangleMeasure.mousemove).off('mouseup', rectangleMeasure.mouseup).off('mousedown', rectangleMeasure.mousedown);
            },
            destory:function(){
                if(rectangleMeasure.rectangle)
                    rectangleMeasure.layer.removeLayer(rectangleMeasure.rectangle);
                if(rectangleMeasure.tips)
                    rectangleMeasure.layer.removeLayer(rectangleMeasure.tips);
            }
         }

  //鼠标点击弹窗
  function onMapClick(e) {
      popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(mymap);
  }  
  
  var poly_points = [];//区域
  var poly_line=new L.Polyline([]);//折线s
  
  
  
  //画矩形
  function addClickLatlng(e){
      //当前点
      var clickLocation=[e.latlng.lat,e.latlng.lng];
    poly_points.push(clickLocation);
    //显示折线
    poly_line.addLatLng(e.latlng);
    mymap.addLayer(poly_line);
      //var point=new L.Point(e.layerPoint.x,e.layerPoint.y);
  }
  
  //显示矩形
  function showPoly(){
      for (var i = 0, latlngs = [], len = poly_points.length; i < len; i++) {
      latlngs.push(new L.LatLng(poly_points[i][0], poly_points[i][1]));
      }
      var poly = new L.Polygon(latlngs);
      map.addLayer(poly);
      //清空
      poly_points=[];
      poly_line=new L.Polyline([]);
  }

   function onMouseMove(e){
	   var lat = e.latlng.lat.toFixed(4);
	   var lon = e.latlng.lng;
	   while(lon > 180)
	   {
		   lon = lon - 360;
	   }
	   while(lon < -180)
	   {
		   lon = lon + 360;
	   }
	   lon = lon.toFixed(4);
	  document.getElementById("latlon").innerHTML = "当前坐标：" + lat + ", " + lon;
	  
   }
   
   

	
