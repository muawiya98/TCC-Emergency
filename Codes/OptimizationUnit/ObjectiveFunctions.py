# from Codes.OptimizationUnit.Dependences import Dependences
import numpy as np
class ObjectiveFunction:


    def Calculate_Coverage(self, radiuses, space_env):
        coverage_rsu = sum([2*3.14*r for r in radiuses])
        return coverage_rsu / space_env

    def Calculate_Cost(self, installation, operational):
        installation = np.array(installation)
        operational = np.array(operational)
        return sum(installation+operational)

    def Calculate_Latency(self, Distances_to_AP):
        return sum(Distances_to_AP)

    def Calculate_Reliability(self, noises):
        return sum(noises)

    def Objective_Functions(self, selected_RSU, space_env):
        radiuses, installation_costs, operational_costs, Distances_to_AP, noises = [], [], [], [], []
        for rsu in selected_RSU:
            radiuses.append(rsu['radius'])
            installation_costs.append(rsu['installation_cost'])
            operational_costs.append(rsu['operational_cost'])
            Distances_to_AP.append(rsu['Distance_to_AP'])
            noises.append(rsu['noise'])
        Coverage = self.Calculate_Coverage(radiuses, space_env)
        Cost = self.Calculate_Cost(installation_costs, operational_costs)
        Latency = self.Calculate_Latency(Distances_to_AP)
        Reliability = self.Calculate_Reliability(noises)
        return [-Coverage, Cost, Latency, -Reliability]
