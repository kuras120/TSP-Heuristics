from FileLoader import *


def calculate_route(route, data):
    cost = 0
    for i in range(1, route.__len__()):
        cost += data[route[i-1]][route[i]]
    return cost


if __name__ == "__main__":
    loader = FileLoader()
    loader.load("test/TSP/berlin52.tsp", "COORDS_EUC")
    route =[39, 38, 35, 34, 33, 43, 45, 15, 28, 49, 19, 22, 29, 1, 6, 41, 20, 16, 2, 17, 30, 21, 0, 48, 31, 44, 18, 40,
            7, 8, 9, 42, 32, 50, 10, 51, 13, 12, 46, 25, 26, 27, 11, 24, 3, 5, 14, 4, 23, 47, 37, 36, 39]

    print("Koszt trasy:")
    print(route)
    print("to")
    print(calculate_route(route, loader.get_data()))
