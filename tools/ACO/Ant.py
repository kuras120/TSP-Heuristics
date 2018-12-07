import sys


class Ant:
	def __init__(self, data):
		self.__tour = []
		self.__cost = sys.maxsize
		self.__map = data
		self.__tabu_list = []

	def find_way(self, start):
		self.__tabu_list.append(start)
		current_place = start
		while self.__tabu_list.__len__() < self.__map.__len__():
				for [cost, pheromone] in self.__map[current_place]:
					