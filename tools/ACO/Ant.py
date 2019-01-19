import time

from tools.General.SolutionGenerator import *


class Ant:
    def __init__(self, maps):
        self.__tour = []
        self.__cost = 0
        self.__maps = maps
        self.__unvisited = list(range(maps.__len__()))

    def move(self, start, alpha, beta):
        self.__tour.append(start)
        self.__unvisited.remove(start)

        current_row = start
        while self.__unvisited.__len__() > 0:
            pheromone_sum = 0
            probability = []

            for place in self.__unvisited:
                cost = pow(1 / self.__maps[current_row][place][0], alpha)
                pheromone = pow(self.__maps[current_row][place][1], beta)
                probability.append(cost * pheromone)
                pheromone_sum += cost * pheromone

            for i in range(probability.__len__()):
                probability[i] /= pheromone_sum

            chosen = random.choices(self.__unvisited, probability)
            self.__cost += self.__maps[self.__tour[-1]][chosen[0]][0]
            self.__tour.append(chosen[0])
            self.__unvisited.remove(chosen[0])

            current_row = chosen[0]

        self.__cost += self.__maps[self.__tour[-1]][self.__tour[0]][0]
        self.__tour.append(self.__tour[0])

    def leave_pheromones(self, maps):
        pheromones_amount = 100 / self.__cost
        for i in range(1, self.__tour.__len__()):
            maps[self.__tour[i - 1]][self.__tour[i]][1] += pheromones_amount
        return maps

    def get_solution(self):
        return [self.__tour, self.__cost]


if __name__ == "__main__":
    file_t = FileLoader()
    file_t.load("../../test/TSP/gr48.tsp", "LOWER_DIAG")
    ant_map = file_t.get_data()
    for outer in range(file_t.get_number_of_cities()):
        for inner in range(file_t.get_number_of_cities()):
            ant_map[outer][inner] = [ant_map[outer][inner], 1]

    sol = SolutionGenerator("../../test/TSP/gr48.tsp", "LOWER_DIAG")
    sol.change_type(Type.GreedyOne)
    grdy_sol = sol.generate()

    ant_route, ant_cost = [], 0
    time_t = time.time()
    for _ in range(62500):
        ant_t = Ant(ant_map)
        ant_t.move(grdy_sol[0][0], 5, 1)
    # ant_route, ant_cost = ant_t.get_solution()
    # ant_map = ant_t.leave_pheromones(ant_map)
    time_t = time.time() - time_t
    # print("Solution: " + ant_route.__str__() + " " + ant_cost.__str__())
    print("Time: " + time_t.__str__())
