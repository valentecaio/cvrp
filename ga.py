import random
import math
from pprint import pprint

POPULATION_SIZE = 50
population = []

def initial_population(nodes):
	population = []
	size = len(nodes)
	for _ in range(0,POPULATION_SIZE):
		population.append(random.sample(nodes, size))

def two_opt(route):
     best = route
     improved = True
     while improved:
          improved = False
          for i in range(1, len(route)-2):
               for j in range(i+1, len(route)):
                    if j-i == 1: continue # changes nothing, skip then
                    new_route = route[:]
                    new_route[i:j] = route[j-1:i-1:-1] # this is the 2woptSwap
                    if cost(new_route) < cost(best):
                         best = new_route
                         improved = True
          route = best
     return best

#cycle crossover
def crossover(P1, P2):
	size = len(P1)
	childs = []
	childs.append([None]*size)
	childs.append([None]*size)
	visited = [False]*size
	cycles = []
	positions = []
	pos = 0

	#find all cycles
	while pos >= 0:
		first_gene_P1 = P1[pos]
		cycle = []
		position = []

		while True:
			cycle.append(P1[pos])
			position.append(pos)
			visited[pos] = True

			gene_in_P2 = P2[pos]
			for i in range(0, size):
				if P1[i] == gene_in_P2:
					pos = i
					break
			if P1[pos] == first_gene_P1:
				break #cycle is closed
		# print("cycle= ")
		# pprint(cycle)
		# print("position= ")
		# pprint(position)
		cycles.append(cycle)
		positions.append(position)
	
		#search for next unvisited gene
		start = pos
		pos = -1
		for i in range(start, size):
			if not visited[i]:
				pos = i
				break
		#all cycles have been found if 'visited' vector is all True

	#fill childs with cycle sequence
	for i in range(0,len(positions)):
		position = positions[i]
		idx1 = i%2
		idx2 = abs(idx1 - 1)
		for pos in position:
			childs[idx1][pos] = P1[pos]
			childs[idx2][pos] = P2[pos]

	return childs[0], childs[1]


def apply_mutation(chromosome):
	return chromosome
