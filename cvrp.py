#!/usr/bin/python3

from pprint import pprint
from time import process_time
from constants import print_constants, PLOT
import initial_solution_generator
import parser
import annealing
import local_search
try:
  import plot
except ImportError:
  global PLOT
  PLOT = False

### DEBUG FUNCTIONS ###

def print_nodes(nodes):
  print("Nodes:")
  pprint(nodes)

def print_solution(header, solution):
  try:
    int(solution[0])
    print("%s: %s" % (header, solution) )
  except TypeError:
    print("%s:" % header)
    pprint(solution)

def percent(a, b):
  return 100 * (a - b) / a


### MAIN ###

def main():
  # get and handle different inputs
  algorithm, initial_solution_algorithm, filepath, cli_capacity, times_to_run, learn = parser.parse_cli_args()
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
  print("learn: %s" % learn)
  print("optimal solution cost: %s\n" % optimal_cost)
  print_constants()
  print_nodes(nodes)



  print("\n\n############## INITIAL SOLUTION ##############\n\n")

  # generate initial solution
  initial_solution = initial_solution_func(nodes, capacity, algorithm)
  initial_cost = cost_func(initial_solution, nodes)
  print_solution("Initial solution:", initial_solution)
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
    if learn:
      final_solution = alg_func(nodes, capacity, initial_solution = best_solution)
    else:
      final_solution = alg_func(nodes, capacity, initial_solution_func = initial_solution_func)
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
    print_solution("Final solution:", final_solution)
    print("Final solution cost: %d" % final_cost)
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

  print_solution("\nBest solution:", best_solution)

  print("\n\n")
  if PLOT:
    plot.draw_solution(nodes, best_solution, algorithm)


def run_n_times_and_get_average_and_best_solutions(nodes, capacity, initial_solution, initial_cost, times_to_run, optimal_cost, init_t, t_factor, n_factor):
  time_acc = 0
  cost_acc = 0
  min_cost = 99999999999999999
  max_cost = 0
  best_time = 0
  for i in range(times_to_run):
    # run algorithm
    start_time = process_time()
    final_solution = annealing.annealing(nodes, capacity, init_t, t_factor, n_factor, initial_solution = initial_solution)
    end_time = process_time()

    # calculate time and cost
    time_diff = end_time - start_time
    final_cost = annealing.solution_cost(final_solution, nodes)
    cost_diff_optimal = percent(final_cost, optimal_cost)
    cost_diff_initial = percent(initial_cost, final_cost)

    # accumulate data for statistics
    if final_cost < min_cost:
      best_solution = final_solution
      best_time = time_diff
    time_acc += time_diff
    cost_acc += final_cost
    max_cost = max(max_cost, final_cost)
    min_cost = min(min_cost, final_cost)

  print("\n\n############## FINAL STATISTICS ##############\n\n")

  average_cost = int(cost_acc / times_to_run)
  average_time = time_acc / times_to_run

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

  print_solution("\nBest solution:", best_solution)
  return {
    "best": {
      "solution": best_solution,
      "cost": min_cost,
      "execution time": best_time,
      "diff to optimal": percent(min_cost, optimal_cost),
      "diff to initial": percent(initial_cost, min_cost),
      "initial_temp": init_t,
      "t_factor": t_factor,
      "n_factor": n_factor
    },
    "average": {
      "cost": average_cost,
      "execution time": average_time,
      "diff to optimal": percent(average_cost, optimal_cost),
      "diff to initial": percent(initial_cost, average_cost),
      "initial_temp": init_t,
      "t_factor": t_factor,
      "n_factor": n_factor
    }
  }


def find_best_parameters():
  # get and handle different inputs
  algorithm, initial_solution_algorithm, filepath, cli_capacity, times_to_run, learn = parser.parse_cli_args()
  nodes, vrp_capacity = parser.parse_vrp(filepath)
  optimal_cost = parser.get_optimal_cost(filepath)
  capacity = cli_capacity if cli_capacity else vrp_capacity

  initial_solution = initial_solution_generator.greedy(nodes, capacity, 'annealing')
  initial_cost = annealing.solution_cost(initial_solution, nodes)

  print("\n\n############## INPUT ##############\n\n")

  print("algorithm: %s" % algorithm)
  print("initial solution algorithm: %s" % initial_solution_algorithm)
  print("truck capacity: %s" % capacity)
  print("filepath: %s" % filepath)
  print("learn: %s" % learn)
  print("optimal solution cost: %s\n" % optimal_cost)
  print("initial solution cost: %s\n" % initial_cost)
  print_constants()
  print_nodes(nodes)

  # init accumulators:
  results = {
    "best": {
      "solution": initial_solution,
      "cost": initial_cost,
      "execution time": 0,
      "diff to optimal": percent(initial_cost, optimal_cost),
      "diff to initial": 0,
      "initial_temp": 0,
      "t_factor": 0,
      "n_factor": 0
    },
    "average": {
      "cost": initial_cost,
      "execution time": 0,
      "diff to optimal": percent(initial_cost, optimal_cost),
      "diff to initial": 0,
      "initial_temp": 0,
      "t_factor": 0,
      "n_factor": 0
    }
  }
  all_results = [results]
  pprint(results)


  # start loopings changing parameters values
  # initial_temp_values = [10, 20]
  # t_factor_values = [0.1, 0.3]
  # n_factor_values = [0.1, 0.3]
  initial_temp_values = [10, 20, 100, 200]
  t_factor_values = [0.1, 0.3, 0.5, 0.7, 0.9, 0.95]
  n_factor_values = [0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.98]
  for init_t in initial_temp_values:
    for t_factor in t_factor_values:
      for n_factor in n_factor_values:
        print("\n\n############## STARTED TO RUN ALGORITHM ##############\n\n")
        print("\nRunning with (%s, %s, %s)..." % (init_t, t_factor, n_factor))

        new_results = run_n_times_and_get_average_and_best_solutions(nodes, capacity, initial_solution, initial_cost, times_to_run, optimal_cost, init_t, t_factor, n_factor)

        print("\n\n############## FINISHED ##############\n\n")

        # update best "best cost" and best "average cost"
        if(new_results["best"]["cost"] < results["best"]["cost"]):
          results["best"] = new_results["best"]
        if(new_results["average"]["cost"] < results["average"]["cost"]):
          results["average"] = new_results["average"]

        # accumulate results
        all_results.append(new_results)

        # print best results in real time
        print(results)

  plot.draw_solution(nodes, results["best"]["solution"], 'annealing')
  parser.write_csv(filepath, optimal_cost, results["best"], results["average"], all_results)



if __name__ == "__main__":
  main()
  # find_best_parameters()
