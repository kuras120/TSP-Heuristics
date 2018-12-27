import random
from tools.FileLoader import *
from copy import deepcopy


class Ant:
	def __init__(self, data, actual_best):
		self.__tour = []
		self.__cost = 0
		self.__map = data
		self.__actual_best = actual_best
		self.__tabu_list = []

		# TEST
		self.__initialize_map(data)

	def spawn(self, start):
		self.__tour.append(start)
		self.__tabu_list.append(start)
		current_place = start
		while self.__tabu_list.__len__() < self.__map.__len__():
			place = self.__map[current_place]
			pheromone_sum = 0
			for i in range(place.__len__()):
				if i not in self.__tabu_list:
					pheromone_sum += place[i][1]

			index = start
			prev_index = start
			route = random.randrange(pheromone_sum)
			route_weight = 0
			for i in range(place.__len__()):
				if i not in self.__tabu_list:
					not_in_tabu = True
					route_weight += place[i][1]
				else:
					not_in_tabu = False
				if route_weight > route:
					if i == 0:
						index = 0
						break
					else:
						index = prev_index
						break
				if not_in_tabu:
					prev_index = i

			self.__tour.append(index)
			self.__cost += self.__map[current_place][index]
			self.__tabu_list.append(index)
			current_place = index

		self.__tour.append(self.__tour[0])
		self.__cost += self.__map[self.__tour[0]]

	def leave_pheromones(self):
		pheromones_amount = round(1 / (self.__cost/self.__actual_best), 2)
		for i in range(1, self.__tour.__len__()):
			self.__map[self.__tour[i-1]][self.__tour[i]][1] += pheromones_amount

		return self.__map

	def __initialize_map(self, data):
		self.__map = deepcopy(data)
		for i in range(self.__map.__len__()):
			for j in range(self.__map.__len__()):
				self.__map[i][j] = [self.__map[i][j], 1]


if __name__ == "__main__":
	file = FileLoader()
	file.load("../../test/TSP/gr8.tsp", "LOWER_DIAG")
	ant = Ant(file.get_data(), 2000)
