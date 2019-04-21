#!/usr/bin/python3

from pprint import pprint
from classes import Client
from utils import *

# read vrp file; returns clients and depot data
def parse_vrp(filename):
  # read whole file
  s = open(filename, "r").read()

  # get coordinates substring
  node_coord_section = extract_section(s, "NODE_COORD_SECTION", "DEMAND_SECTION")
  # get demands substring
  demands_section = extract_section(s, "DEMAND_SECTION", "DEPOT_SECTION")
  # get depot substring
  # depot_section = extract_section(s, "DEPOT_SECTION", "EOF")

  # extract client data from strings
  number_of_clients = len(demands_section)
  clients = []
  for i in range(0, number_of_clients):
    client_id, x, y = remove_spaces_in_borders(node_coord_section[i]).split(" ")
    demand = remove_spaces_in_borders(demands_section[i]).split(" ")[-1]
    n = Client(client_id, demand, x, y)
    clients.append(n)
  # pprint(clients)

  # clients[1] is NOT a client: this is the depot
  depot = clients.pop(0)
  return depot, clients

def main():
  depot, clients = parse_vrp("vrp/B-n31-k5.vrp")
  print("depot: %s" % depot)
  print("clients:")
  pprint(clients)


if __name__ == "__main__":
  main()

