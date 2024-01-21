from Codes.Configuration import Vehicle_characteristics
from traci import lane, trafficlight
import numpy as np

class Density:

    def Density_Vehicles(self, junction_id):
        density = []
        lanes = set(trafficlight.getControlledLanes(junction_id))
        
        for lane_id in lanes:
            count_veh = lane.getLastStepHaltingNumber(lane_id)
            length_lane = lane.getLength(lane_id)
            density.append((count_veh*(Vehicle_characteristics['min_cap']+Vehicle_characteristics['length']))/length_lane)
        
        return density

    def Average_Density_Vehicles(self, junction_id):
        return np.average(self.Density_Vehicles(junction_id))

    def Standard_Deviation_Density_Vehicles(self, junction_id):
        return np.std(self.Density_Vehicles(junction_id))
