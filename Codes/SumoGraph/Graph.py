from Codes.SumoGraph.FixedGraph import FixedGraph
from Codes.SumoGraph.FickleGraph import FickleGraph

class Graph(FixedGraph, FickleGraph):
    def __init__(self, intersection):
        FixedGraph.__init__(self, intersection)
        FickleGraph.__init__(self, self.Edge_Lane, self.lane_state, self.Edge_Junction,
                             self.all_edges, self.Junction_Edge, self.Junction_controlledEdge)