#!/usr/bin/python3

from pprint import pprint
from cli import parse_args, parse_vrp
from copy import deepcopy
from time import process_time
import random
import math
import ga
# import plot

### GLOBAL VARIABLES ###

nodes = None        # nodes loaded from given file
capacity = None     # capacity of a truck, override with -q
verbose = False     # enable logs, override with -v

INITIAL_TEMP = 2000000
FINAL_TEMP = 1      # stop condition
T_FACTOR = 0.9      # decreasing temperature by (1 - T_FACTOR)
N_FACTOR = 0.9      # neighborhood ratio factor

# SIZEFACTOR = 8 
# CUTOFF = 0.2
# FINDIVISOR = 50


### DEBUG FUNCTIONS ###

def print_nodes():
  print("Nodes:")
  pprint(nodes)


### TRANSFORMATION FUNCTIONS ###

# swap two random elements in a given solution
def transf_swap(solution):
  # keep original values
  new_solution = deepcopy(solution)

  # pick two random indexes in the route,
  # excluding the first and the last, that point to depot
  i1, i2 = random.sample(range(1,len(solution)-2), 2)
  if verbose: print("Swapping indexes %s and %s" % (i1, i2))

  # swap them
  new_solution[i1], new_solution[i2] = solution[i2], solution[i1]
  return new_solution

# move a random element in a given solution to a random new index
def transf_move(solution):
  # pick two random indexes in the route,
  # excluding the first and the last, that point to depot
  i1, i2 = random.sample(range(1, len(solution)-2), 2)
  # i1 must be smaller than i2
  i1, i2 = min(i1, i2), max(i1, i2)
  if verbose: print("Moving value from index %s to index %s" % (i1, i2))

  # move value from index i1 to index i2
  return solution[:i1] + solution[i1+1:i2] + [solution[i1]] + solution[i2:]

# invert a random part of a given solution
def transf_flip(solution):
  # pick two random indexes in the route
  i1, i2 = random.sample(range(1, len(solution)-2), 2)
  # i1 must be smaller than i2
  i1, i2 = min(i1, i2), max(i1, i2)
  if verbose: print("Inverting solution from index %s to index %s" % (i1, i2))

  # invert values from index i1 to index i2
  return solution[:i1] + solution[i1:i2][::-1] + solution[i2:]


### ALGORITHM FUNCTIONS ###

def is_valid_solution(solution):
  end = start = 0
  while end < len(solution):
    # find next route in solution
    start = end
    end = start + solution[start:].index(0) + 1
    route = solution[start:end]
    # if route demand is greater than truck capacity, this solution is not ok
    route_demand = sum([nodes[client_id].demand for client_id in route])
    # if verbose: print("route: %s, demand: %s" % (route, route_demand))
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
  p = math.exp(-delta/T)
  return random.random() < p


def generate_neighbor(solution):
  #apply randomly one of the three rules
  opts = [transf_swap, transf_move, transf_flip]
  return opts[random.randint(0, 2)](solution)


def cost(solution):
  cost = 0
  node = nodes[solution[0]]
  for sol in solution[1:]:
    adj_node = nodes[sol]
    cost += node.distance_to_node(adj_node.x, adj_node.y)
    # print("cost from %s to %s is %s" % (node.id, adj_node.id, cost))
    node = adj_node
  return cost


def simulated_annealing():
  T = INITIAL_TEMP
  N = int(len(nodes)*N_FACTOR)

  best = current = generate_initial_solution()
  cost_best = cost_current = cost(current)

  while T > FINAL_TEMP:
    i = 0

    #local search iteration
    while i < N:
      #generate a new state from the current state
      new = generate_neighbor(current)

      # skip invalid solutions
      if not is_valid_solution(new): continue

      # calculate cost delts
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
    #current = best
    #decreases temperature
    T *= T_FACTOR
  return best


### MAIN ###

def main():
  # set global variables from input
  global nodes, capacity, verbose
  algorithm, filepath, cli_verbose, cli_capacity = parse_args()
  nodes, vrp_capacity = parse_vrp(filepath)
  verbose = cli_verbose if cli_verbose else verbose
  capacity = cli_capacity if cli_capacity else vrp_capacity
  # print("Capacity Q: %s" % capacity)
  # print_nodes()

  # generate initial solution
  solution = generate_initial_solution()
  #print("Initial_solution: %s" % solution)
  costSol = cost(solution)
  print("Initial cost: %s" % costSol)

  # solution = transf_swap(solution)
  # print("New solution: %s" % solution)
  # costSol = cost(solution)
  # print("Cost: %s" % costSol)

  # solution = transf_move(solution)
  # print("New solution: %s" % solution)
  # costSol = cost(solution)
  # print("Cost: %s" % costSol)

  # solution = transf_flip(solution)
  # print("New solution: %s" % solution)
  # costSol = cost(solution)
  # print("Cost: %s" % costSol)

  # solution = generate_neighbor(solution)
  # print("New neighbor: %s" % solution)
  # costSol = cost(solution)
  # print("Cost: %s" % costSol)


  start_time = process_time()
  bestSolution = simulated_annealing()
  end_time = process_time()
  costBest = cost(bestSolution)
  #print("Best solution: %s" % bestSolution)
  print("Best cost: %s" % costBest)
  print("Took %.3f seconds to execute" % (end_time - start_time))

  # plot.draw_solution(nodes, solution, verbose)


  ###GA TESTING###
  P1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
  P2 = [9, 3, 7, 8, 2, 6, 5, 1, 4]

  child1, child2 = ga.crossover(P1, P2)
  #print("\nChild 1:\n")
  #pprint(child1)
  #print("\nChild 2:\n")
  #pprint(child2)

if __name__ == "__main__":
  main()

