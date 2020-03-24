from model.SIRStatus import SIRStatus

class Individual: 
    def __init__(self, indId, location, status):
        self.indId = indId 
        self.location = location 
        self.status = status
    
    def __str__(self):
        return "Individual {} at {} is currently {}.".format(self.indId, self.location, self.status.name)
    
    def infect(self):
        self.status = SIRStatus.INFECTED 
    
    def recover(self):
        self.status = SIRStatus.RECOVERED 
        
    def getDistance(self, otherInd):
        return self.location.computeDistance(otherInd.location)
        