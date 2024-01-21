from traci import vehicle, lane, trafficlight, edge
import numpy as np
class WaitingTime:
    
    def __init__(self, Agent_ids):
        self.Agent_ids = Agent_ids
        self.inti_vehicles_waiting_time = {}
        self.vehicles_waiting_time = {}
        # for agent_id in self.Agent_ids:
        #     vehicles = self.get_vehicles(agent_id)
        #     waiting_time = self.Waiting_Time_Vehicles(vehicles)
        #     self.inti_vehicles_waiting_time[agent_id] = [vehicles, waiting_time]
    
    def get_vehicles(self, junction_id):
        lane_ids = trafficlight.getControlledLanes(junction_id)
        vehicles = []
        for lane_id in lane_ids:
            lane_vehicles = list(lane.getLastStepVehicleIDs(lane_id))
            if len(lane_vehicles) <= 0:continue
            vehicles += lane_vehicles
        return vehicles
    
    def Waiting_Time_Vehicles(self, edges_id):
        waiting_time_vehicles = []
        for id in edges_id:
            w_t_v = []
            vehicles = edge.getLastStepVehicleIDs(id)
            if len(vehicles) > 0:
                for veh in vehicles:
                    try:w_t_v.append(vehicle.getWaitingTime(veh))
                    except:pass
                if not len(w_t_v)>0:w_t_v=[0]
                waiting_time_vehicles.append(max(w_t_v))
                # waiting_time_vehicles.append(max(list(map(lambda veh: vehicle.getWaitingTime(veh), vehicles))))
            else:waiting_time_vehicles.append(0)
        return waiting_time_vehicles
    
    def Actual_Waiting(self, edges_id):
        waiting_time = self.Waiting_Time_Vehicles(edges_id)
        return waiting_time
    
        # self.vehicles_waiting_time[junction_id] = [vehicles, waiting_time]
        # vehicles = list(set(self.inti_vehicles_waiting_time[junction_id][0]) -
        #                 set(self.vehicles_waiting_time[junction_id][0]))
        # waiting_times = []
        # for id in vehicles:
        #     waiting_times.append(self.inti_vehicles_waiting_time[junction_id][1][self.inti_vehicles_waiting_time[junction_id][0].index(id)])
        # self.inti_vehicles_waiting_time[junction_id] = self.vehicles_waiting_time[junction_id]
        # return waiting_times
    
    def Average_Waiting_Time_Vehicles(self, waiting_time_vehicles):
        if len(waiting_time_vehicles) > 0:
            average_waiting_time = np.average(waiting_time_vehicles)
            return average_waiting_time
        return 0
    
    def Standard_Deviation_Waiting_Time_Vehicles(self, waiting_time_vehicles):
        if len(waiting_time_vehicles) > 0:
            std_dev_waiting_time = np.std(waiting_time_vehicles)
            return std_dev_waiting_time
        return 0

    def Reward_Info(self, edges_id=None):
        waiting_time_vehicles = self.Actual_Waiting(edges_id)
        std = self.Standard_Deviation_Waiting_Time_Vehicles(waiting_time_vehicles)
        avg = self.Average_Waiting_Time_Vehicles(waiting_time_vehicles)
        return avg, std

