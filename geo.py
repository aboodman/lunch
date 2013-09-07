import math

class Geoposition:
  def __init__(self, lat = 0.0, lon = 0.0):
    self.lat = lat
    self.lon = lon

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.__dict__ == other.__dict__
    else:
      return False

  def __ne__(self, other):
    return not self.__eq__(other)

  def lat_rad(self):
    return math.radians(self.lat)

  def lon_rad(self):
    return math.radians(self.lon)

  def to_json(self):
    return {
      'lat': self.lat,
      'lon': self.lon
      }

  def distance_to(self, other):
    EARTH_RADIUS_KM = 6371
    return math.acos(math.sin(self.lat_rad()) * math.sin(other.lat_rad()) +
                     math.cos(self.lat_rad()) * math.cos(other.lat_rad()) *
                     math.cos(other.lon_rad() - self.lon_rad())) * EARTH_RADIUS_KM
