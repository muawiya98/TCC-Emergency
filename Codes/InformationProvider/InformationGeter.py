from Codes.InformationProvider.WaitingTime import WaitingTime
from Codes.InformationProvider.Density import Density
from Codes.InformationProvider.QueueLength import QueueLength

class Infromation(WaitingTime,QueueLength,Density):
    def __init__(self, Agent_ids):
        WaitingTime.__init__(self, Agent_ids)
        QueueLength.__init__(self)
        Density.__init__(self)