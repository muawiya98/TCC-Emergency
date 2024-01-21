from Codes.TrafficLightController.TrafficLightActions import Actions
from Codes.TrafficLightController.TrafficLightSignal import TrafficLightSignal
class TrafficLightsController:

    def __init__(self, intersection):
        """
        # traffic lights controller :
        to control of all traffic light signals in simulation
        """
        self.control_msg = {}
        self.tls_ids = list(intersection)
        self.tls_objects = []
        for tls_id in self.tls_ids:
            self.tls_objects.append(TrafficLightSignal(tls_id))
        self.traffic_light_signals_dic_actions = {}
        for tls_id_ in self.tls_ids:
            self.traffic_light_signals_dic_actions[tls_id_] = None

    def set_control_msg(self, msg):
        """ set new control message """
        self.control_msg = msg

    def convert_msg_to_tls_cmd(self):
        """ 
        convert control message to message that traffic light signal understand
        """
        for key in self.control_msg.keys():
            try:
                self.traffic_light_signals_dic_actions[key] = Actions(self.control_msg[key])
            except ValueError:
                self.traffic_light_signals_dic_actions[key] = None

    def send_actions_tls(self, msg):
        """ 
        msg: is dictionary contains keys is ids of tfs and values is action for each tfs
        """
        self.set_control_msg(msg)
        self.convert_msg_to_tls_cmd()
        for tls_o in self.tls_objects:
            action = self.traffic_light_signals_dic_actions[tls_o.get_id()]
            tls_o.add_cmd(action)

    def check_tls_cmds(self):
        for tls_o in self.tls_objects:
            tls_o.check_cmds_to_execute()

    def get_state_of_all_tls(self):
        print('the states of all tls: ')
        for tls_o in self.tls_objects:
            print(tls_o.get_current_state())

