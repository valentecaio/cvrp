import argparse
from classes import Client, Point

# returns a substring of s that starts right after flag_start and
# ends right before flag_end
def extract_section(s, flag_start, flag_end):
  return s[s.find(flag_start)+len(flag_start):s.find(flag_end)]

# read vrp file; returns clients and depot data
def parse_vrp(filepath):
  # read whole file
  s = open(filepath, "r").read()

  # get coordinates substring
  node_coord_section = extract_section(s, "NODE_COORD_SECTION", "DEMAND_SECTION").split('\n')[1:-1]
  # get demands substring
  demands_section = extract_section(s, "DEMAND_SECTION", "DEPOT_SECTION").split('\n')[1:-1]

  # extract client data from read strings
  number_of_clients = len(demands_section)
  clients = []
  for i in range(1, number_of_clients):
    # parse client data
    x, y = node_coord_section[i].strip().split(" ")[1:]
    demand = demands_section[i].strip().split(" ")[-1]
    # create client and add to clients list
    clients.append(Client(i-1, demand, x, y))

  # the first "client" of the list is NOT a client: this is the depot
  x, y = node_coord_section[0].strip().split(" ")[1:]
  depot = Point(x, y)

  # extract capacity data from file
  capacity = extract_section(s, "CAPACITY :", "NODE_COORD_SECTION").strip()

  return depot, clients, capacity

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
  parser.add_argument('-q', '--capacity', dest='capacity', type=int,
                      help='override truck capacity')

  args = parser.parse_args()
  return args.algorithm.pop(), args.filepath.pop(), args.verbose, args.capacity
