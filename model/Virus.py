from model.SIRStatus import SIRStatus
from scipy import stats
from factories.Distribution import Distribution

class Virus: 
    def __init__(self, individuals, infectionProb):
        self.all = {}
        self.sus = {}
        self.newinf = {}
        self.inf = {}
        self.rec = {}
        self.infectionProb = infectionProb
        self.time = 0
        
        self.uniDist = Distribution(stats.uniform(0, 1))
        
        self.terminated = False
        
        for individual in individuals:
            self.all[individual.indId] = individual
            if individual.status == SIRStatus.SUSCEPTIBLE:
                self.sus[individual.indId] = individual
            elif individual.status == SIRStatus.INFECTED:
                self.inf[individual.indId] = individual
            elif individual.status == SIRStatus.RECOVERED:
                self.rec[individual.indId] = individual
        
    def spread(self):
        for susInd in self.sus.values():
            for infInd in self.inf.values():
                if self.uniDist.rvs() <= self.infectionProb(dist=susInd.getDistance(infInd), onNH=susInd.location.onNorthernHem):
                    self.infectInd(susInd)
                    break; 
        for infInd in self.inf.values():
            self.recoverInd(infInd)
        
        self.time += 1
        
        self.updateInfected()
        self.checkTermination()
    
    def recoverInd(self, ind):
        ind.recover()
        self.rec[ind.indId] = ind
    
    def infectInd(self, ind):
        ind.infect()
        self.newinf[ind.indId] = ind
    
    def updateInfected(self):
        self.inf = dict(self.newinf)
        for indId in self.newinf.keys():
            del self.sus[indId]
        self.newinf = {}
        
    def checkTermination(self):
        self.terminated = len(self.inf) == 0
            
    def getStats(self):
        return (len(self.sus), len(self.inf), len(self.rec))