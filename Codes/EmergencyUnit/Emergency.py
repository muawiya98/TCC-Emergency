from Codes.Configuration import Simulation_Time, traffic_light_period
import numpy as np
class Emergen:
    def __init__(self, intersections_id, graph):
        self.graph = graph
        self.intersections_id = intersections_id
        self.emergency_steps = {key: [] for key in self.intersections_id}
        self.emergency_edges = {key: [] for key in self.intersections_id}
        self.Make_Emergency()


    def Make_Emergency(self):
        for intersection_id in self.intersections_id:
            controlled_edge = self.graph.Junction_controlledEdge[intersection_id]
            number_of_step = Simulation_Time//traffic_light_period
            vector_length = random.randint(1, number_of_step//1000)
            self.emergency_steps[intersection_id] = np.random.randint(1, number_of_step, size=vector_length)
            self.emergency_edges[intersection_id]  = random.choices(controlled_edge, k=vector_length)




