import datetime
import json
import unittest

import geo
import truck

class TestTruck(unittest.TestCase):
  def setUp(self):
    with open('test_data_locations.json') as test_data:
      self.location_map = truck.parse_locations(json.load(test_data))

  def test_parse_locations(self):
    self.assertEquals(462, len(self.location_map))
    expected = truck.Location(
      'La Falafel',
      'Falafel Sandwiches: Fries: Soda: Iced Tea & Various Drinks.',
      geo.Geoposition(37.7674566391069, -122.421788343116))
    self.assertEquals(expected, self.location_map['427822'])

  def test_parse_appearances(self):
    with open('test_data_appearances.json') as test_data:
      data = json.load(test_data)
      appearances = truck.parse_appearances(data, 1, self.location_map)
      self.assertEquals(3069, len(appearances))

      expected_description = ('Cold Truck: sandwiches: corndogs: tacos: '
                              'yogurt: snacks: candy: hot and cold drinks')
      expected = truck.Appearance(
        truck.Location('M M Catering', expected_description,
                       geo.Geoposition(37.7988640669494, -122.400263583781)),
        datetime.time(10),
        datetime.time(11))

      self.assertEquals(expected, appearances[0])

#  def test_getClosest(self):
#    with open('test_data.json') as test_data:
#      data = json.load(test_data)
#      parsed = truck.parseAllFromJSON(data)
#      closest = truck.getClosest(parsed, geo.Geoposition(37.7833, -122.4167), 5)
#      self.assertEquals(5, len(closest))
#      self.assertEquals('Mang Hang Catering', closest[0].name)
#      self.assertEquals('Walt\'s Catering', closest[-1].name)
#

if __name__ == '__main__':
  unittest.main()
