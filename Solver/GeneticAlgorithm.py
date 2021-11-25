import numpy as np
from Models.Solution import Solution


class GeneticAlgorithm:
    def __init__(self, initial_population, iterations, mutation_chance, crossbreeding_method, mutation_method, local_upgrade_method):
        self.population = initial_population
        self.iterations = iterations
        self.mutation_chance = mutation_chance
        self.crossbreeding_method = crossbreeding_method
        self.mutation_method = mutation_method
        self.local_upgrade_method = local_upgrade_method

    def solve(self):
        for i in range(self.iterations):
            parents = GeneticAlgorithm.get_parents(self.population)

            new_child = None
            if self.crossbreeding_method == 'onepoint':
                new_child = GeneticAlgorithm.get_child_onepoint(*parents)
            elif self.crossbreeding_method == 'twopoint':
                new_child = GeneticAlgorithm.get_child_twopoint(*parents)
            elif self.crossbreeding_method == 'threepoint':
                new_child = GeneticAlgorithm.get_child_threepoint(*parents)

            if np.random.choice([True, False], p=[self.mutation_chance, 1 - self.mutation_chance]):
                if self.mutation_method == 'onepoint':
                    new_child = GeneticAlgorithm.get_mutated_onepoint(new_child)
                elif self.mutation_method == 'twopoint':
                    new_child = GeneticAlgorithm.get_mutated_twopoint(new_child)
            if self.mutation_method == '1':
                new_child = GeneticAlgorithm.local_upgrade_1(new_child)
            elif self.mutation_method == '2':
                new_child = GeneticAlgorithm.local_upgrade_2(new_child)

            if new_child.worth < self.population.best_worth:
                self.population.best_worth = new_child.worth
                self.population.best_solution = new_child

            self.population.add(new_child)

            print(self.population.best_worth)

    def get_solution(self):
        return self.population.best_backpack

    @staticmethod
    def get_parents(population):
        total_population_worth = sum([x.worth for x in population.solutions])
        return tuple(np.random.choice(population.solutions, size=2, replace=False,
                                      p=[x.worth / total_population_worth for x in population.solutions]))

    @staticmethod
    def get_child_twopoint(parent1, parent2):
        point1 = np.random.choice(range(len(parent1.genom) - 2))
        point2 = np.random.choice(range(point1 + 1, len(parent1.genom)))
        new_genom = [-1]*len(parent1.genom)
        new_genom[:point1] = parent1.genom[:point1]
        unvisited = [x for x in parent2.genom if x not in new_genom]
        new_genom[point1:point2] = unvisited[0:point2 - point1]
        unvisited = [x for x in parent1.genom if x not in new_genom]
        new_genom[point2:] = unvisited
        return Solution(new_genom, parent2.map)

    @staticmethod
    def get_child_onepoint(parent1, parent2):
        point1 = np.random.choice(range(len(parent1.genom) - 2))
        new_genom = [-1] * len(parent1.genom)
        new_genom[:point1] = parent1.genom[:point1]
        unvisited = [x for x in parent2.genom if x not in new_genom]
        new_genom[point1:] = unvisited
        return Solution(new_genom, parent2.map)

    @staticmethod
    def get_child_threepoint(parent1, parent2):
        point1 = np.random.choice(range(len(parent1.genom) - 3))
        point2 = np.random.choice(range(point1 + 1, len(parent1.genom) - 2))
        point3 = np.random.choice(range(point2 + 1, len(parent2.genom)))
        new_genom = [-1] * len(parent1.genom)
        new_genom[:point1] = parent1.genom[:point1]
        unvisited = [x for x in parent2.genom if x not in new_genom]
        new_genom[point1:point2] = unvisited[0:point2 - point1]
        unvisited = [x for x in parent1.genom if x not in new_genom]
        new_genom[point2:point3] = unvisited[0:point3 - point2]
        unvisited = [x for x in parent2.genom if x not in new_genom]
        new_genom[point3:] = unvisited
        return Solution(new_genom, parent2.map)


    @staticmethod
    def get_mutated_onepoint(solution):
        points = np.random.choice(len(solution.genom), size=2, replace=False)
        solution.genom[points[0]], solution.genom[points[1]] = solution.genom[points[1]], solution.genom[points[0]]
        solution.recount()
        return solution

    @staticmethod
    def get_mutated_twopoint(solution):
        points = np.random.choice(len(solution.genom), size=4, replace=False)
        solution.genom[points[0]], solution.genom[points[1]] = solution.genom[points[1]], solution.genom[points[0]]
        solution.genom[points[2]], solution.genom[points[3]] = solution.genom[points[3]], solution.genom[points[2]]
        solution.recount()
        return solution

    @staticmethod
    def local_upgrade_1(solution):
        start_solution = Solution(solution.genom, solution.map)
        iterations = 0
        while solution.worth >= start_solution.worth and iterations < 50:
            solution = GeneticAlgorithm.get_mutated_onepoint(solution)
        return solution if solution.worth > start_solution.worth else start_solution

    @staticmethod
    def local_upgrade_2(solution):
        start_solution = Solution(solution.genom, solution.map)
        iterations = 0
        while solution.worth >= start_solution.worth and iterations < 50:
            solution = GeneticAlgorithm.get_mutated_twopoint(solution)
        return solution if solution.worth > start_solution.worth else start_solution
