from tools.FileLoader import *
from tools.KBHit import *
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

        self.__keyboard = KBHit()

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

        #Reset
        self.__timer = 0

    def calculate(self, type_t, method, iterations):
        self.__solution.change_type(type_t)
        self.neighbour.change_method(method)

        actual_solution = self.__solution.generate()
        self.__best_route, self.__best_cost, self.__start_best = actual_solution[0], actual_solution[1], actual_solution

        print("Start best: " + actual_solution[0].__str__())
        print("with cost: " + actual_solution[1].__str__())

        self.__timer = time.time()

        for i in range(iterations):
            self.__app_manager()
            if time.time() - self.__timer > self.__loader.get_number_of_cities() / 8:
                self.__solution.change_type(Type.Random)
                actual_solution = self.__solution.generate()
            temperature = (4999 * math.sin(2 * math.pi * i * 0.001 + (math.pi / 2))) + 5001
            for j in range(self.__loader.get_number_of_cities()):
                neighbour = self.neighbour.generate_one(actual_solution[0])
                previous_cost = actual_solution[1]
                # print("NEIGHBOUR: " + neighbour.__str__())
                cost_difference = neighbour[1] - previous_cost
                if cost_difference <= 0:
                    self.check_for_best(actual_solution)
                    actual_solution = neighbour
                else:
                    x = random.uniform(0, 1)
                    if x < math.exp(-cost_difference / temperature):
                        actual_solution = neighbour

            # print(temperature)
        print("\n\n")
        self.print_solution()

    def check_for_best(self, best_neighbour):
        if best_neighbour[1] < self.__best_cost:
            self.__best_cost = best_neighbour[1]
            self.__best_route = best_neighbour[0]

            self.__timer = time.time()

            print("FOUND: " + self.__best_route.__str__())
            print("COST: " + self.__best_cost.__str__())

    def __app_manager(self):
        if self.__keyboard.kbhit():
            key = ord(self.__keyboard.getch())
            if key == 32:
                print("Program paused")
                self.print_solution()
                while True:
                    key = ord(self.__keyboard.getch())
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
    annealing.calculate(Type.GreedyOne, Method.Invert, 100000)
