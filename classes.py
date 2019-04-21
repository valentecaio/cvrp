class Point:
  def __init__(self, x, y):
    self.x = int(x)
    self.y = int(y)

  def __repr__(self):
    return "{x: %s, y: %s}" % (self.x, self.y)

  def distance_to_point(self, p):
    return int( ((self.x - p.x)**2 + (self.y - p.x))**.5 )


class Client:
  def __init__(self, id, demand, x, y):
    self.id = id
    self.demand = demand
    self.pos = Point(x, y)

  def __repr__(self):
    return "(client %s - demand: %s, position: %s)"\
          % (self.id, self.demand, self.pos)

