from classes import Route
from copy import deepcopy

# greedy algorithm that generates a valid initial solution
def greedy(nodes, capacity, algorithm = 'default'):
  depot = nodes[0]

  # initial state
  clients_to_visit = [node.id for node in nodes[1:]]
  routes = []

  while len(clients_to_visit) > 0:
    # create a truck to visit nodes that have not been visited before
    truck_capacity = capacity
    truck_position = 0
    # create empty route starting in 0
    route = Route([0], 0)
 
    # truck looping
    while True:
      # calculate costs
      costs = {}
      for client_id in clients_to_visit:
        client = nodes[client_id]
        cost = nodes[truck_position].distance_to_node(client.x, client.y)
        costs[client_id] = cost
      # sort possibilities from smallest to biggest cost, [(client_id, cost)]
      costs = sorted(costs.items(), key = lambda kv: (kv[1], kv[0]))

      # choose next destination (next client or depot)
      while len(costs) > 0:
        # pick first element of list
        candidate_id, candidate_cost = costs[0]
        costs = costs[1:]
        if nodes[candidate_id].demand <= truck_capacity:
          # this is a good candidate, it will be the next node
          next_node = nodes[candidate_id]
          cost_to_next_node = candidate_cost
          break
      else:
        # if truck capacity is not enough for any client, return to depot
        next_node = depot
        cost_to_next_node = nodes[truck_position].distance_to_node(depot.x, depot.y)

      # go to next node and update state
      route.path.append(next_node.id)
      route.cost += cost_to_next_node
      truck_capacity -= next_node.demand
      truck_position = next_node.id

      if next_node.id in clients_to_visit:
        clients_to_visit.remove(next_node.id)

      # stop truck looping when truck has returned to depot
      if truck_position == depot.id: break

    # store route data
    routes.append(route)

  # format output according to algorithm
  if algorithm == 'annealing':
    return format_to_annealing(routes)
  elif algorithm == 'local_search':
    return format_to_local_search(routes)
  else:
    return routes


'''
input is a list of Routes starting and ending in 0:
[
  Route - cost: 158 - path: [0, 21, 16, 18, 25, 5, 4, 29, 8, 11, 0],
  Route - cost: 115 - path: [0, 28, 26, 12, 23, 7, 6, 0],
  Route - cost: 240 - path: [0, 22, 9, 13, 17, 30, 3, 2, 0],
  Route - cost: 244 - path: [0, 24, 19, 1, 15, 14, 10, 20, 0],
  Route - cost: 188 - path: [0, 27, 0]
]

output is a list of Routes without zeros:
[
  Route - cost: 158 - path: [21, 16, 18, 25, 5, 4, 29, 8, 11],
  Route - cost: 115 - path: [28, 26, 12, 23, 7, 6],
  Route - cost: 240 - path: [22, 9, 13, 17, 30, 3, 2],
  Route - cost: 244 - path: [24, 19, 1, 15, 14, 10, 20],
  Route - cost: 188 - path: [27]
]

'''
def format_to_local_search(solution):
  for route in solution:
    # remove zeros
    route.path = route.path[1:-1]
  return solution


'''
input is a list of Routes starting and ending in 0:
[
  Route - cost: 158 - path: [0, 21, 16, 18, 25, 5, 4, 29, 8, 11, 0],
  Route - cost: 115 - path: [0, 28, 26, 12, 23, 7, 6, 0],
  Route - cost: 240 - path: [0, 22, 9, 13, 17, 30, 3, 2, 0],
  Route - cost: 244 - path: [0, 24, 19, 1, 15, 14, 10, 20, 0],
  Route - cost: 188 - path: [0, 27, 0]
]

output is a simple list of integers:
[
  0, 21, 16, 18, 25, 5, 4, 29, 8, 11,
  0, 28, 26, 12, 23, 7, 6,
  0, 22, 9, 13, 17, 30, 3, 2,
  0, 24, 19, 1, 15, 14, 10, 20,
  0, 27, 0
]
'''
def format_to_annealing(solution):
  solution_as_list = [0]
  for route in solution:
    solution_as_list += route.path[1:]
  return solution_as_list
