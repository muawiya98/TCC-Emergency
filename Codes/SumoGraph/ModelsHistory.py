from traci import lane, trafficlight

class ModelsHistory:
    def __init__(self, all_edges, Edge_lane, Edge_Junction, lane_state):
        self.history = {key: [[], [], [], [], [], []] for key in all_edges}
        self.operations = ['Ground_Truth_Save', 'Measurement_Save', 'Kalman_Save',
                           'Soomth_Kalman_Save', 'ParticleFilter_Save', 'Soomth_ParticleFilter_Save']
        self.edges_operations = {op:{key: {"Junction": None, "Update": False, "Add": False}
                                     for key in all_edges} for op in  self.operations }
        self.Edge_Information = {key: [0, 0, 0] for key in all_edges}
        self.Edge_lane = Edge_lane
        self.Edge_Junction = Edge_Junction
        self.lane_state = lane_state

    def get_history(self):
        return self.history

    def checker(self, edge_id, junction_id, operation_name):
        if self.edges_operations[operation_name][edge_id]['Junction'] == junction_id:
            self.edges_operations[operation_name][edge_id]['Update'] = False
            self.edges_operations[operation_name][edge_id]['Add'] = True
            return False
        else:
            self.edges_operations[operation_name][edge_id]['Junction'] = junction_id
            if ((not self.edges_operations[operation_name][edge_id]['Add']) and (not self.edges_operations[operation_name][edge_id]['Update'])) \
                    or (self.edges_operations[operation_name][edge_id]['Update']):
                self.edges_operations[operation_name][edge_id]['Update'] = False
                self.edges_operations[operation_name][edge_id]['Add'] = True
                return False
            elif self.edges_operations[operation_name][edge_id]['Add']:
                self.edges_operations[operation_name][edge_id]['Add'] = False
                self.edges_operations[operation_name][edge_id]['Update'] = True
                return True

    def Ground_Truth_Save(self, edges, junction_id):
        for edge_id in edges:
            number_of_vehicles, traffic_light = self.get_number_of_vehicels_traffic_light(edge_id)
            self.Edge_Information[edge_id][0] = number_of_vehicles
            self.Edge_Information[edge_id][2] = traffic_light
            if self.checker(edge_id, junction_id,'Ground_Truth_Save'):
                self.history[edge_id][0][-1] = number_of_vehicles
            else:self.history[edge_id][0].append(number_of_vehicles)

    def Measurement_Save(self, edges, junction_id, measurements):
        for i,edge_id in enumerate(edges):
            if self.checker(edge_id, junction_id,'Measurement_Save'):
                self.history[edge_id][2][-1] = measurements[i]
            else:self.history[edge_id][2].append(measurements[i])

    def Kalman_Save(self, edges, junction_id, Estemated_numbers=None, Estemated_smooth_numbers=None):
        for i, edge_id in enumerate(edges):
            if not Estemated_numbers is None:
                self.Edge_Information[edge_id][1] = Estemated_numbers[i]
                if self.checker(edge_id, junction_id,'Kalman_Save'):
                    self.history[edge_id][1][-1] = Estemated_numbers[i]
                else:self.history[edge_id][1].append(Estemated_numbers[i])
            if not Estemated_smooth_numbers is None:
                if self.checker(edge_id, junction_id,'Soomth_Kalman_Save'):
                    self.history[edge_id][3][-1] = Estemated_smooth_numbers[i]
                else:self.history[edge_id][3].append(Estemated_smooth_numbers[i])

    def ParticleFilter_Save(self,edges, junction_id, estimated_counts=None,estimated_soomth_counts=None):
        for i, edge_id in enumerate(edges):
            if not estimated_counts is None:
                if self.checker(edge_id, junction_id, 'ParticleFilter_Save'):
                    self.history[edge_id][4][-1] = estimated_counts[i]
                else:self.history[edge_id][4].append(estimated_counts[i])
            if not estimated_soomth_counts is None:
                if self.checker(edge_id, junction_id, 'Soomth_ParticleFilter_Save'):
                    self.history[edge_id][5][-1] = estimated_soomth_counts[i]
                else:self.history[edge_id][5].append(estimated_soomth_counts[i])

    def get_number_of_vehicels_traffic_light(self, edge_id):
        try:junction_id = self.Edge_Junction[edge_id]
        except:return 0, 0
        lanes = self.Edge_lane[edge_id]
        controlled_lanes = trafficlight.getControlledLanes(junction_id)
        lane_index = controlled_lanes.index(lanes[len(lanes)//2])
        edge_state = trafficlight.getRedYellowGreenState(junction_id)[lane_index]
        edge_state = self.lane_state[edge_state]
        number_of_vehicles = 0
        for l in lanes:
            number_of_vehicles += lane.getLastStepVehicleNumber(l)
        return number_of_vehicles, edge_state