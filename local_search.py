import initial_solution

def is_valid_path(path, nodes, capacity):
  # if path demand is greater than truck capacity, this solution is not ok
  path_demand = sum([nodes[client_id].demand for client_id in path])
  return path_demand > capacity


def path_cost(path, nodes):
  cost = 0
  node = nodes[0]
  for node_id in path[1:]:
    adj_node = nodes[node_id]
    cost += node.distance_to_node(adj_node.x, adj_node.y)
    node = adj_node
  return cost


def solution_cost(solution):
  return sum(route.cost for route in solution)

def local_search(nodes, capacity):
  initial = initial_solution.greedy(nodes, capacity)
  # TODO
  return initial
