import json
import unittest

import geo
import truck

class TestTruck(unittest.TestCase):

  def test_parseAllFromJSON(self):
    with open('test_data.json') as test_data:
      data = json.load(test_data)
      parsed = truck.parseAllFromJSON(data)

      self.assertEquals(656, len(parsed))

      expected_first = truck.Truck(
          'Cupkates Bakery, LLC',
          geo.Geoposition(37.7901490737255, -122.398658184604))
      expected_last = truck.Truck(
          'Bach Catering',
          geo.Geoposition(37.7287554795043, -122.394408901501))
      self.assertEquals(expected_first, parsed[0])
      self.assertEquals(expected_last, parsed[-1])

  def test_serializeAllToJSON(self):
    trucks = [truck.Truck('Foo', geo.Geoposition(3.14, 88.8)),
              truck.Truck('Bar', geo.Geoposition(88.8, 3.14))]
    json = truck.serializeAllToJSON(trucks)

    self.assertEquals(2, len(json))

    self.assertEquals('Foo', json[0][0])
    self.assertEquals(3.14, json[0][1])
    self.assertEquals(88.8, json[0][2])

    self.assertEquals('Bar', json[1][0])
    self.assertEquals(88.8, json[1][1])
    self.assertEquals(3.14, json[1][2])

  def test_getClosest(self):
    with open('test_data.json') as test_data:
      data = json.load(test_data)
      parsed = truck.parseAllFromJSON(data)
      closest = truck.getClosest(parsed, geo.Geoposition(37.7833, -122.4167), 5)
      self.assertEquals(5, len(closest))
      self.assertEquals('Mang Hang Catering', closest[0].name)
      self.assertEquals('Walt\'s Catering', closest[-1].name)


if __name__ == '__main__':
  unittest.main()
