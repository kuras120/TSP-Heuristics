from SimulatedAnnealing import *


if __name__ == "__main__":
    annealing = SimulatedAnnealing("test/TSP/pr124.tsp", "COORDS_EUC")
    annealing.calculate(Type.GreedyOne, Method.Mixed, Temperature.Geometric, 50000)
    statistics = annealing.get_stats()
    everythin = sum(statistics)

    print("SWAP: " + (statistics[0]).__str__())
    print("INSERT: " + (statistics[1]).__str__())
    print("INVERT: " + (statistics[2]).__str__())

    costs1 = []
    costs2 = []
    costs3 = []
    costs4 = []
    for k in range(10):
        annealing.calculate_sa_list(Type.GreedyOne, Method.Mixed, 250000)
        c, r = annealing.get_solution()
        costs1.append(c)
        annealing.clear_values()
    for k in range(10):
        annealing.calculate(Type.GreedyOne, Method.Mixed, Temperature.Geometric, 250000)
        c, r = annealing.get_solution()
        costs2.append(c)
        annealing.clear_values()
    for k in range(10):
        annealing.calculate(Type.GreedyOne, Method.Mixed, Temperature.Hyperbolic, 250000)
        c, r = annealing.get_solution()
        costs3.append(c)
        annealing.clear_values()
    for k in range(10):
        annealing.calculate(Type.GreedyOne, Method.Mixed, Temperature.Exponential, 250000)
        c, r = annealing.get_solution()
        costs4.append(c)
        annealing.clear_values()

    print("Wyniki dla mixed list")
    srednia = 0
    for elem in costs1:
        srednia += elem
        print(elem)
    print("Srednia: " + (srednia/10).__str__())
    print("Wyniki dla mixed geometric")
    srednia = 0
    for elem in costs2:
        srednia += elem
        print(elem)
    print("Srednia: " + (srednia/10).__str__())
    print("Wyniki dla mixed hyperbolic")
    srednia = 0
    for elem in costs3:
        srednia += elem
        print(elem)
    print("Srednia: " + (srednia/10).__str__())
    print("Wyniki dla mixed exponential")
    srednia = 0
    for elem in costs4:
        srednia += elem
        print(elem)
    print("Srednia: " + (srednia/10).__str__())

