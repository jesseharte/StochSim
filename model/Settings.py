class Settings: 
    
    def __init__(self, settingsText): 
        
        try: 
            self.settingsText = settingsText
            self.set(settingsText)   
            print("Settings set successfully")     
        except: 
            defaultSettingsText = {'numPeopleText':'100', 'numFlyingIndividuals':'0', 'pText':'0.5', 'infectionProbText':'0.05 / (2 * dist)', 'nrRunsToPerform':'1'}
            self.settingsText = defaultSettingsText
            self.set(defaultSettingsText)
            print("Settings failed: default settings used.")
     
       
    def set(self, settingsText):
        self.numPeople = int(settingsText['numPeopleText'])
        self.numFlyingIndividuals = int(settingsText['numFlyingIndividuals'])
        self.p = float(settingsText['pText'])
        self.nrRunsToPerform = int(settingsText['nrRunsToPerform'])
        functionString = "lambda dist,onNH: " + settingsText['infectionProbText']
        self.infectionProb = eval(functionString)