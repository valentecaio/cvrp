import math
import initial_solution
import random
from copy import deepcopy
from constants import INITIAL_TEMP, FINAL_TEMP, T_FACTOR, N_FACTOR, VERBOSE


### TRANSFORMATION FUNCTIONS ###

# swap two random elements in a given solution
def transf_swap(solution):
  # keep original values
  new_solution = deepcopy(solution)

  # pick two random indexes in the route,
  # excluding the first and the last, that point to depot
  i1 = random.randint(1, len(solution)-2)
  i2 = random.randint(1, len(solution)-2)
  if VERBOSE: print("Swapping indexes %s and %s" % (i1, i2))

  # swap them
  new_solution[i1], new_solution[i2] = solution[i2], solution[i1]
  return new_solution

# move a random element in a given solution to a random new index
def transf_move(solution):
  # pick two random indexes in the route,
  # excluding the first and the last, that point to depot
  i1 = random.randint(1, len(solution)-2)
  i2 = random.randint(1, len(solution)-2)
  # i1 must be smaller than i2
  i1, i2 = min(i1, i2), max(i1, i2)
  if VERBOSE: print("Moving value from index %s to index %s" % (i1, i2))

  # move value from index i1 to index i2
  return solution[:i1] + solution[i1+1:i2] + [solution[i1]] + solution[i2:]

# invert a random part of a given solution
def transf_flip(solution):
  # pick two random indexes in the route
  i1 = random.randint(1, len(solution)-2)
  i2 = random.randint(1, len(solution)-2)
  # i1 must be smaller than i2
  i1, i2 = min(i1, i2), max(i1, i2)
  if VERBOSE: print("Inverting solution from index %s to index %s" % (i1, i2))

  # invert values from index i1 to index i2
  return solution[:i1] + solution[i1:i2][::-1] + solution[i2:]


### ALGORITHM FUNCTIONS ###

def is_valid_solution(solution, nodes, capacity):
  end = start = 0
  while end < len(solution):
    # find next route in solution
    start = end
    end = start + solution[start:].index(0) + 1
    route = solution[start:end]
    # if route demand is greater than truck capacity, this solution is not ok
    route_demand = sum([nodes[client_id].demand for client_id in route])
    if route_demand > capacity: return False
    # print("start = %s, end = %s, route_cost = %s" % (start, end, route_demand))
  # all routes are below truck capacity, solution ok
  return True


def is_acceptable(delta, T):
  p = math.exp(-delta/T)
  return random.random() < p


def generate_neighbor(solution):
  #apply randomly one of the three rules
  opts = [transf_swap, transf_move, transf_flip]
  return opts[random.randint(0, 2)](solution)


def solution_cost(solution, nodes):
  cost = 0
  node = nodes[solution[0]]
  for sol in solution[1:]:
    adj_node = nodes[sol]
    cost += node.distance_to_node(adj_node.x, adj_node.y)
    # print("cost from %s to %s is %s" % (node.id, adj_node.id, cost))
    node = adj_node
  return cost


def annealing(nodes, capacity):
  T = INITIAL_TEMP
  N = int(len(nodes)*N_FACTOR)

  best = current = initial_solution.greedy(nodes, capacity, 'annealing')
  cost_best = cost_current = solution_cost(current, nodes)

  while T > FINAL_TEMP:
    i = 0

    #local search iteration
    while i < N:
      #generate a new state from the current state
      new = generate_neighbor(current)

      # skip invalid solutions
      if not is_valid_solution(new, nodes, capacity): continue

      # calculate cost delts
      cost_new = solution_cost(new, nodes)
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

