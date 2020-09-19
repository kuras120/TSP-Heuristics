from Genetic import Genetic, Method as PopMethod, MType, Selection
from AntColonyOpt import AntColonyOpt, Method


def 
if __name__ == "__main__":

    pop_size = 100
    ant_group = 25

    genetic = Genetic("test/TSP/gr21.tsp", "LOWER_DIAG")
    ant_colony = AntColonyOpt("test/TSP/gr21.tsp", "LOWER_DIAG")

    costs_g = []
    times_g = []
    costs_a = []
    times_a = []

    for test1 in range(10):
        genetic.calculate(100, pop_size, MType.Invert, 0.08, PopMethod.OX1, Selection.RouletteWheel, True,
                          int(pop_size * 0.12), False, 10)
        c_g, tl_g = genetic.get_solution_in_time()
        costs_g.append(c_g)
        times_g.append(tl_g)

        ant_colony.calculate(100, ant_group, 0.50, 7 * ant_group, Method.Invert, (5, 1), False, 10)
        c_a, tl_a = ant_colony.get_solution_in_time()
        costs_a.append(c_a)
        times_a.append(tl_a)

        genetic.clear_values()
        ant_colony.clear_values()

    test_file = open("test/GA&ACO/testGR21.txt", "w+")
    test_file.write("----------GENETIC----------\n")
    average = [0] * (costs_g.__len__() + 1)
    for it in range(costs_g.__len__()):
        test_file.write(costs_g[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(costs_g[it].__len__()):
            average[it2] += costs_g[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    test_file.write("\n")
    average = [0] * (times_g.__len__() + 1)
    for it in range(times_g.__len__()):
        test_file.write(times_g[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(times_g[it].__len__()):
            average[it2] += times_g[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    test_file.write("----------ANT-COLONY----------\n")
    average = [0] * (costs_a.__len__() + 1)
    for it in range(costs_a.__len__()):
        test_file.write(costs_a[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(costs_a[it].__len__()):
            average[it2] += costs_a[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    test_file.write("\n")
    average = [0] * (times_a.__len__() + 1)
    for it in range(times_a.__len__()):
        test_file.write(times_a[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(times_a[it].__len__()):
            average[it2] += times_a[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    # --------------------------------------------------------------------------------------------------
    # PopMethod test
    genetic = Genetic("test/TSP/gr48.tsp", "LOWER_DIAG")

    costs_g = []
    times_g = []
    costs_g1 = []
    times_g1 = []
    costs_g2 = []
    times_g2 = []

    for test1 in range(10):
        genetic.calculate(2500, pop_size, MType.Invert, 0.08, PopMethod.OX1, Selection.RouletteWheel, True,
                          int(pop_size * 0.12), False, 250)
        c_g, tl_g = genetic.get_solution_in_time()
        costs_g.append([c_g])
        times_g.append([tl_g])
        genetic.clear_values()

        genetic.calculate(2500, pop_size, MType.Invert, 0.08, PopMethod.PMX, Selection.RouletteWheel, True,
                          int(pop_size * 0.12), False, 250)
        c_g, tl_g = genetic.get_solution_in_time()
        costs_g1.append([c_g])
        times_g1.append([tl_g])
        genetic.clear_values()

        genetic.calculate(2500, pop_size, MType.Invert, 0.08, PopMethod.CX, Selection.RouletteWheel, True,
                          int(pop_size * 0.12), False, 250)
        c_g, tl_g = genetic.get_solution_in_time()
        costs_g2.append([c_g])
        times_g2.append([tl_g])
        genetic.clear_values()

    test_file = open("test/GA&ACO/testGR48-GA-PopMethod.txt", "w+")
    test_file.write("----------GENETIC-OX1----------\n")
    average = [0] * (costs_g.__len__() + 1)
    for it in range(costs_g.__len__()):
        test_file.write(costs_g[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(costs_g[it].__len__()):
            average[it2] += costs_g[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    test_file.write("\n")
    average = [0] * (times_g.__len__() + 1)
    for it in range(times_g.__len__()):
        test_file.write(times_g[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(times_g[it].__len__()):
            average[it2] += times_g[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    # g1
    test_file.write("----------GENETIC-PMX----------\n")
    average = [0] * (costs_g1.__len__() + 1)
    for it in range(costs_g1.__len__()):
        test_file.write(costs_g1[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(costs_g1[it].__len__()):
            average[it2] += costs_g1[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    test_file.write("\n")
    average = [0] * (times_g1.__len__() + 1)
    for it in range(times_g1.__len__()):
        test_file.write(times_g1[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(times_g1[it].__len__()):
            average[it2] += times_g1[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    # g2
    test_file.write("----------GENETIC-CX----------\n")
    average = [0] * (costs_g2.__len__() + 1)
    for it in range(costs_g2.__len__()):
        test_file.write(costs_g2[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(costs_g2[it].__len__()):
            average[it2] += costs_g2[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    test_file.write("\n")
    average = [0] * (times_g2.__len__() + 1)
    for it in range(times_g2.__len__()):
        test_file.write(times_g2[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(times_g2[it].__len__()):
            average[it2] += times_g2[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    # --------------------------------------------------------------------------------------------------
    # Selection test
    genetic = Genetic("test/TSP/gr48.tsp", "LOWER_DIAG")

    costs_g = []
    times_g = []
    costs_g1 = []
    times_g1 = []

    for test1 in range(10):
        genetic.calculate(2500, pop_size, MType.Invert, 0.08, PopMethod.OX1, Selection.RouletteWheel, True,
                          int(pop_size * 0.12), False, 250)
        c_g, tl_g = genetic.get_solution_in_time()
        costs_g.append([c_g])
        times_g.append([tl_g])
        genetic.clear_values()

        genetic.calculate(2500, pop_size, MType.Invert, 0.08, PopMethod.OX1, Selection.Tournament, False,
                          int(pop_size * 0.12), False, 250)
        c_g, tl_g = genetic.get_solution_in_time()
        costs_g1.append([c_g])
        times_g1.append([tl_g])
        genetic.clear_values()

    test_file = open("test/GA&ACO/testGR48-GA-Selection.txt", "w+")
    test_file.write("----------GENETIC-ROULETTE----------\n")
    average = [0] * (costs_g.__len__() + 1)
    for it in range(costs_g.__len__()):
        test_file.write(costs_g[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(costs_g[it].__len__()):
            average[it2] += costs_g[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    test_file.write("\n")
    average = [0] * (times_g.__len__() + 1)
    for it in range(times_g.__len__()):
        test_file.write(times_g[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(times_g[it].__len__()):
            average[it2] += times_g[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    # g1
    test_file.write("----------GENETIC-TOURNAMENT----------\n")
    average = [0] * (costs_g1.__len__() + 1)
    for it in range(costs_g1.__len__()):
        test_file.write(costs_g1[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(costs_g1[it].__len__()):
            average[it2] += costs_g1[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    test_file.write("\n")
    average = [0] * (times_g1.__len__() + 1)
    for it in range(times_g1.__len__()):
        test_file.write(times_g1[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(times_g1[it].__len__()):
            average[it2] += times_g1[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    # --------------------------------------------------------------------------------------------------

    genetic = Genetic("test/TSP/gr48.tsp", "LOWER_DIAG")
    ant_colony = AntColonyOpt("test/TSP/gr48.tsp", "LOWER_DIAG")

    costs_g = []
    times_g = []
    costs_a = []
    times_a = []

    for test1 in range(10):
        genetic.calculate(2500, pop_size, MType.Invert, 0.08, PopMethod.OX1, Selection.RouletteWheel, True,
                          int(pop_size * 0.12), False, 250)
        c_g, tl_g = genetic.get_solution_in_time()
        costs_g.append([c_g])
        times_g.append([tl_g])

        ant_colony.calculate(2500, ant_group, 0.50, 7 * ant_group, Method.Invert, (5, 1), False, 250)
        c_a, tl_a = ant_colony.get_solution_in_time()
        costs_a.append([c_a])
        times_a.append([tl_a])

        genetic.clear_values()
        ant_colony.clear_values()

    test_file = open("test/GA&ACO/testGR48.txt", "w+")
    test_file.write("----------GENETIC----------\n")
    average = [0] * (costs_g.__len__() + 1)
    for it in range(costs_g.__len__()):
        test_file.write(costs_g[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(costs_g[it].__len__()):
            average[it2] += costs_g[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    test_file.write("\n")
    average = [0] * (times_g.__len__() + 1)
    for it in range(times_g.__len__()):
        test_file.write(times_g[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(times_g[it].__len__()):
            average[it2] += times_g[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    test_file.write("----------ANT-COLONY----------\n")
    average = [0] * (costs_a.__len__() + 1)
    for it in range(costs_a.__len__()):
        test_file.write(costs_a[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(costs_a[it].__len__()):
            average[it2] += costs_a[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    test_file.write("\n")
    average = [0] * (times_a.__len__() + 1)
    for it in range(times_a.__len__()):
        test_file.write(times_a[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(times_a[it].__len__()):
            average[it2] += times_a[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    # --------------------------------------------------------------------------------------------------

    genetic = Genetic("test/TSP/gr96.tsp", "COORDS_GEO")
    ant_colony = AntColonyOpt("test/TSP/gr96.tsp", "COORDS_GEO")

    costs_g = []
    times_g = []
    costs_a = []
    times_a = []

    for test1 in range(10):
        genetic.calculate(5000, pop_size, MType.Invert, 0.08, PopMethod.OX1, Selection.RouletteWheel, True,
                          int(pop_size * 0.12), False, 500)
        c_g, tl_g = genetic.get_solution_in_time()
        costs_g.append([c_g])
        times_g.append([tl_g])

        ant_colony.calculate(5000, ant_group, 0.50, 7 * ant_group, Method.Invert, (5, 1), False, 500)
        c_a, tl_a = ant_colony.get_solution_in_time()
        costs_a.append([c_a])
        times_a.append([tl_a])

        genetic.clear_values()
        ant_colony.clear_values()

    test_file = open("test/GA&ACO/testGR96.txt", "w+")
    test_file.write("----------GENETIC----------\n")
    average = [0] * (costs_g.__len__() + 1)
    for it in range(costs_g.__len__()):
        test_file.write(costs_g[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(costs_g[it].__len__()):
            average[it2] += costs_g[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    test_file.write("\n")
    average = [0] * (times_g.__len__() + 1)
    for it in range(times_g.__len__()):
        test_file.write(times_g[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(times_g[it].__len__()):
            average[it2] += times_g[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    test_file.write("----------ANT-COLONY----------\n")
    average = [0] * (costs_a.__len__() + 1)
    for it in range(costs_a.__len__()):
        test_file.write(costs_a[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(costs_a[it].__len__()):
            average[it2] += costs_a[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    test_file.write("\n")
    average = [0] * (times_a.__len__() + 1)
    for it in range(times_a.__len__()):
        test_file.write(times_a[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(times_a[it].__len__()):
            average[it2] += times_a[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    # --------------------------------------------------------------------------------------------------

    genetic = Genetic("test/TSP/gr120.tsp", "LOWER_DIAG")
    ant_colony = AntColonyOpt("test/TSP/gr120.tsp", "LOWER_DIAG")

    costs_g = []
    times_g = []
    costs_a = []
    times_a = []

    for test1 in range(10):
        genetic.calculate(5000, pop_size, MType.Invert, 0.08, PopMethod.OX1, Selection.RouletteWheel, True,
                          int(pop_size * 0.12), False, 500)
        c_g, tl_g = genetic.get_solution_in_time()
        costs_g.append([c_g])
        times_g.append([tl_g])

        ant_colony.calculate(5000, ant_group, 0.50, 7 * ant_group, Method.Invert, (5, 1), False, 500)
        c_a, tl_a = ant_colony.get_solution_in_time()
        costs_a.append([c_a])
        times_a.append([tl_a])

        genetic.clear_values()
        ant_colony.clear_values()

    test_file = open("test/GA&ACO/testGR120.txt", "w+")
    test_file.write("----------GENETIC----------\n")
    average = [0] * (costs_g.__len__() + 1)
    for it in range(costs_g.__len__()):
        test_file.write(costs_g[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(costs_g[it].__len__()):
            average[it2] += costs_g[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    test_file.write("\n")
    average = [0] * (times_g.__len__() + 1)
    for it in range(times_g.__len__()):
        test_file.write(times_g[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(times_g[it].__len__()):
            average[it2] += times_g[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    test_file.write("----------ANT-COLONY----------\n")
    average = [0] * (costs_a.__len__() + 1)
    for it in range(costs_a.__len__()):
        test_file.write(costs_a[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(costs_a[it].__len__()):
            average[it2] += costs_a[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")

    test_file.write("\n")
    average = [0] * (times_a.__len__() + 1)
    for it in range(times_a.__len__()):
        test_file.write(times_a[it].__str__().replace('[', '').replace(']', '') + "\n")
        for it2 in range(times_a[it].__len__()):
            average[it2] += times_a[it][it2]
    for it in range(average.__len__()):
        average[it] /= 10
        average[it] = round(average[it], 2)
    test_file.write("----------AVERAGE----------\n")
    test_file.write(average.__str__() + "\n")
