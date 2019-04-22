#!/usr/bin/python3

from pprint import pprint
from cli import parse_args, parse_vrp
from classes import Truck, State
import plot
import random

### DEBUG FUNCTIONS ###

def print_state(state):
  print("Current state:")
  print(state)
  pprint(state.trucks)

def print_nodes(nodes):
  print("Nodes:")
  pprint(nodes)

### ALGORITHM FUNCTIONS ###

def is_valid_solution(nodes, capacity, solution):
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

def generate_initial_solution(nodes, capacity):
  depot = nodes[0]

  # initial state
  state = State([node.id for node in nodes[1:]])

  while len(state.clients_to_visit) > 0:
    # create a truck to visit nodes that have not been visited before
    truck = Truck(len(state.trucks), capacity, depot)
    state.trucks.append(truck)

    # truck looping
    while True:
      # calculate costs
      costs = {}
      for client_id in state.clients_to_visit:
        client = nodes[client_id]
        cost = truck.position.distance_to_node(client.x, client.y)
        # print("The cost to move to client %s is %s" % (client.id, cost))
        costs[client.id] = cost
      # sort possibilities from smallest to biggest cost, [(client_id, cost)]
      costs = sorted(costs.items(), key = lambda kv: (kv[1], kv[0]))
      # print("Sorted costs : %s " % costs)

      # choose next destination (next client or depot)
      while len(costs) > 0:
        # pick first element of list
        candidate_id, candidate_cost = costs[0]
        costs = costs[1:]
        if nodes[candidate_id].demand <= truck.capacity:
          # this is a good candidate, it will be the next node
          next_node = nodes[candidate_id]
          cost_to_next_node = candidate_cost
          break
      else:
        # if truck capacity is not enough for any client, return to depot
        next_node = depot
        cost_to_next_node = truck.position.distance_to_node(depot.x, depot.y)

      # go to next node and update state
      truck.move_to_node(next_node)
      state.cost += cost_to_next_node
      state.remove_client(next_node.id)

      # stop truck looping when truck has returned to depot
      if truck.position == depot: break
  
  # convert state to an initial solution in the desired format
  # ex: [0, 21, 16, 18, 25, 5, 4, 29, 8, 11, 0, 28, 26, 12, 23, 7, 6, 0, 22, 9, 13, 17, 30, 3, 2, 0, 24, 19, 1, 15, 14, 10, 20, 0, 27, 0]
  initial_solution = [0]
  for truck in state.trucks:
    for client_id in truck.route[1:]:
      initial_solution.append(client_id)

  return initial_solution

def is_acceptable(deltaE, T):
  p = exp(-deltaE/T)
  return rand() < p

### MAIN ###

def main():
  algorithm, filepath, verbose, cli_capacity = parse_args()
  nodes, vrp_capacity = parse_vrp(filepath)
  capacity = cli_capacity if cli_capacity else vrp_capacity
  print("Capacity Q: %s" % capacity)
  print_nodes(nodes)
  initial_solution = generate_initial_solution(nodes, capacity)
  print("Initial_solution: %s" % initial_solution)

  # plot.draw_initial_state(depot, nodes)
  # plot.draw_results(nodes, initial_solution)
  is_valid_solution(nodes, capacity, initial_solution)

if __name__ == "__main__":
  main()

