from datetime import datetime
import json
import os
import SimpleHTTPServer
import SocketServer
import urllib2
import urlparse

import geo
import truck


_LOCATION_FEED = ('https://data.sfgov.org/api/views/rqzj-sfat/rows.json?'
                  'accessType=DOWNLOAD')
_SCHEDULE_FEED = ('https://data.sfgov.org/api/views/jjew-r69b/rows.json?'
                  'accessType=DOWNLOAD')
_MAX_RETURN_QUANTITY = 25

_appearances = []
_last_update = datetime.fromtimestamp(0)


class FoodTruckHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  def do_GET(self):
    if (self.path.startswith('/get_closest?')):
      self.handle_get_closest()
    else:
      SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

  def handle_get_closest(self):
    self._update_cache()
    qs = self.path.split('?', 2)[1]
    params = urlparse.parse_qs(qs)
    lat = float(params['lat'][0])
    lon = float(params['lon'][0])
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()

    response = json.dumps(
      map(truck.Appearance.to_json,
          truck.get_closest(_appearances,
                            geo.Geoposition(lat, lon),
                            datetime.now().time(),
                            _MAX_RETURN_QUANTITY)))

    self.wfile.write(response)

  def _update_cache(self):
    global _last_update
    global _appearances
    now = datetime.now()
    if (now.weekday() == _last_update.weekday()):
      return

    #location_map = truck.parse_locations(
    #  json.loads(urllib2.urlopen(_LOCATION_FEED).read()))

    #_appearances = truck.parse_appearances(
    #  json.loads(urllib2.urlopen(_SCHEDULE_FEED).read()),
    #  now.isoweekday() % 7,
    #  location_map)

    with open('../test_data_locations.json') as test_data:
      location_map = truck.parse_locations(json.load(test_data))

    with open('../test_data_appearances.json') as test_data:
     data = json.load(test_data)
     _appearances = truck.parse_appearances(
        data, now.isoweekday() % 7, location_map)

    _last_update = now


if __name__ == '__main__':
  os.chdir('client')
  try:
    SocketServer.TCPServer(("", 8088), FoodTruckHandler).serve_forever()
  finally:
    os.chdir('../')
