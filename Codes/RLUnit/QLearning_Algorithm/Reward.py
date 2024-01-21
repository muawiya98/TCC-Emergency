import numpy as np 

class Reward:
    def __init__(self, information, graph, Agent_ids):
        self.information = information
        self.graph = graph
        self.previous_waiting_time = {key: 0 for key in Agent_ids}

    def Reward_Function(self, agent_id, vehicles=None):
        # if not agent_id in self.graph.results_history.waiting_time_history.keys():
        #     p_waiting_time = self.previous_waiting_time[agent_id]
        # else:
        #     p_waiting_time = self.graph.results_history.waiting_time_history[agent_id][-1]
        edges = self.graph.Junction_controlledEdge[agent_id]
        waiting_time, std_waiting_time = self.information.Reward_Info(edges)
        waiting_time_, std_waiting_time_ = 1/waiting_time, 1/std_waiting_time
        # reward = - 1/(1+np.exp(-((0.4*std_waiting_time)+(0.6*waiting_time))))
        reward = np.tanh((0.65*std_waiting_time_) + (0.35*waiting_time_))
        # self.previous_waiting_time[agent_id] = waiting_time
        density = self.information.Average_Density_Vehicles(agent_id)
        if not agent_id in self.graph.results_history.waiting_time_history.keys():
            self.graph.results_history.waiting_time_history[agent_id] = [waiting_time]
            self.graph.results_history.reward_history[agent_id] = [reward]
            self.graph.results_history.accumulative_reward_history[agent_id] = [reward]
            self.graph.results_history.density_history[agent_id] = [density]
        else:
            self.graph.results_history.waiting_time_history[agent_id].append(waiting_time)
            self.graph.results_history.reward_history[agent_id].append(reward)
            self.graph.results_history.accumulative_reward_history[agent_id].\
                append(sum(self.graph.results_history.reward_history[agent_id]))
            self.graph.results_history.density_history[agent_id].append(density)
        return reward