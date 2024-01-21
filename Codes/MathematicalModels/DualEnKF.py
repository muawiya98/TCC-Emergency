from Codes.Configuration import Vehicle_characteristics, traffic_light_period, \
    Methods, Q, R1, R2, R3
from Codes.TrafficLightController.TrafficLightActions import Actions
from traci import edge
import numpy as np
class DualEnKF:
    def __init__(self, graph, junction_id):
        self.graph = graph
        self.junction_id = junction_id
        self.edges = np.array([edges for edges in self.graph.Junction_Edge[self.junction_id]])
        self.measurements = np.array([self.graph.Edge_Information[key][0] for key in self.edges])
        self.initial_guess = np.array([self.graph.Edge_Information[key][1] for key in self.edges])
        self.x_estimate = self.initial_guess
        self.Ns = 100
        self.Np = 50
        self.dim_state = len(self.x_estimate)
        self.dim_param = len(self.x_estimate)*3
        self.num_time_steps = 5
        self.matrixes_initilazation()

    def matrixes_initilazation(self):
        self.X = np.random.randn(self.dim_state, self.Ns)
        self.Theta = np.random.randn(self.dim_param, self.Np)
        self.Theta_mean = np.mean(self.Theta, axis=1)
        self.H = np.random.randn(self.dim_state, self.dim_param)
        self.Q = np.eye(self.dim_state)
        self.R = np.eye(self.dim_state)

    def Model(self, state, parameters):
        return state + np.dot(self.H, parameters)

    def Dual_EnKF(self,):
        for t in range(self.num_time_steps):
            Observations = np.random.randn(self.dim_state)
            X_pred = np.zeros((self.dim_state, self.Ns))
            for i in range(self.Ns):
                print(np.random.multivariate_normal(np.zeros(self.dim_state), Q).shape)
                X_pred[:, i] = self.Model(self.X[:, i], self.Theta_mean) + np.random.multivariate_normal(np.zeros(self.dim_state), Q)

            print("Predicted State Ensemble (X_pred):")
            print(X_pred)

            Theta_pred = np.zeros((self.dim_param, self.Np))
            for i in range(self.Np):
                Theta_pred[:, i] = self.Theta[:, i] + np.random.multivariate_normal(np.zeros(self.dim_param), self.Q)

            print("Predicted Parameter Ensemble (Theta_pred):")
            print(Theta_pred)

            Y_obs = Observations + np.random.multivariate_normal(np.zeros(self.dim_state), self.R)  # Add measurement noise
            X_pred_mean = np.mean(X_pred, axis=1)
            P_pred = np.cov(X_pred)
            K = np.dot(np.dot(P_pred, self.H.T), np.linalg.inv(np.dot(np.dot(self.H, P_pred), self.H.T) + self.R))
            for i in range(self.Ns):
                self.X[:, i] = X_pred[:, i] + np.dot(K, Y_obs - np.dot(self.H, X_pred[:, i]))

            print("Updated State Ensemble (X):")
            print(self.X)

            Theta_pred_mean = np.mean(Theta_pred, axis=1)
            P_theta_pred = np.cov(Theta_pred)
            K_theta = np.dot(np.dot(P_theta_pred, self.H.T), np.linalg.inv(np.dot(np.dot(self.H, P_theta_pred), self.H.T) + self.R))
            for i in range(self.Np):
                self.X_mean = np.mean(X_pred, axis=1)
                self.X_pred_i = self.Model(self.X_mean, Theta_pred[:, i])
                self.Theta[:, i] = Theta_pred[:, i] + np.dot(K_theta, Y_obs - np.dot(self.H, self.X_pred_i))

            print("Updated Parameter Ensemble (Theta):")
            print(self.Theta)

            print("\n")