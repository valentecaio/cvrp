from copy import deepcopy
from pprint import pprint
from constants import LOOP_LIMIT
import initial_solution_generator
import annealing

def is_valid_path(path, nodes, capacity):
  # if path demand is greater than truck capacity, this solution is not ok
  path_demand = sum([nodes[client_id].demand for client_id in path])
  if path_demand > capacity: return False
  return True

def path_cost(path, nodes):
  cost = 0
  node = nodes[0]
  route = path + [0] #includes depot
  #pprint(route)
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

def two_opt(route, nodes):
  for i in range(0, len(route.path)):
    for j in range(i+1, len(route.path)):
      if j-i == 1: continue # changes nothing, skip then
      new_route = deepcopy(route)
      new_route.path = new_route.path[:i] + new_route.path[i:j][::-1] + new_route.path[j:]
      new_route.cost = path_cost(new_route.path, nodes)
      if new_route.cost < route.cost:
        return new_route
  #return original route if there's no improvements
  return route

def successor_intra_routes(in_solution, nodes):
  for r in range(0, len(in_solution)):
      neighbor = deepcopy(in_solution)
      neighbor[r] = two_opt(neighbor[r], nodes)
      if solution_cost(neighbor) < solution_cost(in_solution):
        return neighbor
  return in_solution


#moves the client of position i in route1 to position j in route2
def move(solution, r1, r2, i, j):
  new = deepcopy(solution)
  route1 = new[r1]
  route2 = new[r2]

  route2.path.insert(j, route1.path[i])
  route1.path.remove(route1.path[i])

  return new

#returns the first improved neighbor by moving one client from one route to another
def successor_inter_routes(in_solution, capacity, nodes):
  costIn = solution_cost(in_solution)
  for r1 in range(0, len(in_solution)):
    for r2 in range(r1+1, len(in_solution)):
      #print("r1= %d r2= %d" % (r1, r2))
      for i in range(0, len(in_solution[r1].path)):
        for j in range(i+1, len(in_solution[r2].path)):
          #create new neighbor with move transformation
          neighbor = move(in_solution, r1, r2, i, j)
          #pprint(in_solution[0].path)
          #check if neighbor is valid -> only need to check the modified route
          if not is_valid_path(neighbor[r2].path, nodes, capacity): 
            #print("not valid")
            continue

          costval = cost(neighbor, [r1,r2], nodes)
          #print("cost= %d" % costval)
          if costval < costIn:
            return neighbor #returns first neighbor better than current 

  return in_solution #no new combination is better -> returns original


def local_search(nodes, capacity, initial_solution = None, initial_solution_func = None):
  # use given initial solution or create one
  if initial_solution == None:
    initial_solution = initial_solution_func(nodes, capacity, 'local_search')

  current = initial_solution
  i = 0
  while i < LOOP_LIMIT:
    i += 1
    neighbor1 = successor_inter_routes(current, capacity, nodes)
    neighbor2 = successor_intra_routes(current, nodes)
    print("[LS] neighbor(inter)= %d neighbor(intra)= %d" % (solution_cost(neighbor1), solution_cost(neighbor2)))
    #pick the best neighbor
    neighbor = neighbor1 if solution_cost(neighbor1) < solution_cost(neighbor2) else neighbor2
    
    # anneal1 = deepcopy(neighbor1)
    # anneal2 = deepcopy(neighbor2)
    # n1 = annealing.solution_cost(initial_solution_generator.format_from_local_search_to_annealing(anneal1), nodes)
    # n2 = annealing.solution_cost(initial_solution_generator.format_from_local_search_to_annealing(anneal2), nodes)

    # print("[SA] neighbor(inter)= %d neighbor(intra)= %d" % (n1, n2))
    
    #if there is no improvements
    if solution_cost(neighbor) >= solution_cost(current):
      break
    #moves
    current = neighbor


  return current

