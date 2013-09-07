/**
 * Top-level application.
 */
function FoodTruckApp(map, searchbox, geolocator, console, params) {
  this._map = map;
  this._searchbox = searchbox;
  this._geolocator = geolocator;
  this._console = console;
  this._params = params;

  this._currentMarkers = {};
  this._activeInfoWindow = null;
  this._getClosestRequest = null;
  this._moveIdleTimer = -1;

  google.maps.event.addListener(searchbox, 'places_changed',
                                this._handlePlacesChanged.bind(this));
  google.maps.event.addListener(map, 'center_changed',
                                this._handleCenterChanged.bind(this));

  this.autoposition();
}

FoodTruckApp.prototype._handlePlacesChanged = function() {
  this._clearMarkers();

  var places = this._searchbox.getPlaces();
  if (!places || !places.length) {
    return;
  }

  var place = places.shift();
  if (place.geometry.viewport) {
    this._map.fitBounds(place.geometry.viewport);
  } else {
    this._map.setCenter(place.geometry.location);
  }
};

FoodTruckApp.prototype._clearMarkers = function() {
  for (name in this._currentMarkers) {
    this._currentMarkers[name].setMap(null);
  }
  this._currentMarkers = {};
};

FoodTruckApp.prototype._handleCenterChanged = function(isIdle) {
  if (!isIdle) {
    if (this._moveIdleTimer) {
      window.clearTimeout(this._moveIdleTimer);
    }

    this._moveIdleTimer = window.setTimeout(
        this._handleCenterChanged.bind(this, true), 1000);
    return;
  }

  this._moveIdleTimer = null;

  if (this._getClosestRequest != null) {
    this._getClosestRequest.abort();
  }

  var url = "/get_closest?lat=" + this._map.getCenter().lat() +
      "&lon=" + this._map.getCenter().lng();
  if (this._params['now']) {
    url += "&now=" + this._params['now'];
  }

  this._getClosestRequest = new XMLHttpRequest();
  this._getClosestRequest.open("GET", url, true);
  this._getClosestRequest.onload = this._handleGetClosestRequest.bind(this);
  this._getClosestRequest.send(null);
};

FoodTruckApp.prototype._handleGetClosestRequest = function() {
  if (this._getClosestRequest.status != 200) {
    return;
  }

  var data = JSON.parse(this._getClosestRequest.responseText);
  this._getClosestRequest = null;
  data.forEach(function(item) {
    if (this._currentMarkers[item.location.name])
      return;

    var marker = new google.maps.Marker({
      position: new google.maps.LatLng(item.location.geopos.lat,
                                       item.location.geopos.lon),
      map: this._map,
      title: item.location.name + '\n\n' + item.location.description
    });

    marker.setAnimation(google.maps.Animation.DROP);
    this._currentMarkers[item.location.name] = marker;

    google.maps.event.addListener(
        marker, 'click',
        this._handleMarkerClick.bind(this, marker, item));
  }.bind(this));
};

FoodTruckApp.prototype._handleMarkerClick = function(marker, item) {
  // The maps API allows raw HTML to be used for the content property, but we
  // don't do that here because it could lead to XSS if the data from the city
  // is not carefully escaped.
  var content = document.createElement('div');
  content.className = 'infobubble-content';
  var heading = document.createElement('h1');
  heading.textContent = item.location.name;
  var descriptionElm = document.createElement('p');
  descriptionElm.textContent = item.location.description;
  var hours = document.createElement('b');
  hours.textContent = this._formatTime(item.start_time) + ' - ' +
    this._formatTime(item.end_time);
  content.appendChild(heading);
  content.appendChild(descriptionElm);
  content.appendChild(hours);

  var infoWindow = new google.maps.InfoWindow({ content: content });
  if (this._activeInfoWindow) {
    this._activeInfoWindow.close();
  }

  infoWindow.open(this._map, marker);
  this._activeInfoWindow = infoWindow;
};

FoodTruckApp.prototype._formatTime = function(time_tuple) {
  var hours = time_tuple[0];
  var minutes = time_tuple[1];

  var am = true;
  if (hours > 12) {
    am = false;
    hours -= 12;
  }

  if (hours == 0)
    hours = 12;

  minutes = String(minutes);
  minutes = "00".substr(0, 2 - minutes.length) + minutes;

  var period = am ? "AM" : "PM";

  return hours + ":" + minutes + " " + period;
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
    this._map.setCenter(pos);
  }.bind(this), function() {
    this._console.log('User denied access to geolocation.');
    this._handleCenterChanged(true);
  }.bind(this));
};
