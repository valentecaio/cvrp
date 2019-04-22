#!/usr/bin/python3

from pprint import pprint
from cli import parse_args, parse_vrp
import plot
import random
from copy import deepcopy

### GLOBAL ATTRIBUTES ###

nodes = None
capacity = None

### DEBUG FUNCTIONS ###

def print_nodes():
  print("Nodes:")
  pprint(nodes)

### TRANSFORMATION FUNCTIONS ###

def transf_swap(route):
  while True:
    # keep original values
    mod_route = deepcopy(route)

    # pick two random indexes in the route,
    # excluding the first and the last, that point to depot
    node1, node2 = random.sample(range(1,len(route)-2), 2)
    print("Swapping indexes %s and %s" % (node1, node2))

    # swap them
    mod_route[node1], mod_route[node2] = route[node2], route[node1]

    # stop looping when a valid solution is found
    if is_valid_solution(mod_route): break
  return mod_route


### ALGORITHM FUNCTIONS ###

def is_valid_solution(solution):
  end = start = 0
  while end < len(solution):
    # find next route in solution
    start = end + 1
    end = start + solution[start:].index(0) + 1
    route = solution[start:end]
    # if route demand is greater than truck capacity, this solution is not ok
    route_demand = sum([nodes[client_id].demand for client_id in route])
    if route_demand > capacity: return False
    # print("start = %s, end = %s, route_cost = %s" % (start, end, route_demand))
  # all routes are below truck capacity, solution ok
  return True

# greedy algorithm that generates a valid initial solution
def generate_initial_solution():
  depot = nodes[0]

  # initial state
  clients_to_visit = [node.id for node in nodes[1:]]
  route = [0]
  total_cost = 0

  while len(clients_to_visit) > 0:
    # create a truck to visit nodes that have not been visited before
    truck_capacity = capacity
    truck_position = 0

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
      route.append(next_node.id)
      truck_capacity -= next_node.demand
      truck_position = next_node.id
      total_cost += cost_to_next_node
      if next_node.id in clients_to_visit:
        clients_to_visit.remove(next_node.id)

      # stop truck looping when truck has returned to depot
      if truck_position == depot.id: break

  return route

### MAIN ###

def main():
  # set global attributes from input
  global nodes, capacity
  algorithm, filepath, verbose, cli_capacity = parse_args()
  nodes, vrp_capacity = parse_vrp(filepath)
  capacity = cli_capacity if cli_capacity else vrp_capacity
  print("Capacity Q: %s" % capacity)
  print_nodes()

  # generate initial solution
  initial_solution = generate_initial_solution()
  print("Initial_solution: %s" % initial_solution)

  route = transf_swap(initial_solution)
  print("New solution: %s" % route)


  # plot.draw_initial_state(depot, nodes)
  # plot.draw_results(nodes, initial_solution)


if __name__ == "__main__":
  main()

