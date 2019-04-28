from pprint import pprint

#### DEBUG CONSTANTS ####

VERBOSE = False     # enable logs
PLOT = True         # enable plot

#### ANNEALING CONSTANTS ####

INITIAL_TEMP = 20
FINAL_TEMP = 1      # stop condition
T_FACTOR = 0.9      # decreasing temperature by (1 - T_FACTOR)
N_FACTOR = 0.9      # neighborhood ratio factor

#### LOCAL SEARCH CONSTANTS ####

LOOP_LIMIT = 500
RANDOM_START = 20

#### MODULE FUNCTIONS ####

def print_constants():
  const = {
    "INITIAL_TEMP": INITIAL_TEMP,
    "FINAL_TEMP": FINAL_TEMP,
    "T_FACTOR": T_FACTOR,
    "N_FACTOR": N_FACTOR
  }
  print("Constants:")
  pprint(const)
  print("\n")


if __name__ == "__main__":
  print_constants()

