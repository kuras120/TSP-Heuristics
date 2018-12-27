from tools.General.SolutionGenerator import *
from tools.Genetic.PopulationCreator import *
from tools.Genetic.Mutation import Mutation, Type as MType
from tools.FileLoader import *
from tools.KBHit import *
import sys
import itertools


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
        self.__solution_in_time = []
        self.__time_line = []

    def calculate(self, iterations, population_size, mutation_type, mutation_reset, cross_type, selection_type,
                  tournament_size=5):

        d_time = time.time()
        population = []
        self.__solution.change_type(Type.Random)
        for i in range(population_size - 1):
            population.append(self.__solution.generate())

        self.__solution.change_type(Type.GreedyOne)
        actual_solution = self.__solution.generate()
        population.append(actual_solution)

        self.__best_route, self.__best_cost, self.__start_best = actual_solution[0], actual_solution[1], actual_solution

        #TEST
        self.__solution_in_time.append(self.__best_cost)
        self.__time_line.append(0)

        self.__mutation.change_type(mutation_type)
        self.__generation.change_method(cross_type)

        for i in range(iterations):
            self.__app_manager()
            self.__radioactivity = 0

            sorted_population = sorted(population, key=lambda x: x[1])
            sorted_population = list(sorted_population for sorted_population, _ in itertools.groupby(sorted_population))
            sorted_population = sorted_population[:population_size]

            self.check_for_best(sorted_population[0])

            # TEST
            self.start_test(i, d_time)

            new_generation = []
            for _ in range(population_size):
                male, female = self.select_parent(population, selection_type, tournament_size)

                first_child, second_child = self.__generation.create(male[0], female[0])

                new_generation.extend([first_child, second_child])

            self.__mutation.mutation_routine(new_generation, self.__radioactivity + 1)

            if self.__mutation.get_mutation_chance() >= mutation_reset:
                population = new_generation
                self.__local_best_cost = sys.maxsize
                self.__mutation.set_mutation_chance(0.05)
            else:
                population = new_generation + sorted_population

        print("\n\n")
        self.print_solution()

    @staticmethod
    def select_parent(population, selection, size):
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
            parent_one, parent_two = random.randrange(population.__len__()), random.randrange(population.__len__())
            group.extend([population[parent_one], population[parent_two]])

        else:
            raise Exception("Cannot find that kind of selection.")

        return group[0], group[1]

    def check_for_best(self, best_person):
        if best_person[1] < self.__local_best_cost:
            self.__local_best_cost = best_person[1]

            print("FOUND LOCAL BEST: " + best_person[0].__str__())
            print("COST: " + best_person[1].__str__())

            # print("Mutation ratio: " + self.__mutation.get_ratio().__str__())

            if best_person[1] < self.__best_cost:
                self.__best_cost = best_person[1]
                self.__best_route = best_person[0]
                self.__radioactivity -= 20
                print("FOUND BEST: " + self.__best_route.__str__())
                print("COST: " + self.__best_cost.__str__())

            self.__radioactivity -= 8

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
        self.__start_best = []
        self.__local_best_cost = sys.maxsize
        self.__radioactivity = 0
        self.__solution_in_time = []
        self.__time_line = []
        self.__mutation.set_mutation_chance(0.001)

    def print_solution(self):
        print("Best route: " + self.__best_route.__str__())
        print("with cost: " + self.__best_cost.__str__())
        print("Start best: " + self.__start_best[0].__str__())
        print("with cost: " + self.__start_best[1].__str__())

    def get_population_number(self):
        return self.__loader.get_number_of_cities()

    def get_solution(self):
        return self.__best_cost, self.__best_route

    def get_solution_in_time(self):
        return self.__solution_in_time, self.__time_line

    def get_data(self):
        return self.__data

    def start_test(self, i, time_t):
        diff = time.time() - time_t
        if (i + 1) % 500 == 0:
            self.__solution_in_time.append(self.__best_cost)
            self.__time_line.append(round(diff, 2))


