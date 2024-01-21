from enum import Enum

class Actions(Enum):
    Switch_phase = 0
    # The Permitted Left Turn System:
    N_S_open = 1
    E_W_open = 2

    # The Protected Left Turn System:
    N_open = 3
    E_open = 4
    S_open = 5
    W_open = 6


