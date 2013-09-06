/**
 * Top-level application.
 */
function FoodTruckApp(map, searchbox, geolocator, console) {
  this._map = map;
  this._searchbox = searchbox;
  this._geolocator = geolocator;
  this._console = console;

  this._currentMarkers = [];
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
  this._currentMarkers.forEach(function(m) {
    m.setMap(null);
  });
  this._currentMarkers.length = 0;
};

FoodTruckApp.prototype._handleCenterChanged = function(isIdle) {
  this._clearMarkers();

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

  this._getClosestRequest = new XMLHttpRequest();
  this._getClosestRequest.open("GET",
      "/get_closest?lat=" + this._map.getCenter().lat() +
      "&lon=" + this._map.getCenter().lng(), true);
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
    var title = item[0];
    var lat = item[1];
    var lon = item[2];
    var description = item[3];
    var schedule = item[4];

    var marker = new google.maps.Marker({
      position: new google.maps.LatLng(lat, lon),
      map: this._map,
      title: title + '\n\n' + description
    });
    marker.setAnimation(google.maps.Animation.DROP);
    this._currentMarkers.push(marker);

    google.maps.event.addListener(
        marker, 'click',
        this._handleMarkerClick.bind(this, marker, title, description,
                                     schedule));
  }.bind(this));
};

FoodTruckApp.prototype._handleMarkerClick = function(marker, title,
						     description, schedule) {
  // The maps API allows raw HTML to be used for the content property, but we
  // don't do that here because it could lead to XSS if the data from the city
  // is not carefully escaped.
  var content = document.createElement('div');
  content.className = 'infobubble-content';
  var heading = document.createElement('h1');
  heading.textContent = title;
  var descriptionElm = document.createElement('p');
  descriptionElm.textContent = description;
  var link = document.createElement('a');
  link.href = schedule;
  link.target = "_blank";
  link.textContent = 'Schedule';
  content.appendChild(heading);
  content.appendChild(descriptionElm);
  content.appendChild(link);

  var infoWindow = new google.maps.InfoWindow({ content: content });
  if (this._activeInfoWindow) {
    this._activeInfoWindow.close();
  }

  infoWindow.open(this._map, marker);
  this._activeInfoWindow = infoWindow;
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
  }.bind(this));
};
