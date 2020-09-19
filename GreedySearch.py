import copy
import sys
import time

from tools.FileLoader import *


class GreedySearch:
    def __init__(self, file, type_t):
        self.__loader = FileLoader()
        self.__loader.load(file, type_t)

        self.__data = self.__loader.get_data()
        self.__best_route = []
        self.__best_cost = sys.maxsize

    def calculate(self):
        for elem in self.__data:
            cost = 0
            temp = copy.deepcopy(self.__data)
            index = temp.index(elem)
            visited = [index]
            while visited.__len__() < self.__loader.get_number_of_cities():
                temp_index = temp[index].index(min(temp[index][:index] + temp[index][index + 1:]))
                if temp_index not in visited:
                    cost += min(temp[index][:index] + temp[index][index + 1:])
                    visited.append(temp_index)
                    index = temp_index
                else:
                    temp[index][temp_index] = sys.maxsize

            cost += self.__data[visited[visited.__len__() - 1]][visited[0]]
            visited.append(visited[0])
            if cost < self.__best_cost:
                # print("GREEDY FOUND " + visited.__str__())
                self.__best_cost = cost
                self.__best_route = visited

        return self.__best_cost, self.__best_route

    def calculate_one(self, start_index):
        if start_index > self.__data.__len__() - 1 or start_index < 0:
            raise Exception("Start index must be in range of an instance size.")
        else:
            index = start_index
            cost = 0
            temp = copy.deepcopy(self.__data)
            visited = [index]
            while visited.__len__() < self.__loader.get_number_of_cities():
                temp_index = temp[index].index(min(temp[index][:index] + temp[index][index + 1:]))
                if temp_index not in visited:
                    cost += min(temp[index][:index] + temp[index][index + 1:])
                    visited.append(temp_index)
                    index = temp_index
                else:
                    temp[index][temp_index] = sys.maxsize

            cost += self.__data[visited[visited.__len__() - 1]][visited[0]]
            visited.append(visited[0])
            if cost < self.__best_cost:
                # print("GREEDY FOUND " + visited.__str__())
                self.__best_cost = cost
                self.__best_route = visited

        return self.__best_cost, self.__best_route

    def clear_values(self):
        self.__best_route = []
        self.__best_cost = sys.maxsize

    def print_solution(self):
        print("Best route: " + self.__best_route.__str__())
        print("with cost: " + self.__best_cost.__str__())

    def get_solution(self):
        return self.__best_cost, self.__best_route

    def get_number_of_cities(self):
        return self.__data.__len__()


if __name__ == "__main__":
    greedy = GreedySearch("test/TSP/gr96.tsp", "COORDS_GEO")
    start_time = time.time()
    greedy.calculate()
    print("--- %s seconds ---" % (time.time() - start_time))
    greedy.print_solution()
