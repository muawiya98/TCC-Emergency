from Codes.Configuration import Vehicle_characteristics, Green_red_period
from Codes.TrafficLightController.TrafficLightActions import Actions
from Codes.SumoGraph.ResultsHistory import ResultsHistory
from Codes.SumoGraph.ModelsHistory import ModelsHistory
from traci import edge, lane, trafficlight
import numpy as np
class FickleGraph:
    def __init__(self, Edge_lane, lane_state, Edge_Junction, all_edges,
                 Junction_Edge, Junction_controlledEdge):
        self.models_history = ModelsHistory(all_edges, Edge_lane, Edge_Junction, lane_state)
        self.Junction_controlledEdge = Junction_controlledEdge
        self.results_history = ResultsHistory()
        self.Edge_Junction = Edge_Junction
        self.Junction_Edge = Junction_Edge
        self.lane_state = lane_state
        self.Edge_lane = Edge_lane
        self.all_edges = all_edges
        self.RL_State = {}

    def set_RL_State(self, RL_State, junction_id):
        self.RL_State[junction_id] = RL_State
    def get_RL_State(self, junction_id):
        return self.RL_State[junction_id]

    def get_state_base_action(self, action, junction_id, edges):
        programs = trafficlight.getAllProgramLogics(junction_id)
        if action == Actions.N_S_open or action == Actions.E_W_open:
            phases1 = programs[2].phases
            if action == Actions.N_S_open:states = phases1[0].state
            else:states = phases1[2].state
        else:
            phases2 = programs[1].phases
            if action == Actions.N_open: states = phases2[0].state
            elif action == Actions.E_open: states = phases2[2].state
            elif action == Actions.S_open: states = phases2[4].state
            else:states = phases2[6].state
        controlled_lanes = trafficlight.getControlledLanes(junction_id)
        States = []
        for edge_id in edges:
            lanes = self.Edge_lane[edge_id]
            try:
                lane_index = controlled_lanes.index(lanes[len(lanes)//2])
                edge_state = states[lane_index]
                edge_state = self.lane_state[edge_state]
            except:edge_state = 0
            States.append(edge_state)
        return np.array(States)
    def Claculate_Number_of_Vehicels_Outside_Lane(self, edge_id, number_of_vehicles):
        max_distance_from_the_signal = number_of_vehicles * (
                    Vehicle_characteristics['length'] + Vehicle_characteristics['min_cap'])
        if max_distance_from_the_signal == 0: return 0
        traffic_green_light_period = Green_red_period
        speed = edge.getLastStepMeanSpeed(edge_id)
        if speed == 0: return 0
        total_pass_time = max_distance_from_the_signal / speed
        flow_ratio = traffic_green_light_period / total_pass_time
        flow_ratio = 1 if flow_ratio >= 1 else flow_ratio
        number_of_cars_that_will_pass = number_of_vehicles * flow_ratio
        return flow_ratio # round(number_of_cars_that_will_pass)

    def Get_Estimation_parameters(self, junction_id, edges, Outcomming_edges, estimation_type="", action=None):
        if not action is None:States = self.get_state_base_action(action, junction_id, edges)
        else:States = np.array([self.models_history.Edge_Information[key][2] for key in edges])
        if estimation_type == "soomth":return np.eye(States.shape[0])
        A = np.eye(States.shape[0])
        indexes = np.where(States == 1)[0]
        for i, edge_id in enumerate(edges[indexes]):
            number_of_vehicles = edge.getLastStepVehicleNumber(edge_id)
            flow_ratio = self.Claculate_Number_of_Vehicels_Outside_Lane(edge_id, number_of_vehicles)
            lanes = self.Edge_lane[edge_id]
            par = []
            for l in lanes:
                x = (lane.getLastStepVehicleNumber(l) * flow_ratio) / number_of_vehicles if number_of_vehicles !=0 else 0
                par.append(x)
            for k, l in enumerate(lanes):
                if k!=0 or k!=(len(lanes)-1):par[k] = par[k] + (par[0]/2) + (par[-1]/2)
                else:par[k] = par[k]/2
            edges_related = np.where(np.isin(edges, Outcomming_edges[edge_id]))[0]
            if edges_related.size == 0:continue
            for k,j in enumerate(edges_related):
                A[j, indexes[i]] = par[k] # flow_ratio/3
        return A