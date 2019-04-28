from copy import deepcopy


def is_valid_path(path, nodes, capacity):
  # if path demand is greater than truck capacity, this solution is not ok
  path_demand = sum([nodes[client_id].demand for client_id in path])
  return path_demand > capacity

def path_cost(path, nodes):
  cost = 0
  node = nodes[0]
  route = path + [0] #includes depot
  for node_id in route:
    adj_node = nodes[node_id]
    cost += node.distance_to_node(adj_node.x, adj_node.y)
    node = adj_node

  return cost

def cost(solution, routes, nodes):
  #recalculate all cost for the given modified routes
  for r in routes:
    solution[r].cost = path_cost(solution[r].path, nodes)
  #sum the cost of all solutions again
  return solution_cost(solution)

def solution_cost(solution, _nodes = None):
  return sum(route.cost for route in solution)

def flip(route, nodes):
  for i in range(0, len(route)):
    for j in range(i+1, len(route)):
      if j-i == 1: continue # changes nothing, skip then
      new_rote = deepcopy(route)
      new_route = new_route[:i] + new_route[i:j][::-1] + new_route[j:]
      new_route.cost = path_cost(new_route.path, nodes)
      if new_route.cost < route.cost:
        return new_route
  #return original route if there's no improvements
  return route

def successor_intra_routes(in_solution):
  for r in range(0, len(in_solution)):
      neighbor = deepcopy(in_solution)
      neighbor[r] = two_opt(neighbor[r])
      if solution_cost(neighbor) < solution_cost(in_solution):
        return neighbor
  return in_solution


#moves the client of position i in route1 to position j in route2
def move(solution, r1, r2, i, j):
  new = deepcopy(in_solution)
  route1 = new[r1]
  route2 = new[r2]

  route2.insert(j, route1[i])
  route1.remove(route1[i])

  return new

def successor_inter_routes(in_solution, capacity, nodes):
  costIn = solution_cost(in_solution)
  for r1 in range(0, len(in_solution)):
    for r2 in range(r1+1, len(in_solution)):
      for i in range(0, len(in_solution[r1].path)):
        for j in range(i+1, len(in_solution[r2].path)):
          #create new neighbor with move transformation
          neighbor = move(neighbor, r1, r2, i, j)
          
          #check if neighbor is valid -> only need to check the modified route
          if not is_valid_path(neighbor[r2], nodes, capacity): continue

          if cost(neighbor, [r1,r2], nodes) < costIn:
            return neighbor #returns first neighbor that is better than current 

  return in_solution #no new combination is better -> returns original

def local_search(nodes, capacity, initial_solution_func):
  LOOP_LIMIT = 1000
  current = initial_solution_func(nodes, capacity)
  i = 0
  while i < LOOP_LIMIT:
    i += 1
    neighbor1 = successor_inter_routes(current, capacity, nodes)
    neighbor2 = successor_intra_routes(current)
    #pick the best neighbor
    neighbor = neighbor1 if neighbor1 < neighbor2 else neighbor2
    #if there is no improvements
    if solution_cost(neighbor) > solution_cost(current.cost):
      break
    #moves
    current = neighbor

  return current

