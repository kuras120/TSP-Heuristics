import random
from enum import Enum


class Type(Enum):
    Invert = 0
    RandomSlide = 1
    Insert = 2
    SwapOne = 3


class Mutation:
    def __init__(self, data):
        self.__type = Type.Invert
        self.__mutation_chance = 0.001
        self.__data = data
        self.__radioactivity = 0

        self.__mutation_ratio = 0

    def get_ratio(self):
        return self.__mutation_ratio

    def get_mutation_chance(self):
        return self.__mutation_chance

    def set_mutation_chance(self, mutation):
        self.__mutation_chance = mutation

    def change_type(self, type_m):
        self.__type = type_m

    def mutation_routine(self, population, points):
        self.__radioactivity += points
        if self.__radioactivity >= 20:
            self.__mutation_chance += self.__mutation_chance
            self.__radioactivity = 0
        elif self.__radioactivity < 0:
            self.__mutation_chance = 0.001
            self.__radioactivity = 0

        self.__mutation_chance = round(self.__mutation_chance, 3)
        for elem in population:
            self.mutate(elem)

        self.__mutation_ratio = self.__mutation_ratio / population.__len__()

    def mutate(self, person):
        counter = 0
        person[0].pop(-1)

        if self.__type == Type.SwapOne:
            for i in range(person[0].__len__() - 1):
                chance = random.uniform(0, 1)
                if chance < self.__mutation_chance:
                    counter += 1
                    index_to_swap = i

                    while index_to_swap == i:
                        index_to_swap = random.randrange(person[0].__len__())

                    person[0][i], person[0][index_to_swap] = person[0][index_to_swap], person[0][i]

        elif self.__type == Type.Invert:
            for i in range(person[0].__len__() - 1):
                chance = random.uniform(0, 1)
                if chance < self.__mutation_chance:
                    counter += 1
                    index_to_swap = i

                    while index_to_swap == i:
                        index_to_swap = random.randrange(person[0].__len__())

                    if index_to_swap < i:
                        person[0][index_to_swap:i] = reversed(person[0][index_to_swap:i])
                    else:
                        person[0][i:index_to_swap] = reversed(person[0][i:index_to_swap])

        else:
            raise NotImplementedError

        self.__mutation_ratio += counter

        person[0].append(person[0][0])
        cost = 0
        for j in range(1, person[0].__len__()):
            cost += self.__data[person[0][j - 1]][person[0][j]]

        person[1] = cost
