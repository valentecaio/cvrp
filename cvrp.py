#!/usr/bin/python3

from pprint import pprint
from parser import parse_args, parse_vrp
from copy import deepcopy
from time import process_time
from classes import Route
import random
import math
import ga
import initial_solution
import simulated_annealing
import local_search
# import plot

### GLOBAL VARIABLES ###

nodes = None        # nodes loaded from given file
capacity = None     # capacity of a truck, override with -q
verbose = False     # enable logs, override with -v

### DEBUG FUNCTIONS ###

def print_nodes():
  print("Nodes:")
  pprint(nodes)

def print_solution(solution):
  print("Solution:")
  pprint(solution)

### MAIN ###

def main():
  # set global variables from input
  global nodes, capacity, verbose
  algorithm, filepath, cli_verbose, cli_capacity = parse_args()
  nodes, vrp_capacity = parse_vrp(filepath)
  verbose = cli_verbose if cli_verbose else verbose
  capacity = cli_capacity if cli_capacity else vrp_capacity

  print_nodes()

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

