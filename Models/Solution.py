class Solution:
    def __init__(self, genom, map):
        self.genom = genom
        self.map = map
        self.recount()


    def __str__(self):
        return 'Worth: ' + str(self.worth)

    def recount(self):
        result_worth = 0
        for i in range(len(self.genom) - 1):
            result_worth += self.map[self.genom[i]][self.genom[i + 1]]
        result_worth += self.map[self.genom[-1]][self.genom[0]]
        self.worth = result_worth