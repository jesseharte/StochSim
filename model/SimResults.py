import math
import json

class SimResults: 
    def __init__(self, settings):
        self.curVirus = None
        self.curVirusResults = []
        self.results = [] 
        self.numRuns = 0
        
        self.settings = settings
    
    def __str__(self):
        settingsJSON = json.dumps(self.settings.settingsText)
        resultsJSON = json.dumps(self.results)
        returnVal = settingsJSON + "\n" + resultsJSON
        return returnVal
    
    def storeVirusTimeEpochs(self):
        self.results.append(self.curVirusResults)
        self.numRuns += 1
    
    def registerNewVirus(self, virus):
        self.curVirus = virus
        self.numPeopleOnNorthernHem = int(sum(person.location.onNorthernHem for person in self.curVirus.all.values()))
        self.curVirusResults = []
            
    
    def registerTimeEpoch(self):
        self.curVirusResults.append([len(self.curVirus.sus), len(self.curVirus.inf), len(self.curVirus.rec), self.numPeopleOnNorthernHem, int(sum(person.location.onNorthernHem for person in self.curVirus.inf.values()))])
        
    
    def getLastTimeEpoch(self):
        if len(self.curVirusResults) == 0:
            return (0,0,0)
        return self.curVirusResults[len(self.curVirusResults) - 1]
    
        
    def getAverageOnTimeEpoch(self, timeEpoch):
        resultsLength = len(self.results)
        
        if resultsLength == 0: 
            return (0,0,0)
        
        totalSum = 0
        totalSum2 = 0
        
        for tempResults in self.results:
            if len(tempResults) > timeEpoch:
                totalSum += tempResults[timeEpoch][1]
                totalSum2 += tempResults[timeEpoch][1] ** 2
         
        avg = totalSum / resultsLength
        avg2 = totalSum2 / resultsLength 
        var = avg2 - avg ** 2
        std = math.sqrt(var)
        halfW = self.getHalfWidth(std, resultsLength)
        
        return (avg, var, halfW) 
    
    def getAverageTimeSpan(self):
        resultsLength = len(self.results)
        if resultsLength == 0: 
            return (0,0,0)
        
        totalSum = 0 
        totalSum2 = 0
        
        for tempResults in self.results:
            totalSum += len(tempResults) - 2
            totalSum2 += (len(tempResults) - 2) ** 2
        
        avg = totalSum / resultsLength
        avg2 = totalSum2 / resultsLength 
        var = avg2 - avg ** 2
        std = math.sqrt(var)
        halfW = self.getHalfWidth(std, resultsLength)
        
        return (avg, var, halfW) 
    
    def getAverageAffected(self):
        resultsLength = len(self.results)
        if resultsLength == 0: 
            return (0,0,0)
        
        totalSum = 0 
        totalSum2 = 0
        
        for tempResults in self.results:
            totalSum += tempResults[-1][2]
            totalSum2 += tempResults[-1][2] ** 2
        
        avg = totalSum / resultsLength
        avg2 = totalSum2 / resultsLength 
        var = avg2 - avg ** 2
        std = math.sqrt(var)
        halfW = self.getHalfWidth(std, resultsLength)
        
        return (avg, var, halfW) 
        
    
    def getHalfWidth(self, std, n):
        Za = 1.96
        return Za * std / math.sqrt(n)