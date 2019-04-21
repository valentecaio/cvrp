#!/usr/bin/python3

import argparse
from pprint import pprint
from classes import Client
from utils import *

# parse CLI args
def parse_args():
  parser = argparse.ArgumentParser(description='Capacitated Vehicle Routing Problem in Python')

  # mandatory args
  parser.add_argument('algorithm', choices=['1', '2'],
                      help='Search Algorithm to be used', nargs=1)
  parser.add_argument('filepath', help='Path of input file', nargs=1)

  # optional args
  parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                      help='execute script in verbose mode')

  args = parser.parse_args()
  return args.algorithm.pop(), args.filepath.pop(), args.verbose

# read vrp file; returns clients and depot data
def parse_vrp(filepath):
  # read whole file
  s = open(filepath, "r").read()

  # get coordinates substring
  node_coord_section = extract_section(s, "NODE_COORD_SECTION", "DEMAND_SECTION")
  # get demands substring
  demands_section = extract_section(s, "DEMAND_SECTION", "DEPOT_SECTION")
  # get depot substring
  # depot_section = extract_section(s, "DEPOT_SECTION", "EOF")

  # extract client data from read strings
  number_of_clients = len(demands_section)
  clients = []
  for i in range(0, number_of_clients):
    # parse client data
    client_id, x, y = remove_spaces_in_borders(node_coord_section[i]).split(" ")
    demand = remove_spaces_in_borders(demands_section[i]).split(" ")[-1]
    # create client and add to clients list
    clients.append(Client(client_id, demand, x, y))

  # clients[1] is NOT a client: this is the depot
  depot = clients.pop(0)
  return depot, clients

def main():
  algorithm, filepath, verbose = parse_args()
  depot, clients = parse_vrp(filepath)
  print("depot: %s" % depot)
  print("clients:")
  pprint(clients)


if __name__ == "__main__":
  main()

