import math

class Geoposition:
  def __init__(self, lat = 0.0, lon = 0.0):
    self.lat = lat
    self.lon = lon

  def __eq__(self, other):
    if (self.lat != other.lat):
      print 'lat ', self.lat, other.lat
    if (self.lon != other.lon):
      print 'lon'
    return self.lat == other.lat and self.lon == other.lon

  def lat_rad(self):
    return math.radians(self.lat)

  def lon_rad(self):
    return math.radians(self.lon)

  def getDistanceTo(self, other):
    EARTH_RADIUS_KM = 6371
    return math.acos(math.sin(self.lat_rad()) * math.sin(other.lat_rad()) +
                     math.cos(self.lat_rad()) * math.cos(other.lat_rad()) *
                     math.cos(other.lon_rad() - self.lon_rad())) * EARTH_RADIUS_KM
