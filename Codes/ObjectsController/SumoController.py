from Codes.ObjectsController.PedestriansController import PedestrianController
from Codes.ObjectsController.VehiclesController import VehicleController

class SumoObjectController(VehicleController,PedestrianController):
    
    def __init__(self,incomming_edges,outcomming_edges):
        VehicleController.__init__(self,incomming_edges,outcomming_edges)
        PedestrianController.__init__(self)

    def generate_object(self,sub_episode_number):
        self.generate_vehicles(sub_episode_number)