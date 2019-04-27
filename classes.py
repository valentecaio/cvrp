class Node:
  def __init__(self, id, demand, x, y):
    self.id = id
    self.demand = int(demand)
    self.x = int(x)
    self.y = int(y)

  def __repr__(self):
    return "(node %s - demand: %s, position: (%s, %s) )"\
          % (self.id, self.demand, self.x, self.y)

  def __eq__(self, other):
    return self.id == other.id

  def distance_to_node(self, x, y):
    # cast to int to avoid working with floats
    return int( ( (self.x - x)**2 + (self.y - y)**2 )**.5 )

class Route:
  def __init__(self):
    self.path = [0]
    self.cost = 0

  def __repr__(self):
    return "Route - cost: %s - path: %s" % (self.cost, self.path)
