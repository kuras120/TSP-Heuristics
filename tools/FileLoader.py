import math
import time


class FileLoader:
    def __init__(self):
        self.__coords = []
        self.__final_matrix = []
        self.__status = ""
        self.__length = 0

    def load(self, filename, status):
        __file = open(filename)
        self.__status = status

        #Case lower diag
        if "LOWER_DIAG" in self.__status:
            line = __file.read().split()
            self.__length = int(line.pop(0))
            counter = 0
            for i in range(1, self.__length):
                temp = []
                for j in range(i):
                    temp.append(int(line[counter]))
                    counter += 1
                self.__coords.append(temp)
            temp = []
            temp_counter = counter
            for k in range(counter, temp_counter+self.__length):
                temp.append(int(line[k]))
            self.__coords.append(temp)
            self.__data_processing()

            __file.close()

        # TODO Blad dla wiekszych instancji (nie splituje wszystkich linii).
        #Case full matrix
        if "FULL_MATRIX" in self.__status:
            line = __file.read()
            line = line.split()
            self.__length = int(line.pop(0))
            counter = 0
            for i in range(self.__length):
                temp = []
                for j in range(self.__length):
                    temp.append(int(line[counter]))
                    counter += 1
                self.__coords.append(temp)
            self.__data_processing()

            __file.close()

        #Case coords euclides
        if "COORDS" in self.__status:
            lines = __file.readlines()
            self.__length = int(lines.pop(0))
            if lines.__len__() != self.__length:
                raise Exception("Wrong number of coordinates detected.")
            for elem in lines:
                line = elem.split()
                self.__coords.append([float(line[1]), float(line[2])])

            self.__data_processing()

            __file.close()

    def __data_processing(self):
        self.__final_matrix = [[0 for x in range(self.__length)] for y in range(self.__length)]

        if "LOWER_DIAG" in self.__status:
            counter = 1
            for i in range(self.__length):
                for j in range(counter, self.__length):
                    temp = self.__coords[j]
                    self.__coords[i].append(temp[i])
                counter += 1
            self.__final_matrix = self.__coords

        elif "FULL_MATRIX" in self.__status:
            self.__final_matrix = self.__coords

        elif "COORDS_EUC" in self.__status:
            for i in range(self.__coords.__len__()):
                for j in range(self.__coords.__len__()):
                    self.__final_matrix[i][j] = \
                        round(math.sqrt(math.pow(self.__coords[j][0] - self.__coords[i][0], 2) +
                                        math.pow(self.__coords[j][1] - self.__coords[i][1], 2)))

        elif "COORDS_GEO" in self.__status:
            R = 6378.388
            PI = 3.141592
            for i in range(self.__coords.__len__()):
                for j in range(self.__coords.__len__()):
                    lat1, lon1, lat2, lon2 = \
                        self.to_radians(PI, self.__coords[j][0]), self.to_radians(PI, self.__coords[j][1]), \
                        self.to_radians(PI, self.__coords[i][0]), self.to_radians(PI, self.__coords[i][1])

                    q1 = math.cos(lon1 - lon2)
                    q2 = math.cos(lat1 - lat2)
                    q3 = math.cos(lat1 + lat2)

                    distance = round(R * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)

                    self.__final_matrix[i][j] = distance

    def to_radians(self, PI, coordinate):
        deg = round(coordinate)
        min = coordinate - deg
        rad = PI * (deg + 5.0 * min / 3.0) / 180.0
        return rad

    def write(self, filename):
        __file = open(filename, 'w+')
        for elem in self.__final_matrix:
            elem = elem.__str__().replace('[', '')
            elem = elem.__str__().replace(']', '')
            elem = elem.__str__().replace('\'', '')
            elem = elem.__str__().replace(',', '')
            elem = elem.__str__().replace('-1', '0')
            __file.write(elem + '\n')

        __file.close()

    def print_data(self):
        iterator = 0
        for elem in self.__final_matrix:
            print('\n'+ iterator.__str__() + " " + elem.__str__() + '\n')
            iterator += 1

    def get_data(self):
        return self.__final_matrix

    def get_number_of_cities(self):
        return self.__length


if __name__ == "__main__":
    loader = FileLoader()
    loader.load("test/TSP/gr96.tsp", "COORDS_GEO")
