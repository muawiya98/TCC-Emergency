from traci import lane

class GridBuilder:

    def __init__(self, graph, grid_size=10):
        self.graph = graph
        self.grid_size = grid_size
        self.end_x, self.start_x, self.end_y, self.start_y = self.Starting_Coordinates()
        self.Get_Centers_Of_Grids()

    def Starting_Coordinates(self):
        incomming_edges = self.graph.incomming_edges
        Xs, Ys = [], []
        for edge_id in incomming_edges:
            lane_id = self.graph.Edge_lane[edge_id][0]
            points = lane.getShape(lane_id)
            e_point, s_point = points[0], points[-1]
            Xs.append(e_point[0])
            Xs.append(s_point[0])
            Ys.append(e_point[1])
            Ys.append(s_point[1])
        max_y, min_y = max(Ys), min(Ys)
        max_x, min_x = max(Xs), min(Xs)
        return int(max_x), int(min_x), int(max_y), int(min_y)

    def Build_Grid(self):
        self.center_of_environment = (((self.start_x + self.end_x) / 2), ((self.start_y + self.end_y) / 2))
        grids = []
        for y in range(self.start_y, self.end_y, self.grid_size):
            for x in range(self.start_x, self.end_x, self.grid_size):
                grid = {'x_start': x,'y_start': y,
                        'x_end': min(x + self.grid_size, self.end_x),
                        'y_end': min(y + self.grid_size, self.end_y)}
                grids.append(grid)
        return grids

    def Find_Square_Center(self, grid):
        start_x = grid['x_start']
        end_x = grid['x_end']
        start_y = grid['y_start']
        end_y = grid['y_end']
        center_x = (start_x + end_x) / 2
        center_y = (start_y + end_y) / 2
        return center_x, center_y

    def Get_Centers_Of_Grids(self):
        grids = self.Build_Grid()
        centers_of_grids = []
        for grid in grids:
            centers_of_grids.append(self.Find_Square_Center(grid))
        self.centers_of_grids = centers_of_grids





