import time
import sys

from matplotlib import pyplot as plt

from tools.General.SolutionGenerator import *
from tools.Genetic.Mutation import Mutation, Type as MType
from tools.Genetic.PopulationCreator import *
from tools.KBHit import *


class Selection(Enum):
    Tournament = 0
    RouletteWheel = 1


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
        self.__start_best = []

        self.__local_best_cost = sys.maxsize

        self.__solution = SolutionGenerator(self.__file, self.__type_t, self.__data)
        self.__generation = PopulationCreator(self.__data)
        self.__mutation = Mutation(self.__data)

        self.__radioactivity = 0
        self.__solution_in_time = []
        self.__time_line = []

    def calculate(self, iterations, population_size, mutation_type, mutation_reset, cross_type, selection_type,
                  steady_state, select_size, gui, interval):

        # print("Starting...\n")

        d_time = time.time()

        population = []
        check_list = []

        # CREATE FIRST POPULATION
        actual_solution = self.initialize_population(population, check_list, population_size)

        self.__best_route, self.__best_cost, self.__start_best = actual_solution[0], actual_solution[1], actual_solution
        self.__local_best_cost = self.__start_best[1]

        self.__mutation.change_type(mutation_type)
        self.__generation.change_method(cross_type)

        sorted_population = sorted(population, key=lambda x: x[1])

        # TEST
        self.__solution_in_time.append(self.__best_cost)
        self.__time_line.append(round(time.time() - d_time, 2))

        # INITIALIZE GRAPH
        fig = 0
        if gui:
            fig = plt.gcf()
            fig.show()
            fig.canvas.draw()
            var_x, var_y = self.get_plot_data()
            plt.plot(var_x, var_y, linestyle='--', marker='o', color='b')
            fig.canvas.draw()

        # print("START BEST: " + sorted_population[0][0].__str__())
        # print("WITH COST: " + sorted_population[0][1].__str__())
        #
        # print("\nAlgorithm has been started\n")

        for i in range(iterations):

            self.__app_manager()
            self.__radioactivity = 0

            self.check_for_best(sorted_population[0])

            # TEST
            self.start_test(i, d_time, interval)

            # UPDATE GRAPH
            if gui:
                plt.clf()
                var_x, var_y = self.get_plot_data()
                plt.plot(var_x, var_y, linestyle='--', marker='o', color='b')
                fig.canvas.draw()

            # PREPARATION FOR SPECIFIC ALGORITHM IMPROVEMENTS
            new_generation = []
            if selection_type == Selection.RouletteWheel:
                select_size = 0
                for elem in sorted_population:
                    select_size += 1 / elem[1]

            check_list = []
            if steady_state:
                new_generation = sorted_population.copy()
                for elem in new_generation:
                    check_list.append(elem[0])

            # CREATE NEW GENERATION
            for _ in range(int(population_size / 2)):
                male = self.select_parent(sorted_population, selection_type, select_size)
                female = self.select_parent(sorted_population, selection_type, select_size)
                first_child, second_child = self.__generation.create(male[0], female[0])

                sublist = [first_child, second_child]

                for elem in sublist:
                    if elem[0] not in check_list:
                        check_list.append(elem[0])
                        new_generation = [elem] + new_generation
                        if steady_state:
                            weak_sol = new_generation.pop(-1)
                            check_list.remove(weak_sol[0])

            # MUTATION ROUTINE
            self.__mutation.mutation_routine(new_generation, self.__radioactivity + 1)

            # ELITISM
            population = new_generation
            elite_counter = 0
            while elite_counter < 10:
                for elem in sorted_population:
                    if elem[0] not in check_list:
                        population.append(elem)
                        elite_counter += 1

            # RESET MUTATION IF NEEDED
            if self.__mutation.get_mutation_chance() >= mutation_reset:
                self.__mutation.set_mutation_chance(0.001)
                self.__local_best_cost = sys.maxsize
                population = new_generation

            sorted_population = sorted(population, key=lambda x: x[1])
            sorted_population = sorted_population[:population_size]

        # print("\n\n")
        # print(self.get_solution_in_time().__str__())
        # self.print_solution()

        if gui:
            plt.show()

    def initialize_population(self, population, check_list, population_size):
        self.__solution.change_type(Type.Random)
        while population.__len__() < population_size - 1:
            sol = self.__solution.generate()
            if sol[0] not in check_list:
                check_list.append(sol[0])
                population.append(sol)

        self.__solution.change_type(Type.GreedyOne)
        actual_solution = self.__solution.generate()
        population.append(actual_solution)

        return actual_solution

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

        elif selection == Selection.RouletteWheel:
            number = random.uniform(0, size)
            sum_calc = 0
            for elem in population:
                sum_calc += 1 / elem[1]
                if sum_calc > number:
                    group.append(elem)
                    break
        else:
            raise Exception("Cannot find that kind of selection.")

        return group[0]

    def check_for_best(self, best_person):
        if best_person[1] < self.__local_best_cost:
            self.__local_best_cost = best_person[1]
            # print("FOUND LOCAL BEST: " + best_person[0].__str__())
            # print("COST: " + best_person[1].__str__())

            if best_person[1] < self.__best_cost:
                self.__best_cost = best_person[1]
                self.__best_route = best_person[0]
                self.__radioactivity -= 20
                # print("FOUND BEST: " + self.__best_route.__str__())
                # print("COST: " + self.__best_cost.__str__())

            self.__radioactivity -= 8

    def __app_manager(self):
        if self.__keyboard.kbhit():
            key = ord(self.__keyboard.getch())
            if key == 32:
                print("Program paused")
                print(self.get_solution_in_time().__str__())
                self.print_solution()
                while True:
                    key = ord(self.__keyboard.getch())
                    if key == 32:
                        print("Program resumed")
                        break
                    elif key == 27:
                        print("Program stopped")
                        exit(0)
            elif key == 27:
                print("Program stopped")
                print(self.get_solution_in_time().__str__())
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

    def get_solution_in_time(self):
        return self.__solution_in_time, self.__time_line

    def start_test(self, i, time_t, interval):
        diff = time.time() - time_t
        if (i + 1) % interval == 0:
            self.__solution_in_time.append(self.__best_cost)
            self.__time_line.append(round(diff, 2))

    def print_solution(self):
        print("Best route: " + self.__best_route.__str__())
        print("with cost: " + self.__best_cost.__str__())
        print("Start best: " + self.__start_best[0].__str__())
        print("with cost: " + self.__start_best[1].__str__())

    def get_plot_data(self):
        x = self.__best_route.copy()
        y = self.__best_route.copy()
        y.pop(0)
        y.append(y[0])

        return x, y


if __name__ == "__main__":
    alg = Genetic("test/TSP/pr226.tsp", "COORDS_EUC")
    # Iterations, Population size, Mutation type, Mutation_reset (chance), Cross type, Selection type,
    # Steady state, Tournament size, GUI true/false, INTERVAL - measure time
    pop_size = 100
    tm = time.time()
    alg.calculate(25000, pop_size, MType.Invert, 0.08, Method.OX1,
                  Selection.RouletteWheel, True, int(pop_size * 0.12), False, 500)
    tm = time.time() - tm
    print("Processing time: " + tm.__str__())
