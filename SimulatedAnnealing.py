from tools.FileLoader import *
from tools.KBHit import *
from tools.NeighboursGenerator import *
from tools.SolutionGenerator import *
import sys
import random
import math
import time


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

        #Generator rozwiazan
        self.__solution = SolutionGenerator(self.__file, self.__type_t, self.__data)

        #Generator sasiada
        self.__neighbour = NeighboursGenerator(self.__data)

        #Temperatura
        self.__temperature_max = 10000
        self.__temperature = self.__temperature_max
        self.__temperature_list = []
        self.__d = 0

        #Reset
        self.__timer = 0

    def calculate(self, type_t, method, func, iterations):
        self.__solution.change_type(type_t)
        self.__neighbour.change_method(method)

        actual_solution = self.__solution.generate()
        self.__best_route, self.__best_cost, self.__start_best = actual_solution[0], actual_solution[1], actual_solution

        print("Start best: " + actual_solution[0].__str__())
        print("with cost: " + actual_solution[1].__str__())

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

    def calculate_sa_list(self, type_t, method, iterations):
        self.__solution.change_type(type_t)
        self.__neighbour.change_method(method)

        actual_solution = self.create_initial_temperature_list(self.__loader.get_number_of_cities(),
                                                               0.80)
        self.__best_route, self.__best_cost, self.__start_best = actual_solution[0], actual_solution[1], actual_solution

        print("Start best: " + actual_solution[0].__str__())
        print("with cost: " + actual_solution[1].__str__())

        self.__timer = time.time()

        for i in range(1, iterations):
            self.__app_manager()
            if time.time() - self.__timer > self.__loader.get_number_of_cities() / 10:
                self.__temperature_list = []
                self.create_initial_temperature_list(self.__loader.get_number_of_cities(), 0.80)
                self.__timer = time.time()

            self.__temperature_list = sorted(self.__temperature_list, reverse=True)
            temperature_max = self.__temperature_list[0]
            t, c, m = 0, 0, 0
            for j in range(self.__loader.get_number_of_cities()):
                neighbour = self.__neighbour.generate_one(actual_solution[0])
                if neighbour[1] <= actual_solution[1]:
                    actual_solution = neighbour
                    self.check_for_best(actual_solution)
                else:
                    p = math.exp(-(neighbour[1] - actual_solution[1]) / temperature_max)
                    r = random.uniform(0, 0.99)
                    if r < p:
                        t += -(neighbour[1] - actual_solution[1]) / math.log(r, math.e)
                        c += 1
                        actual_solution = neighbour
            if c != 0:
                self.__temperature_list.pop(0)
                self.__temperature_list.append(t / c)

        print("\n\n")
        self.print_solution()

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
        #Temperatura
        self.__temperature_max = 10000
        self.__temperature = self.__temperature_max
        self.__temperature_list = []
        self.__d = 0

        #Reset
        self.__timer = 0

    def print_solution(self):
        print("Best route: " + self.__best_route.__str__())
        print("with cost: " + self.__best_cost.__str__())
        print("Start best: " + self.__start_best[0].__str__())
        print("with cost: " + self.__start_best[1].__str__())

    def get_solution(self):
        return self.__best_cost, self.__best_route

    def get_data(self):
        return self.__data


if __name__ == "__main__":
    annealing = SimulatedAnnealing("test/TSP/gr96.tsp", "COORDS_GEO")
    costs1 = []
    costs2 = []
    costs3 = []
    costs4 = []
    for k in range(10):
        annealing.calculate_sa_list(Type.GreedyOne, Method.Mixed, 250000)
        c, r = annealing.get_solution()
        costs1.append(c)
        annealing.clear_values()
    for k in range(10):
        annealing.calculate(Type.GreedyOne, Method.Mixed, Temperature.Geometric, 250000)
        c, r = annealing.get_solution()
        costs2.append(c)
        annealing.clear_values()
    for k in range(10):
        annealing.calculate(Type.GreedyOne, Method.Mixed, Temperature.Hyperbolic, 250000)
        c, r = annealing.get_solution()
        costs3.append(c)
        annealing.clear_values()
    for k in range(10):
        annealing.calculate(Type.GreedyOne, Method.Mixed, Temperature.Exponential, 250000)
        c, r = annealing.get_solution()
        costs4.append(c)
        annealing.clear_values()

    print("Wyniki dla mixed list")
    srednia = 0
    for elem in costs1:
        srednia += elem
        print(elem)
    print("Srednia: " + (srednia/10).__str__())
    print("Wyniki dla mixed geometric")
    srednia = 0
    for elem in costs2:
        srednia += elem
        print(elem)
    print("Srednia: " + (srednia/10).__str__())
    print("Wyniki dla mixed hyperbolic")
    srednia = 0
    for elem in costs3:
        srednia += elem
        print(elem)
    print("Srednia: " + (srednia/10).__str__())
    print("Wyniki dla mixed exponential")
    srednia = 0
    for elem in costs4:
        srednia += elem
        print(elem)
    print("Srednia: " + (srednia/10).__str__())