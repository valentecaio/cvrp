class Point:
  def __init__(self, x, y):
    self._x = x
    self._y = y

  def __repr__(self):
    return "{x: %s, y: %s}" % (self._x, self._y)

  def distance_to_point(self, p):
    return int( ((self._x - p.x)**2 + (self._y - p.x))**.5 )


class Client:
  def __init__(self, id, demand, x, y):
    self._id = id
    self._demand = demand
    self._pos = Point(x, y)

  def __repr__(self):
    return "(client %s - demand: %s, position: %s)"\
          % (self._id, self._demand, self._pos)

