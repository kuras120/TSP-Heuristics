from FileLoader import FileLoader
from msvcrt import getch, kbhit
from tools.NeighboursGenerator import *
from tools.SolutionGenerator import *
import sys
import random
import math
import time


class SimulatedAnnealing:
    def __init__(self, file, type_t):
        self.__loader = FileLoader()
        self.__loader.load(file, type_t)

        self.__file = file
        self.__type_t = type_t

        self.__data = self.__loader.get_data()
        self.__best_route = []
        self.__best_cost = sys.maxsize
        self.__start_best = [None, None]

        #Generator rozwiazan
        self.__solution = SolutionGenerator(self.__file, self.__type_t, self.__data)

        #Generator sasiada
        self.neighbour = NeighboursGenerator(self.__data)

        #Szacowanie
        self.__previous_cost = self.__best_cost
        self.__cost_difference = 0

    def calculate(self, type_t, method, iterations):
        self.__solution.change_type(type_t)
        self.neighbour.change_method(method)

        route = self.__solution.generate()
        self.__best_route, self.__best_cost, self.__start_best = route[0], route[1], route
        best_neighbour = route
        temperature = 0.8

        print("Start best: " + route[0].__str__())
        print("with cost: " + route[1].__str__())
        for i in range(iterations):
            self.__app_manager()
            for j in range(2, self.__loader.get_number_of_cities()):
                neighbour = self.neighbour.generate_one(route[0])
                self.__previous_cost = best_neighbour[1]
                best_neighbour = neighbour
                print("SOMSIAD: " + best_neighbour.__str__())
                self.check_for_best(best_neighbour)
                self.__cost_difference = best_neighbour[1] - self.__previous_cost
                if self.__cost_difference < 0:
                    route = best_neighbour
                else:
                    x = random.uniform(0, 1)
                    if x < math.exp(-self.__cost_difference / temperature):
                        route = best_neighbour

            temperature = (0.5 * math.sin(i*0.01 + (4 * math.pi) / 5)) + 0.5
        print("\n\n")
        self.print_solution()

    def check_for_best(self, best_neighbour):
        if best_neighbour[1] < self.__best_cost:
            self.__best_cost = best_neighbour[1]
            self.__best_route = best_neighbour[0]

            print("FOUND: " + self.__best_route.__str__())
            print("COST: " + self.__best_cost.__str__())

    def __app_manager(self):
        if kbhit():
            key = ord(getch())
            if key == 32:
                print("Program paused")
                self.print_solution()
                while True:
                    key = ord(getch())
                    if key == 32:
                        print("Program resumed")
                        break
                    elif key == 27:
                        print("Program stopped")
                        self.print_solution()
                        exit(0)
            elif key == 27:
                print("Program stopped")
                self.print_solution()
                exit(0)

    def clear_values(self):
        self.__best_route = []
        self.__best_cost = sys.maxsize
        self.__start_best = [None, None]

        self.__previous_cost = self.__best_cost
        self.__cost_difference = 0

    def print_solution(self):
        print("Best route: " + self.__best_route.__str__())
        print("with cost: " + self.__best_cost.__str__())
        print("Start best: " + self.__start_best[0].__str__())
        print("with cost: " + self.__start_best[1].__str__())

    def get_solution(self):
        return self.__best_cost, self.__best_route


if __name__ == "__main__":
    annealing = SimulatedAnnealing("test/TSP/gr48.tsp", "LOWER_DIAG")
    annealing.calculate(Type.Random, Method.Invert, 100000)
