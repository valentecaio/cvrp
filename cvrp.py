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

# all the transformation functions below assure that their output
# are valid solutions, which means, their output contain only
# routes whose total demand is below a truck capacity

# swap two random elements in a given solution
def transf_swap(solution):
  while True:
    # keep original values
    new_solution = deepcopy(solution)

    # pick two random indexes in the route,
    # excluding the first and the last, that point to depot
    i1, i2 = random.sample(range(1,len(solution)-1), 2)
    print("Swapping indexes %s and %s" % (i1, i2))

    # swap them
    new_solution[i1], new_solution[i2] = solution[i2], solution[i1]

    # stop looping when a valid solution is found
    if is_valid_solution(new_solution): break
  return new_solution


# move a random element in a given solution to a random new index
def transf_move(solution):
  while True:
    # keep original values
    new_solution = deepcopy(solution)

    # pick two random indexes in the route,
    # excluding the first and the last, that point to depot
    i1, i2 = random.sample(range(1, len(solution)-1), 2)
    # i1 must be smaller than i2
    i1, i2 = min(i1, i2), max(i1, i2)
    print("Moving value from index %s to index %s" % (i1, i2))

    # move value from index i1 to index i2
    new_solution = solution[:i1] + solution[i1+1:i2] + [solution[i1]] + solution[i2:]

    # stop looping when a valid solution is found
    if is_valid_solution(new_solution): break
  return new_solution


# invert a random part of a given solution
def transf_flip(solution):
  while True:
    # keep original values
    new_solution = deepcopy(solution)

    # pick two random indexes in the route
    i1, i2 = random.sample(range(1, len(solution)-1), 2)
    # i1 must be smaller than i2
    i1, i2 = min(i1, i2), max(i1, i2)
    print("Inverting solution from index %s to index %s" % (i1, i2))

    # invert values from index i1 to index i2
    new_solution = solution[:i1] + solution[i1:i2][::-1] + solution[i2:]

    # stop looping when a valid solution is found
    if is_valid_solution(new_solution): break
  return new_solution


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


def generate_neighbor(solution):
  #apply randomly one of the three rules
  opt = random.randint(0, 2)
  print("opt= %d" % opt)
  if opt == 0:
    return transf_swap(solution)
  elif opt == 1:
    return transf_move(solution)
  else:
    return transf_flip(solution)


def cost(solution):
  cost = 0
  node = nodes[solution[0]]
  for sol in solution[1:]:
    adj_node = nodes[sol]
    cost += node.distance_to_node(adj_node.x, adj_node.y)
    node = adj_node
  return cost


def simulated_annealing():
  T = INITIAL_TEMP
  N = len(nodes)*N_FACTOR

  best = current = initial = generate_initial_solution()
  cost_best = cost_current = cost_initial = cost(initial)

  while T > FINAL_TEMP:
    i = 0

    #local search iteration
    while i < N:
      #generate a new state from the current state
      new = generate_neighbor(current)
      cost_new = cost(new)

      deltaC = cost_new - cost_current

      if deltaC < 0: #new solution is better than current 
        current = new
        cost_current = cost_new
        if cost_new < cost_best: #new solution is best
          best = new
          cost_best = cost_new
      #accepts a worse solution w/ a probability of exp(-delta/T)
      elif is_acceptable(deltaC, T):
        current = new
        cost_current = cost_new

      i += 1
    #decreases temperature
    T *= T_FACTOR
  return best


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
  solution = generate_initial_solution()
  print("Initial_solution: %s" % solution)
  costSol = cost(solution)
  print("Cost: %s" % costSol)

  solution = transf_swap(solution)
  print("New solution: %s" % solution)
  costSol = cost(solution)
  print("Cost: %s" % costSol)

  solution = transf_move(solution)
  print("New solution: %s" % solution)
  costSol = cost(solution)
  print("Cost: %s" % costSol)

  solution = transf_flip(solution)
  print("New solution: %s" % solution)
  costSol = cost(solution)
  print("Cost: %s" % costSol)

  solution = generate_neighbor(solution)
  print("New neighbor: %s" % solution)
  costSol = cost(solution)
  print("Cost: %s" % costSol)

  # plot.draw_initial_state(depot, nodes)
  # plot.draw_results(nodes, initial_solution)

if __name__ == "__main__":
  main()

