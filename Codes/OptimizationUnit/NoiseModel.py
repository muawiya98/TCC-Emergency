import numpy as np

class NoiseModel:
    def __init__(self, center_of_environment, centers_of_grids, end_x, start_x, end_y, start_y):
        self.center_of_environment = center_of_environment
        self.centers_of_grids = centers_of_grids
        self.end_x = end_x
        self.start_x = start_x
        self.end_y = end_y
        self.start_y = start_y
        self.noise_of_grids = []
        self.sub_squares = None
        self.Noise_Distribution()

    def Point_In_Sub_Square(self, point):
        for i, sub_square in enumerate(self.sub_squares):
            sub_start_x, sub_end_x, sub_start_y, sub_end_y = sub_square
            if sub_start_x <= point[0] <= sub_end_x and sub_start_y <= point[1] <= sub_end_y:
                return i
        return -1

    def Noise_Distribution(self):
        mid_x, mid_y = self.center_of_environment
        self.sub_squares = [
            (self.start_x, mid_x, self.start_y, mid_y),  # Sub-square 0
            (mid_x, self.end_x, self.start_y, mid_y),  # Sub-square 1
            (self.start_x, mid_x, mid_y, self.end_y),  # Sub-square 2
            (mid_x, self.end_x, mid_y, self.end_y)]  # Sub-square 3

        for i, point in enumerate(self.centers_of_grids):
            index = self.Point_In_Sub_Square(point)
            if index==0:
                min_val, max_val = 10, 20
                mean = (min_val + max_val) / 2
                std_dev = (max_val - min_val) / 6
                self.noise_of_grids.append(np.random.normal(mean, std_dev, 1))
            elif index==1:
                min_val, max_val = 0, 20
                mean = (min_val + max_val) / 2
                std_dev = (max_val - min_val) / 6
                self.noise_of_grids.append(np.random.normal(mean, std_dev, 1))
            elif index==2:
                min_val, max_val = 30, 60
                mean = (min_val + max_val) / 2
                std_dev = (max_val - min_val) / 6
                self.noise_of_grids.append(np.random.normal(mean, std_dev, 1))
            elif index==3:
                self.noise_of_grids.append(np.zeros(1))


