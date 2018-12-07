import sys


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

        for row in self.__data:
        	for elem in row:
        		elem = [elem, 1]
	
	def calculate(self):
		raise NotImplementedException
		