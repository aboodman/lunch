import datetime
import geo


class Location:
  def __init__(self, name = '', description = '', geopos = None):
    self.name = name
    self.description = description
    self.geopos = geopos

  def __repr__(self):
    return '<Location(%s, %f, %f)>' % (self.name, self.geopos.lat,
                                       self.geopos.lon)

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.__dict__ == other.__dict__
    else:
      return False

  def __ne__(self, other):
    return not self.__eq__(other)

  def to_json(self):
    return {
      'name': self.name,
      'description': self.description,
      'geopos': self.geopos.to_json()
      }


class Appearance:
  def __init__(self, location = None, start_time = '', end_time = ''):
    self.location = location
    self.start_time = start_time
    self.end_time = end_time

  def to_json(self):
    return {
      'location': self.location.to_json(),
      'start_time': [
        self.start_time.hour,
        self.start_time.minute
        ],
      'end_time': [
        self.end_time.hour,
        self.end_time.minute
        ]
      }

  def __repr__(self):
    return ('<Appearance(%s, %s, %s)>' %
            (self.location, self.start_time, self.end_time))

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.__dict__ == other.__dict__
    else:
      return False

  def __ne__(self, other):
    return not self.__eq__(other)


def _get_columns(json):
  # The data from the city comes in JSON, but the columns are separate from the
  # rows. This function collects the indicies for each column so that they don't
  # need to be hard-coded.
  result = {}
  columns = json['meta']['view']['columns']
  for i in xrange(len(columns)):
    result[columns[i]['fieldName']] = i
  return result


def parse_locations(location_json):
  columns = _get_columns(location_json)
  result = {}
  for row in location_json['data']:
    # The data contains lots of permits that are expired, rejected, etc, meaning
    # the trucks won't actually be there :(. Skip those.
    if row[columns['status']] != 'APPROVED':
      continue

    # A small amount of the data don't contain geoposition, skip those.
    latitude = row[columns['latitude']]
    longitude = row[columns['longitude']]
    if (latitude == '' or latitude == None or
        longitude == '' or longitude == None):
      continue

    geopos = geo.Geoposition(float(latitude), float(longitude))
    result[row[columns['objectid']]] = Location(row[columns['applicant']],
                                                row[columns['fooditems']],
                                                geopos)
  return result


def parse_time(time_str):
  try:
    (hours, minutes) = map(int, time_str.split(':'))
    if hours == 24:
      hours = 0
    return datetime.time(hours, minutes)
  except BaseException as e:
    print('Could not parse 24 hour time: %s: %s' % (time_str, e))
    return None


def parse_appearances(schedule_json, day_index, location_map):
  columns = _get_columns(schedule_json)

  seen_appearances = set()
  not_found_locations = set()

  result = []
  for row in schedule_json['data']:
    if day_index != int(row[columns['dayorder']]):
      continue

    location_id = row[columns['locationid']]
    location = location_map.get(location_id)
    if location is None:
      not_found_locations.add(location_id)
      continue

    start_time = row[columns['start24']]
    end_time = row[columns['end24']]
    appearance_data = (location_id, start_time, end_time)
    if (not appearance_data in seen_appearances):
      seen_appearances.add(appearance_data)
      result.append(Appearance(location,
                               parse_time(start_time),
                               parse_time(end_time)))

  print('Could not find %d locations: %s' %
        (len(not_found_locations), not_found_locations))
  return result


def get_open_at(appearances, when):
  def appearing_now(appearance):
    return appearance.start_time <= when and appearance.end_time >= when

  return filter(appearing_now, appearances)
