from Codes.Configuration import Vehicle_characteristics
from traci import lane, trafficlight
import numpy as np

class QueueLength:

    def Queue_Length_Vehicles(self, junction_id):
        QL = []
        lanes = trafficlight.getControlledLanes(junction_id)
        for lane_id in lanes:
            count_veh = lane.getLastStepHaltingNumber(lane_id)
            QL.append(count_veh*(Vehicle_characteristics['min_cap']+Vehicle_characteristics['length']))
        return QL

    def Average_Queue_Length_vehicles(self, junction_id):
        return np.average(self.Queue_Length_Vehicles(junction_id))

    def Standard_Deviation_Queue_Length_Vehicels(self, junction_id):
        return np.std(self.Queue_Length_Vehicles(junction_id))

   