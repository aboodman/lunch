window.addEventListener('load', function() {
  // Enables a newer UI look in Google Maps.
  google.maps.visualRefresh = true;

  var sfCoords = new google.maps.LatLng(37.7833, -122.4167);
  var mapOptions = {
    zoom: 13,
    center: sfCoords,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  var map = new google.maps.Map(document.getElementById('map-canvas'),
                                mapOptions);

  var app = new FoodTruckApp(map, navigator.geolocation);
});
