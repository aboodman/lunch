/**
 * Top-level application.
 */
function FoodTruckApp(map, geolocator, console) {
  this._map = map;
  this._geolocator = geolocator;
  this._console = console;

  this.autoposition();
}

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
