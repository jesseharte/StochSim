'''
Created on 11 Mar 2020

@author: Jesse Harte, 20174537
'''
from views.View import View
from factories.IndividualFactory import IndividualFactory
from model.SimResults import SimResults
from model.Virus import Virus
from model.Location import Location
from datetime import datetime
import math
import random
import time

class MainController: 
    def __init__(self):
        self.mainView = View(self)
        self.individuals = []
        
        self.simResults = None

        self.mainView.start()
        
         
    def initializeVirus(self):
        self.factory = IndividualFactory(self.settings.p)
        self.individuals = []
        self.individuals += self.factory.generateSusceptibleIndividuals(self.settings.numPeople - 1, self.settings.p)
        infIndList = self.factory.generateInfectedIndividuals(1, self.settings.p)
        self.individuals += infIndList
        infInd = infIndList[0]
        
        # Force infected individual location
        # infInd.location = Location(0, -1, 0)
        # infInd.location = Location(0, -1/3, (2/3) * math.sqrt(2))
        # infInd.location = Location(0, 1/3, (2/3) * math.sqrt(2))
        # infInd.location = Location(0, 1, 0)
        
        
        
        self.virus = Virus(self.individuals, self.settings.infectionProb)
        self.simResults.registerNewVirus(self.virus)
            
    
    def simulateOnce(self, showCanvas=True):
        self.virus.spread()
        
        numFlyingIndividuals = self.settings.numFlyingIndividuals
        flyingIndividuals = random.sample(self.individuals, numFlyingIndividuals)
        for flyInd in flyingIndividuals:
            (x, y, z) = self.factory.generateLocation()
            flyInd.location = Location(x, y, z)
        
        
        if showCanvas: 
            self.mainView.updateCanvas(self.individuals)
        
        self.simResults.registerTimeEpoch()
        
    def simulateIndefinitely(self, showCanvas=True):
        
        while not(self.virus.terminated):
            self.simulateOnce(showCanvas)
        
    def simulateNRuns(self, settings, showCanvas=True):
        self.settings = settings
        self.newResults()
        n = settings.nrRunsToPerform
        
        for i in range(0, n):
            self.initializeVirus()
            self.simResults.registerTimeEpoch()
            self.simulateIndefinitely(showCanvas)
            self.simResults.storeVirusTimeEpochs()
            self.mainView.updateLongStats(self.simResults)
    
    def newResults(self):
        self.simResults = SimResults(self.settings)
      
    
    def notify(self):
        self.mainView.updateCanvas(self.individuals)
    
    def storeSimResults(self, dir):
        filename = dir + "/simResults_" + datetime.now().strftime('%Y%m%d%H%M%S') + ".txt"
        try:
            f = open(filename, "w")
            f.write(str(self.simResults))
            f.close()
            print("Results saved.")
        except:
            print("Results not saved.")
         
         
         
