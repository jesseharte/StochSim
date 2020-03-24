from model.Individual import Individual
from model.Location import Location
from model.SIRStatus import SIRStatus

from scipy import stats

import math

from factories.Distribution import Distribution

class IndividualFactory: 
    
    def __init__(self, probNHvsSH):
        self.curIndex = 0
        self.uniDist = Distribution(stats.uniform(0, 1))
        self.probNHvsSH = probNHvsSH
    
    def generateSusceptibleIndividuals(self, numSus, p):
        cusList = []
        for _ in range(numSus):
            cusList.append(self.generateIndividual(SIRStatus.SUSCEPTIBLE))
        return cusList    
            
    def generateInfectedIndividuals(self, numInf, p):
        cusList = []
        for _ in range(numInf):
            cusList.append(self.generateIndividual(SIRStatus.INFECTED))
        return cusList
    
    def generateRecoveredIndividuals(self, numRec, p):
        cusList = []
        for _ in range(numInf):
            cusList.append(self.generateIndividual(SIRStatus.RECOVERED))
        return cusList   
    
    def generateIndividual(self, sirStatus):
        sphereLoc = self.generateLocation()
        location = Location(x=sphereLoc[0], y=sphereLoc[1], z=sphereLoc[2])
        individual = Individual(self.curIndex, location, sirStatus)
        self.curIndex += 1
        return individual
    
    def generateLocation(self):
        randArray = self.uniDist.rvs(2)
        randArray[0] = randArray[0] * 2 - 1
        
        locNorm = randArray[0] * randArray[0] + randArray[1] * randArray[1]
        
        if locNorm > 1: 
            return self.generateLocation()
        
        # With chance 1 - p, an individual is on the Southern Hemisphere
        if self.uniDist.rvs() > self.probNHvsSH:
            randArray[1] = -1 * randArray[1]
        
        x = 2*randArray[0] * math.sqrt(1 - randArray[0] * randArray[0] - randArray[1] * randArray[1])
        y = 2*randArray[1] * math.sqrt(1 - randArray[0] * randArray[0] - randArray[1] * randArray[1])
        z = 1 - 2*(randArray[0] * randArray[0] + randArray[1] * randArray[1])
        
        
        
        return (x,y,z)
        
        
        