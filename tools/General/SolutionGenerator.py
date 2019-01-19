import random
from enum import Enum

from GreedySearch import GreedySearch
from tools.FileLoader import *


class Type(Enum):
    Greedy = 0
    GreedyOne = 1
    Random = 2


class SolutionGenerator:
    def __init__(self, file, type_t, data=None):
        self.__gen_type = Type.Greedy
        self.__file = file
        self.__type_t = type_t

        if not data:
            file_t = FileLoader()
            file_t.load(file, type_t)
            self.__data = file_t.get_data()
        else:
            self.__data = data

    def change_type(self, type_t):
        self.__gen_type = type_t

    def generate(self):
        temp_cost = 0
        temp_route = []

        # GREEDY SOLUTION
        if self.__gen_type == Type.Greedy:
            greedy = GreedySearch(self.__file, self.__type_t)
            temp_cost, temp_route = greedy.calculate()

        elif self.__gen_type == Type.GreedyOne:
            greedy = GreedySearch(self.__file, self.__type_t)
            temp_cost, temp_route = greedy.calculate_one(random.randrange(self.__data.__len__()))

        # RANDOM SOLUTION
        elif self.__gen_type == Type.Random:
            cities = list(range(self.__data.__len__()))
            first_index = random.randrange(self.__data.__len__())
            temp_route.append(cities.pop(first_index))
            while cities:
                index = random.randrange(cities.__len__())
                temp_route.append(cities.pop(index))
            temp_route.append(temp_route[0])
            for i in range(1, temp_route.__len__()):
                temp_cost += self.__data[temp_route[i - 1]][temp_route[i]]

        return [temp_route, round(temp_cost, 2)]
