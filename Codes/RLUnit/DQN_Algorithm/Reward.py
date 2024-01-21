from Codes.Configuration import traffic_light_period, WINDOW_SIZE, \
    episode_time, W_Short_term
import numpy as np
class Reward:
    def __init__(self, information, graph, Agent_ids):
        self.information = information
        self.graph = graph
        self.previous_waiting_time = {key: 0 for key in Agent_ids}

    def Short_Term_Reward(self, Agent_id, vehicles=None):
        p_waiting_time = self.previous_waiting_time[Agent_id]
        waiting_time = self.information.Average_Waiting_Time_Vehicles(Agent_id, vehicles)
        reward = p_waiting_time - waiting_time
        self.previous_waiting_time[Agent_id] = waiting_time
        if not Agent_id in self.graph.results_history.waiting_time_history.keys():
            self.graph.results_history.waiting_time_history[Agent_id] = [waiting_time]
        else:
            self.graph.results_history.waiting_time_history[Agent_id].append(waiting_time)
        return np.tanh(reward)
    def Long_Term_Reward(self, Agent_id, vehicles=None):
        # waiting_time = self.information.Average_Waiting_Time_Vehicles(Agent_id, vehicles)
        # self.graph.waiting_time_history[Agent_id].append(waiting_time)
        reward = np.average(self.graph.results_history.waiting_time_history[Agent_id][-WINDOW_SIZE:])
        # self.graph.set_waiting_time_history(Agent_id)
        return reward
    def Reward_Function(self, Agent_id, step, vehicles=None):
        # if step + traffic_light_period == (episode_time * ((step + traffic_light_period) // episode_time)):
        reward_1 = self.Short_Term_Reward(Agent_id, vehicles)
        if (step % (episode_time+1)) // traffic_light_period >= WINDOW_SIZE:
            reward_2 = self.Long_Term_Reward(Agent_id, vehicles)
            reward = (W_Short_term * reward_1) + ((1-W_Short_term) * reward_2)
        else:reward = reward_1
        density = self.information.Average_Density_Vehicles(Agent_id)
        if not Agent_id in self.graph.results_history.reward_history.keys():
            self.graph.results_history.reward_history[Agent_id] = [reward]
            self.graph.results_history.accumulative_reward_history[Agent_id] = [reward]
            self.graph.results_history.density_history[Agent_id] = [density]
        else:
            self.graph.results_history.reward_history[Agent_id].append(reward)
            self.graph.results_history.accumulative_reward_history[Agent_id].append(sum(self.graph.results_history.reward_history[Agent_id]))
            self.graph.results_history.density_history[Agent_id].append(density)
        return reward
