import numpy as np

class State:
    def __init__(self, graph, information):
        self.graph = graph
        self.information = information
        self.low = 0
        self.high = 1

    def get_state(self, agent_id):
        edges = self.graph.Junction_controlledEdge[agent_id]
        waiting_time = self.information.Actual_Waiting(edges)
        edges = np.array([edges for edges in self.graph.Junction_Edge[agent_id]])
        ground_truth = np.array([self.graph.models_history.Edge_Information[key][0] for key in edges])
        self.graph.models_history.Ground_Truth_Save(edges, agent_id)
        maximum = max(waiting_time)
        minimum = min(waiting_time)
        threshold = ((maximum-minimum)/2)+minimum
        RLState = []
        for i, n in enumerate(waiting_time):
            if n>=threshold:RLState.append(self.high)
            else:RLState.append(self.low)
        return RLState, waiting_time