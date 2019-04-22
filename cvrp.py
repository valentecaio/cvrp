#!/usr/bin/python3

from pprint import pprint
from cli import parse_args, parse_vrp
#import plot
import random
from copy import deepcopy

### GLOBAL VARIABLES ###

nodes = None
capacity = None

INITIAL_TEMP = 20
FINAL_TEMP = 1
T_FACTOR = 0.95 #decreasing temperature by 0.05
N_FACTOR = None #neighborhood ratio factor

# SIZEFACTOR = 8 
# CUTOFF = 0.2
# FINDIVISOR = 50

### DEBUG FUNCTIONS ###

def print_nodes():
  print("Nodes:")
  pprint(nodes)


### TRANSFORMATION FUNCTIONS ###

# all the transformation functions belo assure that their output
# are valid solutions, which means, their output contain only
# routes whose total demand is below a truck capacity

# swap two random elements in a given solution
def transf_swap(route):
  while True:
    # keep original values
    mod_route = deepcopy(route)

    # pick two random indexes in the route,
    # excluding the first and the last, that point to depot
    i1, i2 = random.sample(range(1,len(route)-2), 2)
    print("Swapping indexes %s and %s" % (i1, i2))

    # swap them
    mod_route[i1], mod_route[i2] = route[i2], route[i1]

    # stop looping when a valid solution is found
    if is_valid_solution(mod_route): break
  return mod_route

# move a random element in a given solution to a new random index
def transf_move(route):
  while True:
    # keep original values
    mod_route = deepcopy(route)

    # pick two random indexes in the route,
    # excluding the first and the last, that point to depot
    i1, i2 = random.sample(range(1, len(route)-2), 2)
    # i1 must be smaller than i2
    if i1 > i2:
      i1, i2 = i2, i1
    print("Moving value from index %s to index %s" % (i1, i2))

    # move value from index i1 to index i2
    mod_route = route[0:i1] + route[i1+1:i2] + [route[i1]] + route[i2:len(route)]

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

def is_acceptable(delta, T):
  p = exp(-delta/T)
  return rand() < p

#TODO
def generate_neighbor(state):
  #apply randomly one of the three rules
  return state #temporary

#TODO
def cost(solution):
  return 0



def simulated_annealing():
  T = INITIAL_TEMP
  N = len(nodes)*N_FACTOR

  initial = generate_initial_solution()
  current = initial
  best = current

  while T > FINAL_TEMP:
    i = 0

    #local search iteration
    while i < N:
      #generate a new state from de current state
      new = generate_neighbor(current)
      deltaC = cost(new) - cost(current)

      if deltaC < 0: #new solution is better than current
        current = new
        if cost(new) < cost(best): #new solution is best
          best = new
      #accepts a worse solution w/ a probability of exp(-delta/T)
      elif is_acceptable(deltaC, T):
        current = new

      i += 1
    #decreases temperature
    T *= T_FACTOR



### MAIN ###

def main():
  # set global variables from input
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

  route = transf_move(initial_solution)
  print("New solution: %s" % route)

  # plot.draw_initial_state(depot, nodes)
  # plot.draw_results(nodes, initial_solution)


if __name__ == "__main__":
  main()

