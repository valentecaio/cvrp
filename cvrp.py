#!/usr/bin/python3

from pprint import pprint
from cli import parse_args, parse_vrp
from classes import Truck
import plot

def print_state(state):
  print("Current state:")
  pprint(state)

def print_clients(clients):
  print("Clients:")
  pprint(clients)

def method1(depot, clients, capacity):
  # initial state
  state = {
    'clients_to_visit': [client.id for client in clients],
    'trucks': [],
    'cost': 0
  }

  print("----- INITIAL STATE -----")
  print_clients(clients)
  print_state(state)

  while len(state['clients_to_visit']) > 0:
    # create a truck to visit nodes that have not been visited before
    truck = Truck(len(state['trucks']), capacity, depot)
    state['trucks'].append(truck)

    # truck looping
    while True:
      # calculate costs
      costs = {}
      for client_id in state['clients_to_visit']:
        client = clients[client_id]
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
        if clients[candidate_id].demand <= truck.capacity:
          # this is a good candidate, it will be the next node
          next_node = clients[candidate_id]
          cost_to_next_node = candidate_cost
          break
      else:
        # if truck capacity is not enough for any client, return to depot
        next_node = depot
        cost_to_next_node = truck.position.distance_to_node(depot.x, depot.y)

      # go to next node and update state
      truck.move_to_node(next_node)
      state['cost'] += cost_to_next_node
      if next_node.id in state['clients_to_visit']:
        state['clients_to_visit'].remove(next_node.id)

      # stop truck looping when truck has returned to depot
      if truck.position == depot: break
  
  print("----- FINAL STATE -----")
  print_state(state)
  return state

def main():
  algorithm, filepath, verbose, cli_capacity = parse_args()
  depot, clients, vrp_capacity = parse_vrp(filepath)
  capacity = cli_capacity if cli_capacity else vrp_capacity
  print("depot: %s" % depot)
  print("truck capacity: %s" % capacity)
  results = method1(depot, clients, capacity)
  # plot.draw_initial_state(depot, clients)
  plot.draw_results(depot, clients, results)


if __name__ == "__main__":
  main()

