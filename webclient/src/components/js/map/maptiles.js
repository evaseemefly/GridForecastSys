var mymap = L.map('basemap').setView([30.09, 127.75], 5)
      // var mymap = L.map('basemap').setView([51.505, -0.09], 13)
      // mapLink = "../static/mapfiles/";

L.tileLayer('../../static/img/mapfiles/{z}/{x}/{y}.jpg', {
  attribution: '',
  maxZoom: 8,
  minZoom: 2
}).addTo(mymap)
var status = 0
var popup = L.popup()

var rectangleMeasure = {
  startPoint: null,
  endPoint: null,
  rectangle: null,
  tips: null,
  layer: L.layerGroup(),
  color: '#0D82D7',
  addRectangle: function () {
    rectangleMeasure.destory()
    var bounds = []
    bounds.push(rectangleMeasure.startPoint)
    bounds.push(rectangleMeasure.endPoint)
    rectangleMeasure.rectangle = L.rectangle(bounds, {
      color: rectangleMeasure.color,
      weight: 1
    })
    rectangleMeasure.rectangle.addTo(rectangleMeasure.layer)

    var northWestPoint = rectangleMeasure.rectangle
              .getBounds()
              .getNorthWest(),
      southEastPoint = rectangleMeasure.rectangle
              .getBounds()
              .getSouthEast()
    rectangleMeasure.layer.addTo(map)
  },
  mousedown: function (e) {
    rectangleMeasure.rectangle = null
    rectangleMeasure.tips = null
    map.dragging.disable()
    rectangleMeasure.startPoint = e.latlng
    map.on('mousemove', rectangleMeasure.mousemove)
  },
  mousemove: function (e) {
    rectangleMeasure.endPoint = e.latlng
    rectangleMeasure.addRectangle()
    map
            .off('mousedown ', rectangleMeasure.mousedown)
            .on('mouseup', rectangleMeasure.mouseup)
  },
  mouseup: function (e) {
    map.dragging.enable()
    map
            .off('mousemove', rectangleMeasure.mousemove)
            .off('mouseup', rectangleMeasure.mouseup)
            .off('mousedown', rectangleMeasure.mousedown)
  },
  destory: function () {
    if (rectangleMeasure.rectangle) { rectangleMeasure.layer.removeLayer(rectangleMeasure.rectangle) }
    if (rectangleMeasure.tips) { rectangleMeasure.layer.removeLayer(rectangleMeasure.tips) }
  }
}
