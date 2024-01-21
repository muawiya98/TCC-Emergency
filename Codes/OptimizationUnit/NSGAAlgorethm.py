from Codes.OptimizationUnit.ObjectiveFunctions import ObjectiveFunction
from Codes.OptimizationUnit.Dependences import Dependences
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
import numpy as np

class NSGAAlgorethm(Problem):

    def __init__(self, noise_of_grids, centers_of_grids, AggregationPoint,
                 end_x, start_x, end_y, start_y):
        self.noise_of_grids = noise_of_grids
        self.centers_of_grids = centers_of_grids
        self.AggregationPoint = AggregationPoint
        self.end_x, self.start_x, self.end_y, self.start_y = end_x, start_x, end_y, start_y
        self.dependences = Dependences()
        self.env_space = self.dependences.Calculate_Space(end_x, start_x, end_y, start_y)
        self.Objective_Function  =ObjectiveFunction()
        self.number_RSU = len(self.centers_of_grids)
        self.Roadside_units = [
            {"position": g_center,
             "radius": self.dependences.get_Radius(),
             "noise": g_noise,
             "Distance_to_AP": self.dependences.Calculate_Distance(g_center,self.AggregationPoint),
             "installation_cost": self.dependences.Cost_Function(),
             "operational_cost": self.dependences.Cost_Function()}
            for g_center, g_noise in zip(self.centers_of_grids, self.noise_of_grids)
        ]
        super().__init__(n_var=self.number_RSU, n_obj=4, n_constr=0, xl=0, xu=1, elementwise_evaluation=True)

    def _evaluate(self, solution_, out, *args, **kwargs):
        results = []
        array_after_round = solution_.round()
        maskes = array_after_round.astype(bool)
        for mask in maskes:
            if not np.any(mask):
                mask = np.logical_not(mask)
            selected_RSU = [Roadside for Roadside, flag in zip(self.Roadside_units, mask) if flag]
            results.append(self.Objective_Function.Objective_Functions(selected_RSU, self.env_space))
        out["F"] = np.array(results)


def NSGA_Algorethm(noise_of_grids, centers_of_grids, AggregationPoint, end_x, start_x, end_y, start_y):
  problem = NSGAAlgorethm(noise_of_grids, centers_of_grids, AggregationPoint, end_x, start_x, end_y, start_y)
  algorithm = NSGA2(pop_size=20)
  stop_criteria = ('n_gen', 20)
  res = minimize(problem, algorithm, termination= stop_criteria)
  pareto_front = res.X
  random_index = np.random.choice(len(pareto_front))
  selected_solution = pareto_front[random_index]
  return selected_solution.round().astype(bool)
