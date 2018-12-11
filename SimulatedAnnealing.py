from tools.FileLoader import *
from tools.KBHit import *
from tools.General.NeighboursGenerator import *
from tools.General.SolutionGenerator import *
import sys
import random
import math
import time
import matplotlib.pyplot as plt


class Temperature(Enum):
    Geometric = 0
    Exponential = 1
    Logarithmic = 2
    Arithmetic = 3
    Sinusoid = 4
    Hyperbolic = 5


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

        # Generator rozwiazan
        self.__solution = SolutionGenerator(self.__file, self.__type_t, self.__data)

        # Generator sasiada
        self.__neighbour = NeighboursGenerator(self.__data)

        # Temperatura
        self.__temperature_max = 10000
        self.__temperature = self.__temperature_max
        self.__temperature_list = []
        self.__d = 0

        # Reset
        self.__timer = 0

        # TEST
        self.__min = sys.maxsize
        self.__max = 0

    def calculate(self, type_t, method, func, iterations):
        print("Starting...")

        self.__solution.change_type(type_t)
        self.__neighbour.change_method(method)

        actual_solution = self.__solution.generate()
        self.__best_route, self.__best_cost, self.__start_best = actual_solution[0], actual_solution[1], actual_solution

        print("Start best: " + actual_solution[0].__str__())
        print("with cost: " + actual_solution[1].__str__())

        print("Algorithm has been started.")
        self.__timer = time.time()

        for i in range(1, iterations):
            self.__app_manager()
            if time.time() - self.__timer > self.__loader.get_number_of_cities() / 10:
                self.__solution.change_type(Type.GreedyOne)
                actual_solution = self.__solution.generate()
                self.__timer = time.time()

            temperature = self.temperature(func, i)

            for j in range(self.__loader.get_number_of_cities()):
                neighbour = self.__neighbour.generate_one(actual_solution[0])

                # print("NEIGHBOUR: " + neighbour.__str__())

                previous_cost = actual_solution[1]
                cost_difference = neighbour[1] - previous_cost
                if cost_difference <= 0:
                    self.check_for_best(actual_solution)
                    actual_solution = neighbour
                else:
                    x = random.uniform(0, 1)
                    if x < math.exp(-cost_difference / temperature):
                        actual_solution = neighbour

        print("\n\n")
        self.print_solution()

    def calculate_sa_list(self, type_t, method, init_temp, temp_list_length, iterations):
        print("Starting...\n")

        self.__solution.change_type(type_t)
        self.__neighbour.change_method(method)

        actual_solution = self.create_initial_temperature_list(temp_list_length, init_temp)
        self.__best_route, self.__best_cost, self.__start_best = actual_solution[0], actual_solution[1], actual_solution

        print("Start best: " + actual_solution[0].__str__())
        print("with cost: " + actual_solution[1].__str__())

        print("\nAlgorithm has been started.\n")
        self.__timer = time.time()

        for i in range(1, iterations):
            self.__app_manager()

            if time.time() - self.__timer > self.__loader.get_number_of_cities() / 15:
                self.__temperature_list = []
                self.create_initial_temperature_list(temp_list_length, init_temp)
                self.__timer = time.time()

            self.__temperature_list = sorted(self.__temperature_list, reverse=True)
            temperature_max = self.__temperature_list[0]
            t, c = 0, 0
            for j in range(self.__loader.get_number_of_cities()):
                neighbour = self.__neighbour.generate_one(actual_solution[0])

                # print("NEIGHBOUR: " + neighbour.__str__())

                if neighbour[1] <= actual_solution[1]:
                    actual_solution = neighbour
                    self.check_for_best(actual_solution)
                else:
                    p = math.exp(-(neighbour[1] - actual_solution[1]) / temperature_max)
                    if p > self.__max:
                        self.__max = p
                    if p < self.__min:
                        self.__min = p
                    r = random.uniform(0, 0.99)
                    if r < p:
                        t = -(neighbour[1] - actual_solution[1]) / math.log(r, math.e)
                        c += 1
                        actual_solution = neighbour
            if c != 0:
                self.__temperature_list.pop(0)
                self.__temperature_list.append(t / c)

        print("\n\n")
        self.print_solution()
        print("Min: " + self.__min.__str__() + " Max: " + self.__max.__str__())

    def create_initial_temperature_list(self, max_length, initial_probability):
        route = self.__solution.generate()

        while self.__temperature_list.__len__() < max_length:
            neighbour = self.__neighbour.generate_one(route[0])
            if neighbour[1] < route[1]:
                route = neighbour
                self.check_for_best(route)

            temperature = -abs(neighbour[1] - route[1]) / math.log(initial_probability, math.e)
            if neighbour[1] - route[1] != 0:
                self.__temperature_list.append(int(temperature))

        return route

    def temperature(self, func, i):
        if func == Temperature.Sinusoid:
            return round((4999 * math.sin(2 * math.pi * i * 0.0005 + (math.pi / 2))) + 5001, 4)
        elif func == Temperature.Hyperbolic:
            temperature = self.__temperature_max/(i - self.__d)
            if temperature < 2:
                self.__d = i
            return round(temperature, 4)
        elif func == Temperature.Exponential:
            temperature = math.pow(math.e, -i/100 + (self.__d/100)) * self.__temperature_max
            if temperature < 1:
                self.__d = i
            return round(temperature, 4)
        elif func == Temperature.Geometric:
            self.__temperature = self.__temperature/2
            if self.__temperature <= 0:
                self.__temperature = self.__temperature_max
            return self.__temperature
        elif func == Temperature.Arithmetic:
            self.__temperature -= 1.6
            if self.__temperature <= 0:
                self.__temperature = self.__temperature_max
            return self.__temperature

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
                print("\nProgram paused\n")
                self.print_solution()
                while True:
                    key = ord(self.__keyboard.getch())
                    if key == 32:
                        print("\nProgram resumed\n")
                        break
                    elif key == 27:
                        print("\nProgram stopped\n")
                        self.print_solution()
                        exit(0)
            elif key == 27:
                print("\nProgram stopped\n")
                self.print_solution()
                exit(0)

    def clear_values(self):
        self.__best_route = []
        self.__best_cost = sys.maxsize
        self.__start_best = [None, None]
        # Temperatura
        self.__temperature_max = 10000
        self.__temperature = self.__temperature_max
        self.__temperature_list = []
        self.__d = 0

        # Reset
        self.__timer = 0

    def print_solution(self):
        print("Best route: " + self.__best_route.__str__())
        print("with cost: " + self.__best_cost.__str__())
        print("Start best: " + self.__start_best[0].__str__())
        print("with cost: " + self.__start_best[1].__str__())

        statistics = self.get_stats()
        everythin = sum(statistics)

        print("SWAP: " + round(statistics[0] / everythin, 2).__str__())
        print("INSERT: " + round(statistics[1] / everythin, 2).__str__())
        print("INVERT: " + round(statistics[2] / everythin, 2).__str__())

    def get_solution(self):
        return self.__best_cost, self.__best_route

    def get_data(self):
        return self.__data

    def get_stats(self):
        return self.__neighbour.get_statistics()


if __name__ == "__main__":
    annealing = SimulatedAnnealing("test/TSP/pr152.tsp", "COORDS_EUC")
    # TYPE: GREEDY/GREEDY ONE/RANDOM
    # METHOD: INVERT/INSERT/SWAP/MIXED
    # TEMPERATURE: GEOMETRIC/EXPONENTIAL/SINUSOID/ARITHMETIC/LENGTH OF LIST
    # ITERATIONS: NUMBER
    tm = time.time()
    annealing.calculate_sa_list(Type.GreedyOne, Method.Mixed, 0.49, 120, 25000)
    # annealing.calculate(Type.GreedyOne, Method.Mixed, Temperature.Geometric, 25000)
    tm = time.time() - tm
    print("Processing time: " + tm.__str__())
