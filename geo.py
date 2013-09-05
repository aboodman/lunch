import math

class Geoposition:
  lat = 0
  lon = 0

  def __init__(self, lat = 0, lon = 0):
    self.lat = lat
    self.lon = lon

  def lat_rad(self):
    return math.radians(self.lat)

  def lon_rad(self):
    return math.radians(self.lon)

  def getDistanceTo(self, other):
    EARTH_RADIUS_KM = 6371
    return math.acos(math.sin(self.lat_rad()) * math.sin(other.lat_rad()) +
                     math.cos(self.lat_rad()) * math.cos(other.lat_rad()) *
                     math.cos(other.lon_rad() - self.lon_rad())) * EARTH_RADIUS_KM
