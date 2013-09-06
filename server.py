from datetime import datetime
import json
import os
import SimpleHTTPServer
import SocketServer
import urllib2
import urlparse

import geo
import truck


_trucks = []
_last_update = datetime.fromtimestamp(0)
_CACHE_DAYS = 1
_MAX_RETURN_QUANTITY = 10
_FOOD_TRUCK_FEED = ('https://data.sfgov.org/api/views/rqzj-sfat/rows.json?'
                    'accessType=DOWNLOAD')


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
    response = json.dumps(truck.serializeAllToJSON(
        truck.getClosest(_trucks, geo.Geoposition(lat, lon),
                         _MAX_RETURN_QUANTITY)))
    self.wfile.write(response)

  def _update_cache(self):
    global _last_update
    global _trucks
    now = datetime.now()
    if ((now - _last_update).days < _CACHE_DAYS):
      return
    response = urllib2.urlopen(_FOOD_TRUCK_FEED).read()
    _trucks = truck.parseAllFromJSON(json.loads(response))
    _last_update = now


if __name__ == '__main__':
  os.chdir('client')
  try:
    SocketServer.TCPServer(("", 8088), FoodTruckHandler).serve_forever()
  finally:
    os.chdir('../')
