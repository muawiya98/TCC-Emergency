from Codes.Configuration import Vehicle_characteristics, Green_red_period, Methods, Q
from Codes.TrafficLightController.TrafficLightActions import Actions
from traci import edge
import numpy as np
class KalmanModel:
    def __init__(self, graph, junction_id, edges):
        self.graph = graph
        self.junction_id = junction_id
        self.edges = edges
        self.initial_guess = np.array([self.graph.models_history.Edge_Information[key][1] for key in self.edges])
        self.x_estimate = self.initial_guess
        self.x_predict, self.large_variances = self.initial_guess, 300
        self.matrixes_initilazation()
    def matrixes_initilazation(self):
        self.P = np.diag(np.ones(len(self.initial_guess)) * self.large_variances)
        self.P_predict = self.P
        self.F = np.eye(len(self.initial_guess))
        self.Q = np.diag(np.ones(len(self.initial_guess)) * Q)
        self.R = np.diag(np.ones(len(self.initial_guess)) * Q)
        self.H = np.eye(len(self.initial_guess))
    def prediction(self, kalman_type="" ,action=None):
        A = self.graph.Get_Estimation_parameters(self.junction_id, self.edges, self.graph.Outcomming_edges,
                                                 kalman_type, action)
        self.x_predict = self.x_estimate @ A
        self.x_predict[self.x_predict < 0] = 0
        return np.ceil(self.x_predict).astype(int)
    def measurement(self, measurements, R):
        self.R = np.diag(np.ones(len(self.initial_guess)) * R)
        measurements[measurements < 0] = 0
        self.P_predict = self.H @ self.P @ self.H.T + self.Q
        K = self.P_predict @ self.H.T @ np.linalg.inv(self.H @ self.P_predict @ self.H.T + self.R)
        self.x_estimate = self.x_predict + K @ (measurements - self.H @ self.x_predict)
        self.P = (np.eye(len(self.x_estimate)) - K @ self.H) @ self.P_predict
        self.x_estimate = np.ceil(self.x_estimate).astype(int)
        self.x_estimate[self.x_estimate < 0] = 0
        return self.x_estimate
    def Kalman_equations(self, methode, measurements, R, kalman_type=""):
        RL_State = np.array(self.measurement(measurements, R))
        Estemated_numbers = None if kalman_type == "smooth" else RL_State
        Estemated_smooth_numbers = RL_State if kalman_type == "smooth" else None
        self.graph.models_history.Kalman_Save(self.edges, self.junction_id, Estemated_numbers=Estemated_numbers,
                                             Estemated_smooth_numbers=Estemated_smooth_numbers)
        self.prediction(kalman_type)
        if not kalman_type=="smooth":
            if methode in [Methods.Traditional_R1, Methods.Traditional_R2, Methods.Traditional_R3]:
                self.graph.set_RL_State(RL_State, self.junction_id)
            else:
                for action in Actions:
                    if not action is Actions.Switch_phase:
                        RL_State = np.concatenate((RL_State, self.prediction(kalman_type, action)))
                self.graph.set_RL_State(RL_State, self.junction_id)
