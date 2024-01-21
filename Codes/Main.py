import os
import sys
sys.path.append(os.path.abspath("."))
from Codes.Configuration import Network_Path, Methods
from Codes.Controller import Controller
import matplotlib.pyplot as plt # type: ignore
from traci import trafficlight
from sumolib import checkBinary
from traci import start
import optparse
import traci
class SUMO_ENV:
    def __init__(self):
        self.intersections = None
    def get_Options(self):
        opt_parser = optparse.OptionParser()
        opt_parser.add_option("--nogui", action="store_true",
                            default=True, help="run the commandline version of sumo")
        options, _ = opt_parser.parse_args()
        return options
    def Starting(self):
        if self.get_Options().nogui:sumoBinary = checkBinary('sumo')
        else: sumoBinary = checkBinary('sumo-gui')
        start([sumoBinary, "-c", Network_Path])
    def exit(self):
        traci.close()
        sys.stdout.flush()
    def Random_Methode(self):
        controller = Controller(self.intersections)
        controller.Run(method_name=Methods.Random)
    def Kalman_Methode_R1(self):
        controller = Controller(self.intersections)
        controller.Run(method_name=Methods.Kalman_R1)
    def Kalman_Methode_R2(self):
        controller = Controller(self.intersections)
        controller.Run(method_name=Methods.Kalman_R2)
    def Kalman_Methode_R3(self):
        controller = Controller(self.intersections)
        controller.Run(method_name=Methods.Kalman_R3)
    def Traditional_RL_Methode_R1(self):
        controller = Controller(self.intersections)
        controller.Run(method_name=Methods.Traditional_R1)
    def Traditional_RL_Methode_R2(self):
        controller = Controller(self.intersections)
        controller.Run(method_name=Methods.Traditional_R2)
    def Traditional_RL_Methode_R3(self):
        controller = Controller(self.intersections)
        controller.Run(method_name=Methods.Traditional_R3)
    def Default_Case(self):
        print("Error running method")
    def Run_Methodes(self):
        switch_dict = {
            Methods.Kalman_R1: self.Kalman_Methode_R1,
            Methods.Kalman_R2: self.Kalman_Methode_R2,
            Methods.Kalman_R3: self.Kalman_Methode_R3,
            Methods.Traditional_R1: self.Traditional_RL_Methode_R1,
            Methods.Traditional_R2: self.Traditional_RL_Methode_R2,
            Methods.Traditional_R3: self.Traditional_RL_Methode_R3,
            Methods.Random: self.Random_Methode,
            }
        for i, methode in enumerate(switch_dict.keys()):
            if i != 0: break
            self.Starting()
            self.intersections = trafficlight.getIDList()
            case_function = switch_dict.get(methode, self.Default_Case)
            case_function()
            self.exit()
if __name__ == "__main__":
    # try:
    env = SUMO_ENV()
    env.Run_Methodes()
    # except Exception as e:
    #     print(f"An exception of type {type(e).__name__} occurred.")

