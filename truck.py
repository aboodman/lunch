import geo

class Truck:
  def __init__(self, name = '', position = 0.0, schedule_url = ''):
    self.name = name
    self.position = position
    self.schedule_url = schedule_url

  def __repr__(self):
    return ('<Truck(%s, %f, %f)>' %
            (self.name, self.position.lat, self.position.lon))

  def __eq__(self, other):
    return self.name == other.name and self.position == other.position


def parseAllFromJSON(json):
  # First we need to find the indices of the columns we are interested in. This
  # could just be hardcoded, but that seems brittle somehow.
  field_indicies = {
    'applicant': -1,
    'latitude': -1,
    'longitude': -1,
    'schedule': -1,
  }

  columns = json['meta']['view']['columns']
  for i in xrange(0, len(columns)):
    column = columns[i]
    if column['fieldName'] in field_indicies:
      field_indicies[column['fieldName']] = i
      continue

  # Now, we can parse the rows
  data = json['data']
  result = []
  for row in data:
    applicant = row[field_indicies['applicant']]
    latitude = row[field_indicies['latitude']]
    longitude = row[field_indicies['longitude']]
    schedule = row[field_indicies['schedule']]

    if (latitude == '' or latitude == None or
        longitude == '' or longitude == None):
      continue

    position = geo.Geoposition(float(latitude), float(longitude))
    truck = Truck(applicant, position, schedule)
    result.append(truck)

  return result


def serializeAllToJSON(trucks):
  result = []
  for truck in trucks:
    result.append([truck.name, truck.position.lat, truck.position.lon,
                   truck.schedule_url])
  return result


# TODO(aa): Ideally this function would do something like take a viewport and
# only return trucks within those bounds. If you center the map on the ocean,
# the server should return no data I think.
def getClosest(trucks, origin, quantity):
  def distanceToOrigin(truck):
    return truck.position.getDistanceTo(origin)
  return sorted(trucks, key=distanceToOrigin)[0:quantity]

