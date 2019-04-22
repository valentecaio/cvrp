class Node:
  def __init__(self, id, demand, x, y):
    self.id = id
    self.demand = int(demand)
    self.x = int(x)
    self.y = int(y)

  def __repr__(self):
    return "(node %s - demand: %s, position: (%s, %s) )"\
          % (self.id, self.demand, self.x, self.y)

  def distance_to_node(self, x, y):
    return int( ( (self.x - x)**2 + (self.y - y)**2 )**.5 )


class Truck:
  def __init__(self, id, capacity):
    self.id = id
    self.capacity = int(capacity)
    self.route = []

  def __repr__(self):
    return "(truck %s - capacity: %s, route: %s)"\
          % (self.id, self.capacity, self.route)

  def move_to_node(self, node):
    self.capacity -= node.demand
    self.route.append(node.id)
