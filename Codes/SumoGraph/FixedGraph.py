from traci import trafficlight,lane
class FixedGraph:
    def __init__(self, intersection):
        self.JUNCTIONS_IDS = intersection
        self.lane_state = {'G': 1,'g':1,'r':0,'y':0}
        self.Outcomming_edges = {} # Where this edge lead
        self.Incomming_edges = {} # Whiche edges lead to this edge
        self.Edge_Lane, self.Lane_Edge = {}, {}
        self.Junction_Edge, self.Edge_Junction = {}, {}
        self.Junction_controlledEdge = {}
        self.outcomming_edges, self.incomming_edges = [], []
        self.outcomming_lanes, self.incomming_lanes = [], []
        self.all_edges = []
        self.Fill_Fixed_Information()
    def Fill_Fixed_Information(self):
        controlled_edges, not_controlled_edges = set(), set()
        set_of_incomming_lane, set_of_outcomming_lane = set(), set()
        all_lanes = set()


        for id_inter in self.JUNCTIONS_IDS:
            links = trafficlight.getControlledLinks(id_inter)
            self.Junction_Edge[id_inter] = []
            self.Junction_controlledEdge[id_inter] = []
            for ii,id_link in enumerate(links):
                incoming_lane, outcoming_lane, _ = id_link[0]
                set_of_incomming_lane.add(incoming_lane)
                set_of_outcomming_lane.add(outcoming_lane)
                all_lanes.add(incoming_lane)
                all_lanes.add(outcoming_lane)
                incoming_edge, outcoming_edge = lane.getEdgeID(incoming_lane), lane.getEdgeID(outcoming_lane)
                controlled_edges.add(incoming_edge)
                not_controlled_edges.add(outcoming_edge)

                shap_of_lane = lane.getShape(incoming_lane)
                start_point, end_point = shap_of_lane[-1], shap_of_lane[0]


                # Junction : Edge , # Edge : Junction
                if incoming_lane in (trafficlight.getControlledLanes(id_inter)):
                    self.Edge_Junction[incoming_edge] = id_inter
                    if not incoming_edge in self.Junction_Edge[id_inter]:
                        self.Junction_Edge[id_inter].append(incoming_edge)
                        self.Junction_Edge[id_inter].append(outcoming_edge)
                        self.Junction_controlledEdge[id_inter].append(incoming_edge)
                if outcoming_lane in (trafficlight.getControlledLanes(id_inter)):
                    self.Edge_Junction[outcoming_edge] = id_inter

                # Edge : Outcoming Edges
                if incoming_edge in self.Outcomming_edges.keys():
                    if not outcoming_edge in self.Outcomming_edges[incoming_edge]:
                        self.Outcomming_edges[incoming_edge].append(outcoming_edge)
                else:
                    self.Outcomming_edges[incoming_edge] = [outcoming_edge]

                # Edge : Incoming Edges
                if outcoming_edge in self.Incomming_edges.keys():
                    if not incoming_edge in self.Incomming_edges[outcoming_edge]:
                        self.Incomming_edges[outcoming_edge].append(incoming_edge)
                else:
                    self.Incomming_edges[outcoming_edge] = [incoming_edge]

        self.incomming_edges = list(controlled_edges-not_controlled_edges)
        self.outcomming_edges = list(not_controlled_edges-controlled_edges)
        self.incomming_lanes = list(set_of_incomming_lane)
        self.outcomming_lanes = list(set_of_outcomming_lane)
        self.all_edges = list(set(list(controlled_edges)+list(not_controlled_edges)))
        # Lane: Edge; Edge: Lane
        for my_lane in list(all_lanes):
            my_edge = lane.getEdgeID(my_lane)
            self.Lane_Edge[my_lane] = my_edge
            if my_edge in self.Edge_Lane.keys():
                self.Edge_Lane[my_edge].append(my_lane)
            else:
                self.Edge_Lane[my_edge] = [my_lane]