import math
import unittest

from geo import Geoposition

class TestGeoposition(unittest.TestCase):

  def test_getDistanceTo(self):
    sf = Geoposition(37.7833, -122.4167)
    hong_kong = Geoposition(22.2783, 114.1589)
    buenos_aires = Geoposition(-34.6033, -58.3817)
    sydney = Geoposition(-33.8600, 151.2111)

    self.assertEquals(10409, math.trunc(sf.getDistanceTo(buenos_aires)))
    self.assertEquals(10409, math.trunc(buenos_aires.getDistanceTo(sf)))
    self.assertEquals(11099, math.trunc(sf.getDistanceTo(hong_kong)))
    self.assertEquals(11099, math.trunc(hong_kong.getDistanceTo(sf)))
    self.assertEquals(11947, math.trunc(sf.getDistanceTo(sydney)))
    self.assertEquals(11947, math.trunc(sydney.getDistanceTo(sf)))


if __name__ == '__main__':
  unittest.main()
