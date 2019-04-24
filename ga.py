import random
import math


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
	cycles = []
	pos = 0

	first_gene_P1 = P1[pos]
	cycle = []
	while True:
		cycle.append(P1[pos])
		gene_in_P2 = P2[pos]
		for i in range(0, len(P1)):
			if P1[i] == gene_in_P2:
				pos = i
				break
		if P1[pos] == first_gene_P1:
			break



def apply_mutation(chromosome):
	return chromosome
