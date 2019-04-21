#!/usr/bin/python3

from pprint import pprint
from classes import Client
from cli import parse_args, parse_vrp
import plot

def main():
  algorithm, filepath, verbose, cli_capacity = parse_args()
  depot, clients, vrp_capacity = parse_vrp(filepath)
  capacity = cli_capacity if cli_capacity else vrp_capacity
  print("depot: %s" % depot)
  print("truck capacity: %s" % capacity)
  print("clients:")
  pprint(clients)
  plot.draw_initial_state(depot, clients)


if __name__ == "__main__":
  main()

