from Codes.TrafficLightController.TrafficLightActions import Actions
from Codes.Configuration import Yellow_period, Green_red_period
from traci._trafficlight import Logic , Phase
from traci import trafficlight
import traci

class TrafficLightSignal:

    def __init__(self, id_traffic_light):
        self.id_traffic_light = id_traffic_light
        self.duration = Green_red_period
        self.duration_switch = Yellow_period
        self.default_program = '2'
        self.id_protected_program = '10'
        self.queue_cmd = []
        self.add_program_permatied(self.default_program)
        self.add_program(self.id_protected_program)


    def get_id(self):
        return self.id_traffic_light

    def get_current_state(self):
        return trafficlight.getRedYellowGreenState(self.id_traffic_light)

    def get_current_phase(self):
        return trafficlight.getPhase(self.id_traffic_light)

    def get_current_program(self):
        return trafficlight.getProgram(self.id_traffic_light)

    def switch_to_program(self, id_program):
        trafficlight.setProgram(self.id_traffic_light, id_program)

    def set_phase(self, index_phase):
        traci.trafficlight.setPhase(self.get_id(), index_phase)

    def add_program(self, id_program):
        def make_states(state_, g_duration, y_duration):
            states_ = []
            durations_ = []
            size_wid = len(state_) // 4
            green_window = size_wid * 'G'
            yellow_window = size_wid * 'y'
            red_state = len(state_) * 'r'
            red_state = list(red_state)
            for i in range(4):
                new_state = list(red_state)
                new_state[i * size_wid:i * size_wid + size_wid] = green_window
                green_state = ''.join(new_state)
                states_.append(green_state)
                durations_.append(g_duration)

                new_state[i * size_wid:i * size_wid + size_wid] = yellow_window
                yellow_state = ''.join(new_state)
                states_.append(yellow_state)
                durations_.append(y_duration)
            return states_, durations_

        state = self.get_current_state()
        states, durations = make_states(state, self.duration, self.duration_switch)

        phases = []
        for i in range(len(states)):
            phases.append(Phase(durations[i], states[i]))

        program = Logic(id_program, 0, 0, phases)
        traci.trafficlight.setProgramLogic(self.id_traffic_light, program)
    def add_program_permatied(self, id_program):
        def make_states(state_, g_duration, y_duration):
            states_ = []
            durations_ = []
            size_wid = len(state_) // 4
            green_window = (size_wid-1) * 'G'
            green_window = green_window+'r'
            yellow_window = size_wid * 'y'
            red_state = len(state_) * 'r'
            red_state = list(red_state)
            temp = 3
            for i in range(2):
                new_state = list(red_state)
                new_state[i * size_wid:i * size_wid + size_wid] = green_window
                new_state[(i * size_wid)+2*size_wid:((i * size_wid)+2*size_wid)+size_wid] = green_window
                green_state = ''.join(new_state)
                states_.append(green_state)
                durations_.append(g_duration)

                new_state[i * size_wid:i * size_wid + size_wid] = yellow_window
                new_state[(i * size_wid)+2*size_wid:((i * size_wid)+2*size_wid)+size_wid] = yellow_window
                yellow_state = ''.join(new_state)
                states_.append(yellow_state)
                durations_.append(y_duration)
            return states_, durations_

        state = self.get_current_state()
        states, durations = make_states(state, self.duration, self.duration_switch)

        phases = []
        for i in range(len(states)):
            phases.append(Phase(durations[i], states[i]))

        program = Logic(id_program, 0, 0, phases)
        traci.trafficlight.setProgramLogic(self.id_traffic_light, program)

    def add_cmd(self, action):
        self.queue_cmd.append(action)

    def check_cmds_to_execute(self):
        if len(self.queue_cmd) < 1:
            pass
        else:self.execute_cmd()

    def execute_cmd(self):
        action = self.queue_cmd[0]
        self.apply_action(action)
        remove_action = True
        if remove_action:self.queue_cmd.pop(0)

    def apply_action(self, action):
        if action == Actions.N_S_open or action == Actions.E_W_open:
            self.switch_to_program(self.default_program)
            if action == Actions.N_S_open:self.set_phase(0)
            else:self.set_phase(2)
        else:
            self.switch_to_program(self.id_protected_program)
            if action == Actions.N_open:self.set_phase(0)
            elif action == Actions.E_open:self.set_phase(2)
            elif action == Actions.S_open:self.set_phase(4)
            else:self.set_phase(6)