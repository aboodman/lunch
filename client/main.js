window.addEventListener('load', function() {
  // Enables a newer UI look in Google Maps.
  google.maps.visualRefresh = true;

  var sfCoords = new google.maps.LatLng(37.7833, -122.4167);
  var mapOptions = {
    center: sfCoords,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    panControl: false,
    zoom: 14
  };
  var map = new google.maps.Map(document.querySelector('#map-canvas'),
                                mapOptions);

  var input = document.querySelector('#query');
  var searchbox = new google.maps.places.SearchBox(input);
  searchbox.bindTo('bounds', map);
  input.focus();

  var app = new FoodTruckApp(map, searchbox, navigator.geolocation, console);
});
