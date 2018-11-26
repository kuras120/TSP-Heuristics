from SimulatedAnnealing import *


if __name__ == "__main__":
    annealing = SimulatedAnnealing("test/TSP/gr8.tsp", "LOWER_DIAG")
    # annealing.calculate(Type.Greedy, Method.Mixed, 500000)
    generator = NeighboursGenerator(annealing.get_data())
    generator.change_method(Method.ThreeOpt)
    routes = generator.generate_one([0, 1, 2, 3, 4, 5, 6, 7, 0])
    print(routes)

