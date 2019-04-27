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
  solution = initial_solution.greedy_in_single_list_format(nodes, capacity)
  print("Initial_solution: %s" % solution)
  # print_solution(solution)

  costSol = simulated_annealing.solution_cost(solution, nodes)
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


  # ###GA TESTING###
  # P1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
  # P2 = [9, 3, 7, 8, 2, 6, 5, 1, 4]

  # child1, child2 = ga.crossover(P1, P2)
  # #print("\nChild 1:\n")
  # #pprint(child1)
  # #print("\nChild 2:\n")
  # #pprint(child2)

if __name__ == "__main__":
  main()

