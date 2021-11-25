from Models.Solution import Solution
from Models.Population import Population
from Solver.GeneticAlgorithm import GeneticAlgorithm
import random
import numpy as np
import sys
sys.stdout = open('output.txt', 'w')

m = []
for i in range(300):
    row = [0]*300
    for j in range(300):
        if j > i:
            row[j] = random.randint(5, 150)
    m.append(row)

for i in range(300):
    for j in range(300):
        if i > j:
            m[i][j] = m[j][i]

population = Population([Solution(np.random.permutation(300), m) for _ in range(100)])


for crossbreeding_method in ['onepoint', 'twopoint', 'threepoint']:
    for mutation_method in ['onepoint', 'twopoint']:
        for local_upgrade_method in ['1', '2']:
            ga = GeneticAlgorithm(population, 500, 0.2, crossbreeding_method, mutation_method, local_upgrade_method)
            ga.solve()
            print('for crossbreeding method = ' + crossbreeding_method + '\nmutation method = ' + mutation_method + '\nlocal upgrade method = ' + local_upgrade_method)
            print('result = ' + ga.population.best_solution.__str__())