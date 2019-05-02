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
  parser.add_argument('algorithm', choices=['annealing', 'local_search'],
                      help='Search Algorithm to be used', nargs=1)
  parser.add_argument('initial_solution_algorithm', choices=['greedy', 'naive'],
                      help='Algorithm used in Initial Solution generation', nargs=1)
  parser.add_argument('vrp_filepath', help='Path of input file', nargs=1)

  # optional args
  parser.add_argument('-q', '--capacity', dest='capacity', type=int,
                      help='override truck capacity')
  parser.add_argument('-n', '--times-to-run', dest='times_to_run', type=int, default=1,
                      help='specify how many times the algorithm will be executed')
  parser.add_argument('--learn', dest='learn', action='store_true',
                      help='use best solution as initial solution in next instance')

  args = parser.parse_args()
  return  args.algorithm.pop(),\
          args.initial_solution_algorithm.pop(),\
          args.vrp_filepath.pop(),\
          args.capacity,\
          args.times_to_run,\
          args.learn


# parse csv file and return optimal solution values
def parse_optimal_solutions():
  # read whole file and split by lines
  lines = open("vrp/inputs_optimal.csv").read().split("\n")
  # remove empty lines
  lines.remove('')
  # return a dict with {key: value} = {vrp_name: vrp_optimal_solution}
  return dict(line.split(";") for line in lines)


# filename may be "vrp/B-n31-k5.vrp" or "B-n31-k5.vrp"
def get_optimal_cost(vrp_filepath):
  bar_index = vrp_filepath.rfind('/')
  vrp_filename = vrp_filepath[bar_index+1:]
  return int(parse_optimal_solutions()[vrp_filename])


def to_csv(r):
  return "%s;%s;%s;%s;%s;%s;%s\n" % (r["initial_temp"], r["t_factor"], r["n_factor"], r["cost"], r["execution time"], r["diff to optimal"], r["diff to initial"])


def write_csv(filepath, optimal_cost, best, average, all_results):
  header = "initial_temp;t_factor;n_factor;cost;execution time;diff to optimal;diff to initial\n"
  s = "file:;%s;;optimal cost:;%s" %(filepath, optimal_cost) + "\n\n"
  s += "BEST\n\n" + header + to_csv(best) + "\n\n"
  s += "AVERAGE\n\n" + header + to_csv(average) + "\n\n"
  s += "ALL BEST RESULTS\n\n" + header
  for r in all_results:
    s += to_csv(r["best"])
  s += "\n\nALL AVERAGE RESULTS\n\n" + header
  for r in all_results:
    s += to_csv(r["average"])
  f = open("results_%s.csv" % filepath.replace("/", "-"),"w+")
  f.write(s)