if __name__ == "__main__":
    alg = Genetic("test/TSP/gr120.tsp", "LOWER_DIAG")
    pop_size = 100
    # Iterations, Population size, Mutation type, Mutation_reset (chance), Cross type, Selection type,
    # Tournament size, Plot number
    alg.calculate(20000, pop_size, MType.Invert, 0.5, Method.OX1, Selection.Tournament, int(pop_size * 0.12))
    sol, time_line = alg.get_solution_in_time()
    print(sol)
    print(time_line)

    # analyze_points = 11
    # tries = 10
    # result = open("test/GA&ACO/GAWyniki2.txt", "w+")
    # result.write("GR120--[500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]--\n")
    # result.write("-------------------GENETIC-OX1-TOURNAMENT-------------------\n")
    # avg_cost = [0] * analyze_points
    # avg_time = [0] * analyze_points
    # for k in range(tries):
    #     alg.calculate(5000, pop_size, MType.Invert, 0.5, Method.OX1, Selection.Tournament, int(pop_size*0.12))
    #     costs, time_line = alg.get_solution_in_time()
    #     for l in range(costs.__len__()):
    #         avg_cost[l] += costs[l]
    #         avg_time[l] += time_line[l]
    #     result.write(costs.__str__() + " " + time_line.__str__() + "\n")
    #     alg.clear_values()
    # result.write("-----------------------------AVG-----------------------------\n")
    # for m in range(avg_cost.__len__()):
    #     avg_cost[m] /= tries
    #     avg_time[m] /= tries
    #
    # for m in range(avg_time.__len__()):
    #     avg_time[m] = round(avg_time[m], 2)
    # result.write(avg_cost.__str__() + " " + avg_time.__str__() + "\n\n")
    # avg_cost = [0] * analyze_points
    # avg_time = [0] * analyze_points
    # result.write("-------------------GENETIC-OX1-RANDOM-------------------\n")
    # for k in range(tries):
    #     alg.calculate(5000, pop_size, MType.Invert, 0.5, Method.OX1, Selection.Random, int(pop_size * 0.12))
    #     costs, time_line = alg.get_solution_in_time()
    #     for l in range(costs.__len__()):
    #         avg_cost[l] += costs[l]
    #         avg_time[l] += time_line[l]
    #     result.write(costs.__str__() + " " + time_line.__str__() + "\n")
    #     alg.clear_values()
    # result.write("-----------------------------AVG-----------------------------\n")
    # for m in range(avg_cost.__len__()):
    #     avg_cost[m] /= tries
    #     avg_time[m] /= tries
    #
    # for m in range(avg_time.__len__()):
    #     avg_time[m] = round(avg_time[m], 2)
    # result.write(avg_cost.__str__() + " " + avg_time.__str__() + "\n\n")
    # avg_cost = [0] * analyze_points
    # avg_time = [0] * analyze_points
    # result.write("-------------------GENETIC-PMX-TOURNAMENT-------------------\n")
    # for k in range(tries):
    #     alg.calculate(5000, pop_size, MType.Invert, 0.5, Method.PMX, Selection.Tournament, int(pop_size * 0.12))
    #     costs, time_line = alg.get_solution_in_time()
    #     for l in range(costs.__len__()):
    #         avg_cost[l] += costs[l]
    #         avg_time[l] += time_line[l]
    #     result.write(costs.__str__() + " " + time_line.__str__() + "\n")
    #     alg.clear_values()
    # result.write("-----------------------------AVG-----------------------------\n")
    # for m in range(avg_cost.__len__()):
    #     avg_cost[m] /= tries
    #     avg_time[m] /= tries
    #
    # for m in range(avg_time.__len__()):
    #     avg_time[m] = round(avg_time[m], 2)
    # result.write(avg_cost.__str__() + " " + avg_time.__str__() + "\n\n")
    # avg_cost = [0] * analyze_points
    # avg_time = [0] * analyze_points
    # result.write("-------------------GENETIC-PMX-RANDOM-------------------\n")
    # for k in range(tries):
    #     alg.calculate(5000, pop_size, MType.Invert, 0.5, Method.PMX, Selection.Random, int(pop_size * 0.12))
    #     costs, time_line = alg.get_solution_in_time()
    #     for l in range(costs.__len__()):
    #         avg_cost[l] += costs[l]
    #         avg_time[l] += time_line[l]
    #     result.write(costs.__str__() + " " + time_line.__str__() + "\n")
    #     alg.clear_values()
    # result.write("-----------------------------AVG-----------------------------\n")
    # for m in range(avg_cost.__len__()):
    #     avg_cost[m] /= tries
    #     avg_time[m] /= tries
    #
    # for m in range(avg_time.__len__()):
    #     avg_time[m] = round(avg_time[m], 2)
    # result.write(avg_cost.__str__() + " " + avg_time.__str__() + "\n\n")
    # avg_cost = [0] * analyze_points
    # avg_time = [0] * analyze_points
    # result.write("-------------------GENETIC-CX-TOURNAMENT-------------------\n")
    # for k in range(tries):
    #     alg.calculate(5000, pop_size, MType.Invert, 0.5, Method.CX, Selection.Tournament, int(pop_size * 0.12))
    #     costs, time_line = alg.get_solution_in_time()
    #     for l in range(costs.__len__()):
    #         avg_cost[l] += costs[l]
    #         avg_time[l] += time_line[l]
    #     result.write(costs.__str__() + " " + time_line.__str__() + "\n")
    #     alg.clear_values()
    # result.write("-----------------------------AVG-----------------------------\n")
    # for m in range(avg_cost.__len__()):
    #     avg_cost[m] /= tries
    #     avg_time[m] /= tries
    #
    # for m in range(avg_time.__len__()):
    #     avg_time[m] = round(avg_time[m], 2)
    # result.write(avg_cost.__str__() + " " + avg_time.__str__() + "\n\n")
    # avg_cost = [0] * analyze_points
    # avg_time = [0] * analyze_points
    # result.write("-------------------GENETIC-CX-RANDOM-------------------\n")
    # for k in range(tries):
    #     alg.calculate(5000, pop_size, MType.Invert, 0.5, Method.CX, Selection.Random, int(pop_size * 0.12))
    #     costs, time_line = alg.get_solution_in_time()
    #     for l in range(costs.__len__()):
    #         avg_cost[l] += costs[l]
    #         avg_time[l] += time_line[l]
    #     result.write(costs.__str__() + " " + time_line.__str__() + "\n")
    #     alg.clear_values()
    # result.write("-----------------------------AVG-----------------------------\n")
    # for m in range(avg_cost.__len__()):
    #     avg_cost[m] /= tries
    #     avg_time[m] /= tries
    #
    # for m in range(avg_time.__len__()):
    #     avg_time[m] = round(avg_time[m], 2)
    # result.write(avg_cost.__str__() + " " + avg_time.__str__() + "\n\n")
    # result.close()
