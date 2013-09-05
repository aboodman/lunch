/**
 * Top-level application.
 */
function FoodTruckApp(map, searchbox, geolocator, console) {
  this._map = map;
  this._searchbox = searchbox;
  this._geolocator = geolocator;
  this._console = console;

  this._currentMarker = null;

  google.maps.event.addListener(searchbox, 'places_changed',
                                this._handlePlacesChanged.bind(this));

  this.autoposition();
}

FoodTruckApp.prototype._handlePlacesChanged = function() {
  if (this._currentMarker) {
    this._currentMarker.setMap(null);
  }

  var places = this._searchbox.getPlaces();
  if (!places || !places.length) {
    return;
  }

  var place = places.shift();
  var image = {
    url: place.icon,
    size: new google.maps.Size(71, 71),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(17, 34),
    scaledSize: new google.maps.Size(25, 25)
  };

  this._currentMarker = new google.maps.Marker({
    map: this._map,
    icon: image,
    title: place.name,
    position: place.geometry.location
  });

  if (place.geometry.viewport) {
    this._map.fitBounds(place.geometry.viewport);
  } else {
    this._map.setCenter(place.geometry.location);
  }
};

FoodTruckApp.prototype.autoposition = function() {
  if (!this._geolocator) {
    this._console.log('No geolocator. Perhaps this browser doesn\'t support ' +
                      'Geolocation');
    return;
  }

  this._geolocator.getCurrentPosition(function(position) {
    var pos = new google.maps.LatLng(position.coords.latitude,
                                     position.coords.longitude);

    var infowindow = new google.maps.InfoWindow({
        map: map,
        position: pos,
        content: 'Location found using HTML5.'
    });

    map.setCenter(pos);
  }.bind(this), function() {
    this._console.log('User denied access to geolocation.');
  }.bind(this));
};
