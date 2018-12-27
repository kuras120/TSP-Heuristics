from tools.FileLoader import *
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
        self.__start_best = [None, None]

        for i in range(self.__data.__len__()):
            for j in range(self.__data.__len__()):
                self.__data[i][j] = [self.__data[i][j], 1]

    def calculate(self):
        raise NotImplementedError

