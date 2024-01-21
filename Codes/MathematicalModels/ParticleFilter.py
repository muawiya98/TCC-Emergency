from Codes.Configuration import particle_variance, Vehicle_characteristics, \
    Green_red_period, Methods
from Codes.TrafficLightController.TrafficLightActions import Actions
from traci import edge
import numpy as np
class ParticleFilter:
    def __init__(self, graph, junction_id, edges):
        self.graph = graph
        self.junction_id = junction_id
        self.edges = edges
        self.num_particles, self.num_roads = 100, len(self.edges)
        self.particles = np.array([np.random.randint(0, 50, self.num_particles) for _ in range(self.num_roads)])
        self.weights = np.array([np.ones(self.num_particles) / self.num_particles for _ in range(self.num_roads)])

    def Particle_Filter_per_Edge(self, index, measurements):
        # self.particles[index] = self.particles[index] + np.random.normal(0, 2, self.num_particles)
        likelihoods = np.exp(-0.5 * ((measurements[index] - self.particles[index]) ** 2) / particle_variance)
        self.weights[index] = self.weights[index] * likelihoods
        self.weights[index] = self.weights[index] / sum(self.weights[index]) if sum(self.weights[index]) != 0 else self.weights[index]
        if sum(self.weights[index]) == 0:
            indices = np.random.choice(np.arange(self.num_particles), size=self.num_particles)
        else:
            indices = np.random.choice(np.arange(self.num_particles), size=self.num_particles, p=self.weights[index])
        self.particles[index] = self.particles[index][indices]

    def prediction(self, particle_type="", action=None):
        for index in range(self.num_roads):
            self.particles[index] = self.particles[index] + np.random.normal(0, 2, self.num_particles)
        A = self.graph.Get_Estimation_parameters(self.junction_id, self.edges, self.graph.Outcomming_edges,
                                                 particle_type, action)
        my_particles = self.particles.copy()
        for i in range(self.num_particles):
            my_particles[:, i] = A @ my_particles[:, i]
        if action is None:
            self.particles = my_particles.copy()
        else:
            x = np.array([np.mean(my_particles[i]) for i in range(self.num_roads)])
            return x

    def measurement(self, measurements):
        for i in range(self.num_roads):
            self.Particle_Filter_per_Edge(index=i, measurements=measurements)
    def Particle_Filter(self, methode, measurements, particle_type=""):
        self.prediction(particle_type)
        self.measurement(measurements)
        self.weights = [np.ones(self.num_particles) / self.num_particles for _ in range(self.num_roads)]
        estimated_counts = np.array([np.mean(self.particles[i]) for i in range(self.num_roads)])
        estimated_counts[estimated_counts < 0] = 0
        estimated_count = None if particle_type == "smooth" else np.ceil(estimated_counts).astype(int)
        estimated_smooth_count = np.ceil(estimated_counts).astype(int) if particle_type == "smooth" else None
        self.graph.models_history.ParticleFilter_Save(self.edges, self.junction_id, estimated_counts=estimated_count,
                                                      estimated_soomth_counts=estimated_smooth_count)
        if not particle_type == "smooth":
            RL_State = estimated_counts
            if methode in [Methods.Traditional_R1, Methods.Traditional_R2, Methods.Traditional_R3]:
                self.graph.set_RL_State(RL_State, self.junction_id)
            else:
                for action in Actions:
                    if not action is Actions.Switch_phase:
                        RL_State = np.concatenate((RL_State, self.prediction(particle_type, action)))
                self.graph.set_RL_State(RL_State, self.junction_id)
