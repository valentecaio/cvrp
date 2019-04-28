#!/usr/bin/python3

from pprint import pprint
from time import process_time
import parser
import initial_solution
import simulated_annealing
import local_search
# import plot

### GLOBAL VARIABLES ###

verbose = False     # enable logs, override with -v

### DEBUG FUNCTIONS ###

def print_nodes(nodes):
  print("Nodes:")
  pprint(nodes)

def print_solution(solution):
  print("Solution:")
  pprint(solution)

### MAIN ###

def main():
  global verbose
  algorithm, filepath, cli_verbose, cli_capacity = parser.parse_cli_args()
  nodes, vrp_capacity = parser.parse_vrp(filepath)
  optimal_solution_cost = parser.get_optimal_solution_cost(filepath)
  verbose = cli_verbose if cli_verbose else verbose
  capacity = cli_capacity if cli_capacity else vrp_capacity

  print_nodes(nodes)

  # generate initial solution
  annealing_solution = initial_solution.greedy(nodes, capacity, 'annealing')
  print("Initial_solution: %s" % annealing_solution)
  
  local_search_solution = initial_solution.greedy(nodes, capacity, 'local_search')
  print_solution(local_search_solution)

  costSol = simulated_annealing.solution_cost(annealing_solution, nodes)
  print("Initial cost: %s" % costSol)

  start_time = process_time()
  bestSolution = simulated_annealing.simulated_annealing(nodes, capacity)
  costBest = simulated_annealing.solution_cost(bestSolution, nodes)
  end_time = process_time()
  print("Best solution: %s" % bestSolution)
  print("Best cost: %d" % costBest)
  print("Took %.3f seconds to execute" % (end_time - start_time))

  opt = 1221
  print("Relative dif=  %.3f" % ((costBest - opt)*100 / costBest))

  # # plot.draw_solution(nodes, solution, verbose)


if __name__ == "__main__":
  main()

