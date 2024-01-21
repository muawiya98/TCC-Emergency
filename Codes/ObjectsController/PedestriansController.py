from traci import person
from uuid import uuid4


class PedestrianController :

    def add_persons(self,number_persons,edges):
        while number_persons>0:
            person_id = str(uuid4())
            edge1 = edges[0]
            edge2 = edges[1]
            person.add(person_id , edge1 ,0)
            person.appendWalkingStage(person_id, [edge1,edge2] , 1)
            number_persons-=1
        

    
    