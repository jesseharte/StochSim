'''
Created on 11 Mar 2020

@author: Jesse Harte, 20174537
'''
from tkinter import *
from model.SIRStatus import SIRStatus
import math

from model.Settings import Settings
import tkinter.simpledialog as simpledialog
import tkinter.filedialog as filedialog 

class View:
    
    def __init__(self, controller):
        self.controller = controller
        
        self.projectionsStringToFunc = {"Hammer projection":self.hammerProjection, "Equirectangular projection":self.equirectangularProjection}
        self.onceStatsLabels = {"Susceptible":None, "Infected":None, "Recovered":None}
        self.nRunsStatsLabels = {"Run":None, "E[I1]":None, "E[I5]":None, "E[I10]":None,"Var[I10]":None, "E[T]":None,"Var[T]":None, "E[#Affected]":None}
        
        self.buttons = []
        
        self.sphereCanvasWidth = 800
        self.sphereCanvasHeight = 800
        
        self.mainView = Tk()
        self.mainView.title("Virus spread")
        
        self.mainView.resizable(0, 0)
        
        # Create Canvas
        self.sphereCanvas = Canvas(self.mainView, width=self.sphereCanvasWidth, height=self.sphereCanvasHeight)
        self.sphereCanvas.grid(row=0, column=1, rowspan=2)
    
        
        # Create permanent frame        
        infoFrame = Frame(self.mainView)
        infoFrame.grid(row=0, column=0)
        
        curRow = 0
        
        Label(infoFrame, text="Number of people").grid(row=curRow, column=0)
        self.numPeopleEntry = Entry(infoFrame)
        self.numPeopleEntry.grid(row=curRow, column=1)
        curRow += 1
        
        Label(infoFrame, text="Number of flying people").grid(row=curRow, column=0)
        self.numFlyingEntry = Entry(infoFrame)
        self.numFlyingEntry.grid(row=curRow, column=1)
        curRow += 1
        
        Label(infoFrame, text="NH vs. SH probability").grid(row=curRow, column=0)
        self.pEntry = Entry(infoFrame)
        self.pEntry.grid(row=curRow, column=1)
        curRow += 1
        
        Label(infoFrame, text="Infection probability function (use parameters: dist, onNH)").grid(row=curRow, column=0)
        self.infectionProbEntry = Entry(infoFrame)
        self.infectionProbEntry.insert(END, '(2 - onNH) * (0.002 / (2 * dist * dist))')
        self.infectionProbEntry.grid(row=curRow, column=1)
        curRow += 1
        
        self.projectionChosen = StringVar(self.mainView)
        self.projectionChosen.set(list(self.projectionsStringToFunc.keys())[0])
        self.projectionChosen.trace("w", self.projectionChanged)
        projectionMenu = OptionMenu(infoFrame, self.projectionChosen, *self.projectionsStringToFunc.keys())
        projectionMenu.grid(row=curRow, column=0, columnspan=2)
        curRow += 1
        
        simulateNRunsButton = Button(infoFrame, text="Spread virus n times", width=20, command=self.simulateNRuns)
        simulateNRunsButton.grid(row=curRow, column=0, columnspan=2)
        self.buttons.append(simulateNRunsButton)
        curRow += 1
        
        storeButton = Button(infoFrame, text="Store results", width=20, command=self.storeResults)
        storeButton.grid(row=curRow, column=0, columnspan=2)
        self.buttons.append(storeButton)
        storeButton.config(state = DISABLED)
        curRow += 1
        
        # Create stats frame for simulate once and indefinitely          
        self.statsFrame = Frame(self.mainView)
        self.statsFrame.grid(row=1,column=0)
        
        # Create stats frame for simulate n runs 
        self.nRunsFrame = Frame(self.statsFrame)
        self.nRunsFrame.grid(row=0, column=0)
        
        curRow = 0
        
        for labelText in self.nRunsStatsLabels.keys():
             curStringVar = StringVar()
             Label(self.nRunsFrame, text=labelText).grid(row=curRow, column = 0)
             Label(self.nRunsFrame, textvariable=curStringVar).grid(row=curRow, column = 1)
             self.nRunsStatsLabels[labelText] = curStringVar
             curRow += 1
        
    def disableButtons(self):
        for button in self.buttons:
            button.config(state = DISABLED)
        self.mainView.update_idletasks()
    
    def enableButtons(self):
        for button in self.buttons:
            button.config(state = NORMAL)
        
        self.mainView.update_idletasks()
        
    def simulateNRuns(self):
        self.disableButtons()
        self.sphereCanvas.delete("all")
        runsToPerform = simpledialog.askinteger("Number of runs", "Please enter the number of runs you would like to perform")
        settingsText = {'numPeopleText': self.numPeopleEntry.get(), 'numFlyingIndividuals':self.numFlyingEntry.get(), 'pText': self.pEntry.get(),'infectionProbText':self.infectionProbEntry.get(), 'nrRunsToPerform':runsToPerform}
        settings = Settings(settingsText)
        self.controller.simulateNRuns(settings)
        self.enableButtons()
        
    
    def projectionChanged(self, *args):
        self.controller.notify()
       
    def start(self):
        self.mainView.mainloop()
        
    def quit(self):
        self.mainView.quit()
    
    def storeResults(self):
        path = filedialog.askdirectory()
        if path != "":
            self.controller.storeSimResults(path)
    
    def equirectangularProjection(self, coord):
        x = coord[1] / (2 * math.pi) + 0.5
        y = coord[0] / math.pi + 0.5
        return (x, y)
    
    def hammerProjection(self, coord):
        lam = coord[1]
        phi = coord[0]
        
        x = math.cos(phi) * math.sin(lam/2)
        y = math.sin(phi)
        x = (x + 1) / 2
        y = (y + 1) / 2 
        return (x, y)
        
    
    def getProjectionCoord(self, projectionFunction, coord, circleSize):
        (x, y) = projectionFunction(coord)
        
        x = ((x - 0.5) * 0.95 + 0.5) * self.sphereCanvasWidth
        y = ((y - 0.5) * 0.95 + 0.5) * self.sphereCanvasHeight
        
        
        x0 = x - circleSize 
        x1 = x + circleSize
        y0 = y - circleSize
        y1 = y + circleSize
        
        return (x0, y0, x1, y1)
    
    def drawInd(self, projectionFunction, coord, sirStat, circleSize):
        (x0, y0, x1, y1) = self.getProjectionCoord(projectionFunction, coord, circleSize)
        
        if sirStat == SIRStatus.SUSCEPTIBLE:
            self.sphereCanvas.create_oval(x0, y0, x1, y1, fill="#008000")
        elif sirStat == SIRStatus.INFECTED:
            self.sphereCanvas.create_oval(x0, y0, x1, y1, fill="#FF0000")
        elif sirStat == SIRStatus.RECOVERED:
            self.sphereCanvas.create_oval(x0, y0, x1, y1, fill="#0000FF")
        
            
    
    def updateCanvas(self, individuals, circleSize=4):
        self.sphereCanvas.delete("all")
        projectionFunction = self.projectionsStringToFunc[self.projectionChosen.get()]
        for ind in individuals:
             self.drawInd(projectionFunction, ind.location.getLatLongCoordinates(), ind.status, circleSize)
        
        self.mainView.update_idletasks()
    
    def updateLongStats(self, simResults):
        e1 = simResults.getAverageOnTimeEpoch(1)
        e5 = simResults.getAverageOnTimeEpoch(5)
        e10 = simResults.getAverageOnTimeEpoch(10)
        eT = simResults.getAverageTimeSpan()
        eAff = simResults.getAverageAffected()
        
        tE1 = "(a: {:.3f}, hw: {:.3f})".format(e1[0], e1[2])
        tE5 = "(a: {:.3f}, hw: {:.3f})".format(e5[0], e5[2])
        tE10 = "(a: {:.3f}, hw: {:.3f})".format(e10[0], e10[2])
        tVar10 = "{:.3f}".format(e10[1])
        tET = "(a: {:.3f}, hw: {:.3f})".format(eT[0], eT[2])
        tVarT = "{:.3f}".format(eT[1])
        tEAff = "(a: {:.3f}, hw: {:.3f})".format(eAff[0], eAff[2])
        
        
        self.nRunsStatsLabels['Run'].set(simResults.numRuns)
        self.nRunsStatsLabels['E[I1]'].set(tE1)
        self.nRunsStatsLabels['E[I5]'].set(tE5)
        self.nRunsStatsLabels['E[I10]'].set(tE10)
        self.nRunsStatsLabels['Var[I10]'].set(tVar10)
        self.nRunsStatsLabels['E[T]'].set(tET)
        self.nRunsStatsLabels['Var[T]'].set(tVarT)
        self.nRunsStatsLabels['E[#Affected]'].set(tEAff)
        
        self.mainView.update()
            