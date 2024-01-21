from Codes.Configuration import episode_time, traffic_light_period, Result_Path
import pandas as pd
import numpy as np
import os

class ResultsHistory:

    def __init__(self):
        self.accumulative_reward_history = {}
        self.waiting_time_history = {}
        self.action_history = {}

        self.reward_history = {}
        self.state_history = {}
        self.Q_history = {}
        self.waiting_time_history_for_edge = {}
        self.Action_history = {}

        self.density_history = {}
        self.accumulative_reward_history_per_episode = {}
        self.waiting_time_history_per_episode = {}
        self.action_history_per_episode = {}
        self.reward_history_per_episode = {}
        self.density_history_per_episode = {}

    def Actions_Save(self, action, edges):
        for i, edge in enumerate(edges):
            if not edge in self.action_history:self.action_history[edge] = [action[i]]
            else:self.action_history[edge].append(action[i])

    def Make_Results_Per_episode(self, methode_name):
        number_of_steps_per_episode = episode_time//traffic_light_period
        for key in self.accumulative_reward_history.keys():
            for i in range(0,len(self.accumulative_reward_history[key]),number_of_steps_per_episode):
                if not key in self.accumulative_reward_history_per_episode.keys():
                    self.accumulative_reward_history_per_episode[key] = [np.average(self.accumulative_reward_history[key][i:i+number_of_steps_per_episode])]
                    self.reward_history_per_episode[key] = [np.average(self.reward_history[key][i:i+number_of_steps_per_episode])]
                    self.density_history_per_episode[key] = [np.average(self.density_history[key][i:i+number_of_steps_per_episode])]
                    self.waiting_time_history_per_episode[key] = [np.average(self.waiting_time_history[key][i:i+number_of_steps_per_episode])]
                else:
                    self.accumulative_reward_history_per_episode[key].append(np.average(self.accumulative_reward_history[key][i:i+number_of_steps_per_episode]))
                    self.reward_history_per_episode[key].append(np.average(self.reward_history[key][i:i+number_of_steps_per_episode]))
                    self.density_history_per_episode[key].append(np.average(self.density_history[key][i:i+number_of_steps_per_episode]))
                    self.waiting_time_history_per_episode[key].append(np.average(self.waiting_time_history[key][i:i+number_of_steps_per_episode]))
            df = pd.DataFrame()
            df['Accumulative Reward'] = self.accumulative_reward_history_per_episode[key]
            df['Reward'] = self.reward_history_per_episode[key]
            df['Waiting Time'] = self.waiting_time_history_per_episode[key]
            df['Density'] = self.density_history_per_episode[key]
            save_path = os.path.join(Result_Path, str(methode_name) + ' Results')
            os.makedirs(save_path, exist_ok=True)
            df.to_csv(os.path.join(save_path, "Numerical Results Per Episode " + key + ".csv"), index=False)

    def Save_Results_as_CSV(self, methode_name):
        for key in self.accumulative_reward_history.keys():
            df = pd.DataFrame()
            df['Accumulative Reward'] = self.accumulative_reward_history[key]
            df['Reward'] = self.reward_history[key]
            df['Waiting Time'] = self.waiting_time_history[key]
            df['Density'] = self.density_history[key]

            df['State'] = self.state_history[key]
            df['waiting for edge'] = self.waiting_time_history_for_edge[key]
            df['Q_value'] = self.Q_history[key]
            df['Action'] = self.Action_history[key]

            save_path = os.path.join(Result_Path, str(methode_name) + ' Results')
            os.makedirs(save_path, exist_ok=True)
            df.to_csv(os.path.join(save_path, "Numerical Results Per Step " + key + ".csv"), index=False)


