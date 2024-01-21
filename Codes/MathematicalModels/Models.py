from Codes.MathematicalModels.ParticleFilter import ParticleFilter
from Codes.Configuration import Methods, R1, R2, R3
from Codes.MathematicalModels.KalmanModel import KalmanModel
import numpy as np

class Models:
    def __init__(self, graph, junction_id):
        self.graph = graph
        self.agent_id = junction_id
        self.edges = np.array([edges for edges in self.graph.Junction_Edge[self.agent_id]])
        self.measurements = np.array([self.graph.models_history.Edge_Information[key][0] for key in self.edges])
        self.kalman_model = KalmanModel(self.graph, self.agent_id, self.edges)
        # self.soomth_kalman_model = KalmanModel(self.graph, self.agent_id, self.edges)
        # self.particle_filter = ParticleFilter(self.graph, self.agent_id, self.edges)
        # self.soomth_particle_filter = ParticleFilter(self.graph, self.agent_id, self.edges)
        # self.Dual_EnKF = None
    def generate_random_boolean(self, prob_false=0.9):
        choices = [True, False]
        probabilities = [1 - prob_false, prob_false]
        return np.random.choice(choices, p=probabilities)
    def Run_Models(self, methode_name):
        if methode_name in [Methods.Traditional_R1, Methods.Kalman_R1]:R=R1
        elif methode_name in [Methods.Traditional_R2, Methods.Kalman_R2]:R=R2
        else:R=R3
        ground_truth = np.array([self.graph.models_history.Edge_Information[key][0] for key in self.edges])
        self.graph.models_history.Ground_Truth_Save(self.edges, self.agent_id)

        noise = np.random.normal(0, R, ground_truth.shape)
        sudden_failure = self.generate_random_boolean()
        self.measurements = ground_truth + noise if not sudden_failure else self.measurements
        self.measurements[self.measurements<0]=0
        self.measurements = np.ceil(self.measurements).astype(int)
        self.graph.models_history.Measurement_Save(self.edges, self.agent_id, self.measurements)

        self.kalman_model.Kalman_equations(methode_name, self.measurements, R)
        # self.soomth_kalman_model.Kalman_equations(methode_name, self.measurements, R, "smooth")
        # self.particle_filter.Particle_Filter(methode_name, self.measurements)
        # self.soomth_particle_filter.Particle_Filter(methode_name, self.measurements, "smooth")

