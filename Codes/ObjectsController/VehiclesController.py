from Codes.Configuration import Vehicle_characteristics, HIGH_NUMBER_OF_VEHICLE, LOW_NUMBER_OF_VEHICLE
from traci import vehicle, route
from uuid import uuid4
import random
import traci
import math

class VehicleController:

    def __init__(self, incomming_edges, outcomming_edges):
        self.outcomming_edges = outcomming_edges
        self.incomming_edges = incomming_edges

    def add_vehicles(self, routes, num_veh):
        for i in range(num_veh):
            route_id = str(uuid4())
            vehicle_id = str(uuid4())
            route.add(routeID=route_id, edges=routes)
            vehicle.add(vehID='Veh'+vehicle_id, routeID=route_id)
            vehicle.setLength('Veh'+vehicle_id, Vehicle_characteristics['length'])
            vehicle.setMinGap('Veh'+vehicle_id, Vehicle_characteristics['min_cap'])

    def generate_number(self):
        A,f = 6,0.99
        B = random.randint(0, A)
        C = math.ceil(A + B * math.sin(2 * math.pi * f * traci.simulation.getTime()))
        return C

    def generate_vehicles(self, sub_episode_number):
        for c_edge in self.incomming_edges:
            for nc_edge in self.outcomming_edges:
                if (c_edge.startswith('-') and c_edge.lstrip('-') == nc_edge) or \
                        (nc_edge.startswith('-') and nc_edge.lstrip('-') == c_edge):continue
                route = [c_edge, nc_edge]
                if len(self.incomming_edges)>4:
                    number_of_vehicle = self.generate_number()
                    self.add_vehicles(route, number_of_vehicle)
                else:

                    if sub_episode_number==0:
                        if self.incomming_edges[0] in route:self.add_vehicles(route, HIGH_NUMBER_OF_VEHICLE)
                        else:self.add_vehicles(route, LOW_NUMBER_OF_VEHICLE)
                    elif sub_episode_number==1:
                        if self.incomming_edges[1] in route:self.add_vehicles(route, HIGH_NUMBER_OF_VEHICLE)
                        else:self.add_vehicles(route, LOW_NUMBER_OF_VEHICLE)
                    elif sub_episode_number==2:
                        if self.incomming_edges[2] in route:self.add_vehicles(route, HIGH_NUMBER_OF_VEHICLE)
                        else:self.add_vehicles(route, LOW_NUMBER_OF_VEHICLE)
                    elif sub_episode_number==3:
                        if self.incomming_edges[3] in route:self.add_vehicles(route, HIGH_NUMBER_OF_VEHICLE)
                        else:self.add_vehicles(route, LOW_NUMBER_OF_VEHICLE)

                    elif sub_episode_number==4:
                        if self.incomming_edges[0] in route or self.incomming_edges[1] in route:self.add_vehicles(route, HIGH_NUMBER_OF_VEHICLE)
                        else:self.add_vehicles(route, LOW_NUMBER_OF_VEHICLE)
                    elif sub_episode_number==5:
                        if self.incomming_edges[0] in route or self.incomming_edges[2] in route:self.add_vehicles(route, HIGH_NUMBER_OF_VEHICLE)
                        else:self.add_vehicles(route, LOW_NUMBER_OF_VEHICLE)
                    elif sub_episode_number==6:
                        if self.incomming_edges[0] in route or self.incomming_edges[3] in route:self.add_vehicles(route, HIGH_NUMBER_OF_VEHICLE)
                        else:self.add_vehicles(route, LOW_NUMBER_OF_VEHICLE)
                    elif sub_episode_number==7:
                        if self.incomming_edges[1] in route or self.incomming_edges[2] in route:self.add_vehicles(route, HIGH_NUMBER_OF_VEHICLE)
                        else:self.add_vehicles(route, LOW_NUMBER_OF_VEHICLE)
                    elif sub_episode_number==8:
                        if self.incomming_edges[1] in route or self.incomming_edges[3] in route:self.add_vehicles(route, HIGH_NUMBER_OF_VEHICLE)
                        else:self.add_vehicles(route, LOW_NUMBER_OF_VEHICLE)
                    elif sub_episode_number==9:
                        if self.incomming_edges[2] in route or self.incomming_edges[3] in route:self.add_vehicles(route, HIGH_NUMBER_OF_VEHICLE)
                        else:self.add_vehicles(route, LOW_NUMBER_OF_VEHICLE)

                    elif sub_episode_number==10:
                        if not self.incomming_edges[3] in route:self.add_vehicles(route, HIGH_NUMBER_OF_VEHICLE)
                        else:self.add_vehicles(route, LOW_NUMBER_OF_VEHICLE)
                    elif sub_episode_number==11:
                        if not self.incomming_edges[0] in route:self.add_vehicles(route, HIGH_NUMBER_OF_VEHICLE)
                        else:self.add_vehicles(route, LOW_NUMBER_OF_VEHICLE)
                    elif sub_episode_number==12:
                        if not self.incomming_edges[1] in route:self.add_vehicles(route, HIGH_NUMBER_OF_VEHICLE)
                        else:self.add_vehicles(route, LOW_NUMBER_OF_VEHICLE)
                    elif sub_episode_number==13:
                        if not self.incomming_edges[2] in route:self.add_vehicles(route, HIGH_NUMBER_OF_VEHICLE)
                        else:self.add_vehicles(route, LOW_NUMBER_OF_VEHICLE)
                    elif sub_episode_number==14:self.add_vehicles(route, HIGH_NUMBER_OF_VEHICLE)
                    elif sub_episode_number==15:self.add_vehicles(route, LOW_NUMBER_OF_VEHICLE)

