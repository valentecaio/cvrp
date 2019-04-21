#!/usr/bin/python3

import argparse
from pprint import pprint
from classes import Client
from cli import parse_args, parse_vrp

def main():
  algorithm, filepath, verbose = parse_args()
  depot, clients = parse_vrp(filepath)
  print("depot: %s" % depot)
  print("clients:")
  pprint(clients)


if __name__ == "__main__":
  main()

