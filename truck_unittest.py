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

if __name__ == '__main__':
  unittest.main()
