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


class Truck:
  def __init__(self, id, capacity, position):
    self.id = id
    self.capacity = int(capacity)
    self.position = position # position must be a Node object
    self.route = [position.id]

  def __repr__(self):
    return "(truck %s - capacity: %s, route: %s)"\
          % (self.id, self.capacity, self.route)

  def __eq__(self, other):
    return self.id == other.id

  def move_to_node(self, node):
    self.capacity -= node.demand
    self.route.append(node.id)
    self.position = node
