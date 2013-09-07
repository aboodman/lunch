from datetime import datetime
from datetime import timedelta
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

_appearances = []
_last_update = datetime.fromtimestamp(0)


def _get_pst_now():
  # Totally awful (and non-DST aware) hack. I think the right solution is to use
  # http://pytz.sourceforge.net/, but ... blech.
  return datetime.utcnow() - timedelta(hours=7)


class FoodTruckHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  def do_GET(self):
    if (self.path.startswith('/get_open')):
      self.handle_get_open()
    else:
      SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

  def handle_get_open(self):
    self._update_cache()
    now = None
    qs = self.path[self.path.find('?') + 1:]
    params = urlparse.parse_qs(qs)
    now = params.get('now')
    if not now is None:
      now = truck.parse_time(now[0])
    else:
      now = _get_pst_now().time()

    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()

    response = json.dumps(
      map(truck.Appearance.to_json,
          truck.get_open_at(_appearances, now)))

    self.wfile.write(response)

  def _update_cache(self):
    global _last_update
    global _appearances
    now = _get_pst_now()
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
