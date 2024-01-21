import random
import math


class Dependences:
    def __init__(self):
        self.radius = 25
        self.max_cost = 100
        self.min_cost = 25

    def get_Radius(self):
        return self.radius

    def Calculate_Space(self, end_x, start_x, end_y, start_y):
        width = abs(end_x - start_x)
        height = abs(end_y - start_y)
        return width*height

    def Calculate_Distance(self, point1, point2):
        distance = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
        return distance

    def Cost_Function(self):
        return random.uniform(self.min_cost, self.max_cost)




