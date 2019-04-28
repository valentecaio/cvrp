import argparse
from classes import Node

# returns a substring of s that starts right after flag_start and
# ends right before flag_end
def extract_section(s, flag_start, flag_end):
  # replace tab by spaces to ensure output format
  return s[s.find(flag_start)+len(flag_start):s.find(flag_end)].replace('\t',' ')

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
  nodes = []
  for i in range(0, number_of_clients):
    # parse client data
    x, y = node_coord_section[i].strip().split(" ")[1:]
    demand = demands_section[i].strip().split(" ")[-1]
    # create node and add to nodes list
    nodes.append(Node(i, demand, x, y))

  # extract capacity data from file
  capacity = int(extract_section(s, "CAPACITY :", "NODE_COORD_SECTION").strip())

  return nodes, capacity


def parse_cli_args():
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


# parse csv file and return optimal solution values
def parse_optimal_solutions():
  # read whole file and split by lines
  lines = open("vrp/inputs_optimal.csv").read().split("\n")
  # return a dict with {key: value} = {vrp_name: vrp_optimal_solution}
  return dict(line.split(";") for line in lines)


# filename may be "vrp/B-n31-k5.vrp" or "B-n31-k5.vrp"
def get_optimal_solution_cost(vrp_filepath):
  bar_index = vrp_filepath.rfind('/')
  vrp_filename = vrp_filepath[bar_index+1:]
  return int(parse_optimal_solutions()[vrp_filename])

