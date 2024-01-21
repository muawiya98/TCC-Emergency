from Codes.Configuration import Network_Path, Methods, traffic_light_period, \
    generation_period, episode_time, Simulation_Time, TEST_STAGE, Result_Path
from Codes.TrafficLightController.TrafficLightsControler import TrafficLightsController
from Codes.RLUnit.QLearning_Algorithm.Reward import Reward as Qlearning_Reward
from Codes.ObjectsController.SumoController import SumoObjectController
from Codes.InformationProvider.InformationGeter import Infromation
from Codes.OptimizationUnit.NSGAAlgorethm import NSGA_Algorethm
from Codes.OptimizationUnit.GridBuilder import GridBuilder
from Codes.OptimizationUnit.NoiseModel import NoiseModel
from warnings import simplefilter, filterwarnings
from Codes.Results.Results import Results
from Codes.SumoGraph.Graph import Graph
from Codes.RLUnit.Agent import Agent
from numpy import random
from traci import trafficlight
import traci
import os
filterwarnings('ignore')
filterwarnings(action='once')
simplefilter('ignore', FutureWarning)


class Controller:
    def __init__(self, intersection):
        self.number_of_agent = len(intersection)
        self.tls_controller = TrafficLightsController(intersection)
        self.Agent_ids = intersection
        self.graph = Graph(intersection)
        self.results = Results(self.graph)
        self.SumoObject = SumoObjectController(self.graph.incomming_edges, self.graph.outcomming_edges)
        self.information = Infromation(self.Agent_ids)
        self.reward = Qlearning_Reward(self.information, self.graph, self.Agent_ids)
        self.grid_builder = GridBuilder(self.graph)
        self.noise_model = NoiseModel(self.grid_builder.center_of_environment, self.grid_builder.centers_of_grids,
                                      self.grid_builder.end_x, self.grid_builder.start_x,
                                      self.grid_builder.end_y, self.grid_builder.start_y)
        self.NSGA_solution = NSGA_Algorethm(self.noise_model.noise_of_grids, self.grid_builder.centers_of_grids,
                                            self.grid_builder.center_of_environment, self.grid_builder.end_x,
                                            self.grid_builder.start_x, self.grid_builder.end_y,self.grid_builder.start_y)
        self.Agents = []
    def Create_Agents(self):
        for Agent_id in self.Agent_ids:
            self.Agents.append(Agent(Agent_id, self.graph, self.reward))

    def Save_Start_State(self):
        path_start_state = Network_Path
        path_0 = path_start_state.split('.')[0]
        path_start_state = path_0+'_start_state.xml'
        traci.simulation.saveState(path_start_state)
    def Load_Start_State(self):
        path_start_state = Network_Path
        path_0 = path_start_state.split('.')[0]
        path_start_state = path_0+'_start_state.xml'
        traci.simulation.loadState(path_start_state)
    def Rest_Sumo(self):
        self.Load_Start_State()
    def Maping_Between_agents_junctions(self, actions):
        self.tls_controller.send_actions_tls(actions)
        self.tls_controller.check_tls_cmds()
    def Save_Actions_For_Edge(self):
        for i, Agent_id in enumerate(self.Agent_ids):
            edges = self.graph.Junction_controlledEdge[Agent_id]
            list_action = []
            for edge_id in edges:
                lanes = self.graph.Edge_lane[edge_id]
                controlled_lanes = trafficlight.getControlledLanes(Agent_id)
                lane_index = list(controlled_lanes).index(lanes[len(lanes) // 2])
                edge_state = trafficlight.getRedYellowGreenState(Agent_id)[lane_index]
                edge_state = self.graph.lane_state[edge_state]
                list_action.append(edge_state)
            self.graph.results_history.Actions_Save(list_action, edges)

    def Communication_With_Environment(self, method_name, step, Scenario_Type):
        Actions_dic = {}
        for i, Agent_id in enumerate(self.Agent_ids):
            if method_name is Methods.Random:
                Actions_dic[Agent_id] = random.choice([1, 2, 3, 4, 5, 6])
                self.reward.Reward_Function(Agent_id, step)
            else:
                Actions_dic[Agent_id] = self.Agents[i].get_action(step, Scenario_Type)
        self.Maping_Between_agents_junctions(Actions_dic)
        self.Save_Actions_For_Edge()

    def Run(self, method_name):
        os.makedirs(Result_Path, exist_ok=True)
        step_generation, step, sub_episode_number, episode_number = 0, 0, 0, 0
        print(method_name)
        self.Create_Agents()
        Scenario_Type = "train"
        while step < Simulation_Time:
            traci.simulationStep()
            if episode_number>=TEST_STAGE:Scenario_Type = "test"
            if step == 0: self.Save_Start_State()
            if step % traffic_light_period == 0:
                self.Communication_With_Environment(method_name, step, Scenario_Type)
            if step_generation % generation_period == 0:
                self.SumoObject.generate_object(sub_episode_number)
                sub_episode_number += 1
                step_generation = 0
            if (step+generation_period) % episode_time == 0 and step != 0:
                sub_episode_number = 0
                episode_number += 1
                self.Rest_Sumo()
            step_generation += 1
            step += 1
            # self.results.Prepare_All_Results(method_name)
        self.results.Prepare_All_Results(method_name)
