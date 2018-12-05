from tools.General.SolutionGenerator import *
from tools.Genetic.PopulationCreator import *
from tools.Genetic.Mutation import Mutation, Type as MType
from tools.FileLoader import *
from tools.KBHit import *
import sys
import time


class Selection(Enum):
    Tournament = 0
    Random = 1


class Genetic:
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

        self.__local_best_cost = sys.maxsize

        self.__solution = SolutionGenerator(self.__file, self.__type_t, self.__data)
        self.__generation = PopulationCreator(self.__data)
        self.__mutation = Mutation(self.__data)

        self.__radioactivity = 0
        self.__timer = 0

    def calculate(self, iterations, tournament_size, population_size, selection_type):
        population = []
        self.__solution.change_type(Type.GreedyOne)
        actual_solution = self.__solution.generate()
        self.__best_route, self.__best_cost, self.__start_best = actual_solution[0], actual_solution[1], actual_solution

        print("Start best: " + actual_solution[0].__str__())
        print("with cost: " + actual_solution[1].__str__())

        self.__solution.change_type(Type.Random)

        for i in range(population_size):
            population.append(self.__solution.generate())

        self.__timer = time.time()
        for i in range(iterations):
            self.__app_manager()
            self.__radioactivity = 0

            sorted_population = sorted(population, key=lambda x: x[1])
            sorted_population = sorted_population[:population_size]

            self.check_for_best(sorted_population[0])

            # print("Best human in the world: " + sorted_population[0].__str__())

            new_generation = []
            for _ in range(population_size):
                male = self.select_parent(population, tournament_size, selection_type)
                female = self.select_parent(population, tournament_size, selection_type)

                first_child, second_child = self.__generation.create(male[0], female[0])
                new_generation.extend([first_child, second_child])

            self.__mutation.mutation_routine(new_generation, self.__radioactivity + 1)

            if time.time() - self.__timer > population_size/12:
                population = sorted(new_generation, key=lambda x: x[1])
                self.__local_best_cost = population[0][1]
                self.__timer = time.time()
            else:
                population = \
                    new_generation + sorted_population[:int(population_size/4)]

        print("\n\n")
        self.print_solution()

    @staticmethod
    def select_parent(population, size, selection):
        group = []
        if selection == Selection.Tournament:
            index = []
            while index.__len__() < size:
                rand = random.randrange(population.__len__())
                if rand not in index:
                    index.append(rand)
                    group.append(population[rand])

            group.sort(key=lambda x: x[1])

        elif selection == Selection.Random:
            parent_one = random.randrange(population.__len__())
            group.append(population[parent_one])

        else:
            raise Exception("Cannot find that kind of selection.")

        return group[0]

    def check_for_best(self, best_person):
        if best_person[1] < self.__local_best_cost:
            self.__local_best_cost = best_person[1]

            print("FOUND LOCAL BEST: " + best_person[0].__str__())
            print("COST: " + best_person[1].__str__())

            print("Mutation ratio: " + self.__mutation.get_ratio().__str__())

            if best_person[1] < self.__best_cost:
                self.__best_cost = best_person[1]
                self.__best_route = best_person[0]
                self.__radioactivity -= 100
                print("FOUND BEST: " + self.__best_route.__str__())
                print("COST: " + self.__best_cost.__str__())

            self.__radioactivity -= 50
            self.__timer = time.time()

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

    def print_solution(self):
        print("Best route: " + self.__best_route.__str__())
        print("with cost: " + self.__best_cost.__str__())
        print("Start best: " + self.__start_best[0].__str__())
        print("with cost: " + self.__start_best[1].__str__())

    def get_population_number(self):
        return self.__loader.get_number_of_cities()

    def get_solution(self):
        return self.__best_cost, self.__best_route

    def get_data(self):
        return self.__data


if __name__ == "__main__":
    alg = Genetic("test/TSP/gr202.tsp", "COORDS_GEO")
    pop_size = 75
    alg.calculate(100000, int(5*pop_size/16), pop_size, Selection.Tournament)
