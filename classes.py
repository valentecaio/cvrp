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


class State:
  def __init__(self, clients_to_visit):
    self.clients_to_visit = clients_to_visit
    self.trucks = []
    self.cost = 0

  def __repr__(self):
    return "(clients_to_visit %s, cost: %s)"\
          % (self.clients_to_visit, self.cost)

  def remove_client(self, id_to_remove):
    if id_to_remove in self.clients_to_visit:
      self.clients_to_visit.remove(id_to_remove)
