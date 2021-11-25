class Population:
    def __init__(self, solutions):
        self.solutions = solutions
        self.best_worth = min([x.worth for x in self.solutions])
        self.best_solution = solutions[[x.worth for x in self.solutions].index(self.best_worth)]

    def add(self, solution):
        self.solutions.append(solution)
        self.solutions.pop([x.worth for x in self.solutions].index(max([x.worth for x in self.solutions])))