import copy

from matplotlib import pyplot as plt

from tools.ACO.Ant import *
from tools.General.NeighboursGenerator import *
from tools.KBHit import *


class AntColonyOpt:
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
        self.__local_best = [[], sys.maxsize]

        # OPTIMIZATION
        self.__neighbours_generator = NeighboursGenerator(copy.deepcopy(self.__data))
        self.__solution_generator = SolutionGenerator(self.__file, self.__type_t)
        # RESET
        self.__iterations_without_changes = 0

        # TEST
        self.__solution_in_time = []
        self.__time_line = []

        for i in range(self.__data.__len__()):
            for j in range(self.__data.__len__()):
                self.__data[i][j] = [self.__data[i][j], 1]

    def calculate(self, iterations, group_size, evaporation_percent, without_changes, local_search_type, path_params,
                  gui, interval):

        print("Starting...\n")

        d_time = time.time()

        self.__neighbours_generator.change_method(local_search_type)
        self.__solution_generator.change_type(Type.GreedyOne)

        self.__start_best = self.__solution_generator.generate()
        self.__best_route, self.__best_cost = self.__start_best[0], self.__start_best[1]

        # ADD PHEROMONES FOR GREEDY SOLUTION
        for i in range(1, self.__best_route.__len__()):
            self.__data[self.__best_route[i - 1]][self.__best_route[i]][1] += 1.5

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

        print("START BEST: " + self.__start_best.__str__())
        print("\nAlgorithm has been started\n")

        for i in range(iterations):
            self.__app_manager()

            # RESET IF NEEDED
            if self.__iterations_without_changes > without_changes:
                self.__iterations_without_changes = 0
                self.__local_best = [[], sys.maxsize]
                # print("NEIGHBOURHOOD SEARCH: " + self.__best_route.__str__() + " " + self.__best_cost.__str__())

                neighbours = self.__neighbours_generator.generate(self.__best_route, [])
                neighbours.sort(key=lambda x: x[1])

                paths_iterator = 0
                neighbour_path = neighbours[paths_iterator]
                while neighbour_path[1] < self.__best_cost:
                    for j in range(1, neighbour_path[0].__len__()):
                        self.__data[neighbour_path[0][j - 1]][neighbour_path[0][j]][1] += 0.5
                    paths_iterator += 1
                    neighbour_path = neighbours[paths_iterator]

                self.check_for_best(neighbours[0])

            # RELEASE ANTS!
            ant_colony = self.__generate_ants(group_size, path_params)

            # TEST
            self.start_test(i, d_time, interval)

            # UPDATE GRAPH
            if gui:
                plt.clf()
                var_x, var_y = self.get_plot_data()
                plt.plot(var_x, var_y, linestyle='--', marker='o', color='b')
                fig.canvas.draw()

            # EVAPORATION (PAROWANIE)
            self.__pheromones_evaporation(evaporation_percent)

            # RELEASE PHEROMONES
            self.__pheromones_release(group_size, ant_colony)

            self.__iterations_without_changes += 1

        print("\n\n")
        print(self.get_solution_in_time().__str__())
        self.print_solution()

        if gui:
            plt.show()

    def __generate_ants(self, group_size, path_params):
        ant_colony = []

        for _ in range(group_size):
            ant = Ant(self.__data)
            spawn_point = random.randrange(self.__loader.get_number_of_cities())
            ant.move(spawn_point, path_params[0], path_params[1])
            temp_solution = ant.get_solution()

            self.check_for_best(temp_solution)
            ant_colony.append(ant)

        return ant_colony

    def __pheromones_evaporation(self, percent):
        for i in range(self.__data.__len__()):
            for j in range(self.__data.__len__()):
                if self.__data[i][j][1] * (1 - percent) >= 0.001:
                    self.__data[i][j][1] *= (1 - percent)
                else:
                    self.__data[i][j][1] = 0.001

    def __pheromones_release(self, group_size, ant_colony):
        for i in range(group_size):
            self.__data = ant_colony[i].leave_pheromones(self.__data)

    def check_for_best(self, temp_solution):
        found = False
        if temp_solution[1] < self.__local_best[1]:
            self.__local_best = [temp_solution[0], temp_solution[1]]
            print("FOUND LOCAL BEST: " + temp_solution[0].__str__())
            print("COST: " + temp_solution[1].__str__())
            self.__iterations_without_changes = int(self.__iterations_without_changes / 2)
            found = True

            if temp_solution[1] < self.__best_cost:
                self.__best_cost = temp_solution[1]
                self.__best_route = temp_solution[0]
                print("FOUND BEST: " + temp_solution[0].__str__())
                print("COST: " + temp_solution[1].__str__())
                self.__iterations_without_changes = 0

        return found

    def __app_manager(self):
        if self.__keyboard.kbhit():
            key = ord(self.__keyboard.getch())
            if key == 32:
                print("\nProgram paused\n")
                print(self.get_solution_in_time().__str__())
                self.print_solution()
                while True:
                    key = ord(self.__keyboard.getch())
                    if key == 32:
                        print("\nProgram resumed\n")
                        break
                    elif key == 27:
                        print("\nProgram stopped\n")
                        exit(0)
            elif key == 27:
                print("\nProgram stopped\n")
                print(self.get_solution_in_time().__str__())
                self.print_solution()
                exit(0)

    def clear_values(self):
        self.__best_route = []
        self.__best_cost = sys.maxsize
        self.__start_best = []
        self.__local_best = [[], sys.maxsize]

        # RESET
        self.__iterations_without_changes = 0

        # TEST
        self.__solution_in_time = []
        self.__time_line = []

        for i in range(self.__data.__len__()):
            for j in range(self.__data.__len__()):
                self.__data[i][j][1] = 1

    def get_solution_in_time(self):
        return self.__solution_in_time, self.__time_line

    def start_test(self, i, tm_t, interval):
        diff = time.time() - tm_t
        if (i + 1) % interval == 0:
            self.__solution_in_time.append(self.__best_cost)
            self.__time_line.append(round(diff, 2))

    def print_solution(self):
        print("Best route: " + self.__best_route.__str__())
        print("with cost: " + self.__best_cost.__str__())
        print("Start best: " + self.__start_best[0].__str__())
        print("with cost: " + self.__start_best[1].__str__())
        print("Local best: " + self.__local_best[0].__str__())
        print("with cost: " + self.__local_best[1].__str__())

    def get_plot_data(self):
        x = self.__best_route.copy()
        y = self.__best_route.copy()
        y.pop(0)
        y.append(y[0])

        return x, y


if __name__ == "__main__":
    colony = AntColonyOpt("test/TSP/pr124.tsp", "COORDS_EUC")
    # ITERATIONS, GROUP SIZE, EVAPORATION, ITERATIONS WITHOUT CHANGES, LOCAL SEARCH METHOD
    # (COST, PHEROMONE) WEIGHT, GUI TRUE/FALSE, INTERVAL - measure time
    ant_group = 25
    tm = time.time()
    colony.calculate(10000, ant_group, 0.50, 7 * ant_group, Method.Invert, (5, 1), True, 500)
    tm = time.time() - tm
    print("Processing time: " + tm.__str__())
