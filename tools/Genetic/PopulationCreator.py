import random
from enum import Enum


class Method(Enum):
    PMX = 0
    CX = 1
    OX1 = 2
    OX2 = 3
    POS = 4
    VR = 5
    AP = 6
    SCX = 7


class PopulationCreator:
    def __init__(self, data):
        self.__method = Method.OX1
        self.__data = data

    def change_method(self, method):
        self.__method = method

    def get_method(self):
        return self.__method

    def create(self, parent_male, parent_female, index_one=0, index_two=0):
        parent_male_t = parent_male.copy()
        parent_female_t = parent_female.copy()
        parent_male_t.pop(-1)
        parent_female_t.pop(-1)

        person_length = parent_male_t.__len__()

        while index_one == index_two:
            index_one = random.randrange(person_length)
            index_two = random.randrange(person_length)

        if index_one > index_two:
            index_one, index_two = index_two, index_one

        first_child = [-1] * person_length
        second_child = [-1] * person_length

        if self.__method == Method.OX1:
            first_child[index_one:index_two + 1] = parent_male_t[index_one:index_two + 1]
            second_child[index_one:index_two + 1] = parent_female_t[index_one:index_two + 1]

            iterator_first = index_two + 1
            iterator_second = index_two + 1

            for i in range(index_two, person_length):
                if parent_female_t[i] not in first_child:
                    if iterator_first >= person_length:
                        iterator_first = 0

                    first_child[iterator_first] = parent_female_t[i]
                    iterator_first += 1

                if parent_male_t[i] not in second_child:
                    if iterator_second >= person_length:
                        iterator_second = 0

                    second_child[iterator_second] = parent_male_t[i]
                    iterator_second += 1

            for i in range(index_two):
                if parent_female_t[i] not in first_child:
                    if iterator_first >= person_length:
                        iterator_first = 0

                    first_child[iterator_first] = parent_female_t[i]
                    iterator_first += 1

                if parent_male_t[i] not in second_child:
                    if iterator_second >= person_length:
                        iterator_second = 0

                    second_child[iterator_second] = parent_male_t[i]
                    iterator_second += 1

            first_child.append(first_child[0])
            second_child.append(second_child[0])

        elif self.__method == Method.PMX:
            first_child[index_one:index_two + 1] = parent_male_t[index_one:index_two + 1]
            second_child[index_one:index_two + 1] = parent_female_t[index_one:index_two + 1]

            for i in range(index_one, index_two + 1):
                if parent_female_t[i] not in first_child:
                    insert_index = i
                    while index_one <= insert_index <= index_two:
                        gene = parent_male_t[insert_index]
                        insert_index = parent_female_t.index(gene)
                    first_child[insert_index] = parent_female_t[i]

                if parent_male_t[i] not in second_child:
                    insert_index = i
                    while index_one <= insert_index <= index_two:
                        gene = parent_female_t[insert_index]
                        insert_index = parent_male_t.index(gene)
                    second_child[insert_index] = parent_male_t[i]

            for i in range(person_length):
                if first_child[i] == -1:
                    first_child[i] = parent_female_t[i]
                if second_child[i] == -1:
                    second_child[i] = parent_male_t[i]

            first_child.append(first_child[0])
            second_child.append(second_child[0])

        elif self.__method == Method.CX:
            parent_female_t.insert(person_length, parent_female_t.pop(0))
            change = True
            for i in range(person_length):
                index = i
                if parent_male_t[i] not in first_child:
                    while True:
                        if change:
                            first_child[index] = parent_male_t[index]
                            second_child[index] = parent_female_t[index]
                        else:
                            first_child[index] = parent_female_t[index]
                            second_child[index] = parent_male_t[index]
                        index = parent_male_t.index(parent_female_t[index])
                        if index == i:
                            break
                    if change:
                        change = False
                    else:
                        change = True

            first_child.append(first_child[0])
            second_child.append(second_child[0])

        else:
            raise NotImplementedError

        cost_first = 0
        cost_second = 0
        for i in range(1, person_length + 1):
            cost_first += self.__data[first_child[i - 1]][first_child[i]]
            cost_second += self.__data[second_child[i - 1]][second_child[i]]

        return [first_child, cost_first], [second_child, cost_second]
