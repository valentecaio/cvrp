#!/usr/bin/python3

from pprint import pprint
from time import process_time
from constants import print_constants, PLOT
import initial_solution_generator
import parser
import annealing
import local_search
# if PLOT:
#   import plot

### DEBUG FUNCTIONS ###

def print_nodes(nodes):
  print("Nodes:")
  pprint(nodes)

def print_solution(solution):
  print("Solution:")
  pprint(solution)

def percent(a, b):
  return 100 * (a - b) / a


### MAIN ###

def main():
  # get and handle different inputs
  algorithm, initial_solution_algorithm, filepath, cli_capacity, times_to_run = parser.parse_cli_args()
  nodes, vrp_capacity = parser.parse_vrp(filepath)
  optimal_cost = parser.get_optimal_cost(filepath)
  capacity = cli_capacity if cli_capacity else vrp_capacity

  # select algorithm
  if algorithm == "annealing":
    cost_func = annealing.solution_cost
    alg_func = annealing.annealing
  elif algorithm == "local_search":
    cost_func = local_search.solution_cost
    alg_func = local_search.local_search

  # select initial solution algorithm
  if initial_solution_algorithm == "greedy":
    initial_solution_func = initial_solution_generator.greedy
  elif initial_solution_algorithm == "naive":
    initial_solution_func = initial_solution_generator.naive

  print("\n\n############## INPUT ##############\n\n")

  print("algorithm: %s" % algorithm)
  print("initial solution algorithm: %s" % initial_solution_algorithm)
  print("truck capacity: %s" % capacity)
  print("filepath: %s" % filepath)
  print("optimal solution cost: %s\n" % optimal_cost)
  print_constants()
  print_nodes(nodes)



  print("\n\n############## INITIAL SOLUTION ##############\n\n")

  # generate initial solution
  initial_solution = initial_solution_func(nodes, capacity, algorithm)
  initial_cost = cost_func(initial_solution, nodes)
  print("Initial solution: %s" % initial_solution)
  print("Initial solution cost: %s" % initial_cost)



  print("\n\n############## ALGORITHM RUN OUTPUT ##############\n\n")

  time_acc = 0
  cost_acc = 0
  min_cost = 99999999999999999
  max_cost = 0
  best_solution = initial_solution
  for i in range(times_to_run):
    # run algorithm
    start_time = process_time()
    final_solution = alg_func(nodes, capacity, initial_solution_func)
    end_time = process_time()

    # calculate time and cost
    time_diff = end_time - start_time
    final_cost = cost_func(final_solution, nodes)
    cost_diff_optimal = percent(final_cost, optimal_cost)
    cost_diff_initial = percent(initial_cost, final_cost)

    # accumulate data for statistics
    if final_cost < min_cost:
      best_solution = final_solution
    time_acc += time_diff
    cost_acc += final_cost
    max_cost = max(max_cost, final_cost)
    min_cost = min(min_cost, final_cost)

    print("\n# RUNNING INSTANCE %s #\n" % str(i+1))
    print("Final solution: %s" % final_solution)
    print("Final cost: %d" % final_cost)
    print("This solution costs %.2f percent MORE than the optimal" % cost_diff_optimal)
    print("This solution costs %.2f percent LESS than the initial" % cost_diff_initial)
    print("Took %.3f seconds to execute" % time_diff)


  print("\n\n############## FINAL STATISTICS ##############\n\n")

  average_cost = int(cost_acc / times_to_run)
  average_time = time_acc / times_to_run

  print("The algorithm %s ran for %s times !\n" % (algorithm, times_to_run))
  print("Total execution time: %.3f seconds" % time_acc)
  print("Average execution time: %.3f seconds" % average_time)
  print("Optimal solution cost: %s" % optimal_cost)
  print("Initial solution cost: %s" % initial_cost)
  
  for (analysis, cost) in [("average", average_cost), ("worst", max_cost), ("best", min_cost)]:
    cost_diff_optimal = percent(cost, optimal_cost)
    cost_diff_initial = percent(initial_cost, cost)

    print("\n# %s SOLUTION ANALYSIS #\n" % analysis.upper() )
    print("%s cost: %s" % (analysis, cost) )
    print("The %s solution costs %.2f percent MORE than the OPTIMAL solution" % (analysis, cost_diff_optimal) )
    print("The %s solution costs %.2f percent LESS than the INITIAL solution" % (analysis, cost_diff_initial) )

  print("\nBest solution: %s" % best_solution)

  print("\n\n")
  if PLOT:
    plot.draw_solution(nodes, best_solution, algorithm)


if __name__ == "__main__":
  main()

