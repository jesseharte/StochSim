'''
Created on 11 Mar 2020

@author: Jasper

Code for visualizing the txt files produced by the MainController
'''


import json
import numpy as np


import matplotlib.pyplot as plt


fileResults1 = open("simResults_20200320152003", "r")
info1 = fileResults1.readlines()
settings1 = json.loads(info1[0])
dataArray1 = json.loads(info1[1])

fileResults2 = open("simResults_20200320160205", "r")
info2 = fileResults2.readlines()
settings2 = json.loads(info2[0])
dataArray2 = json.loads(info2[1])

fileResults3 = open("simResults_20200320173559", "r")
info3 = fileResults3.readlines()
settings3 = json.loads(info3[0])
dataArray3 = json.loads(info3[1])


fileResults4 = open("simResults_2metNH", "r")
info4 = fileResults4.readlines()
settings4 = json.loads(info4[0])
dataArray4 = json.loads(info4[1])

fileResults5 = open("simResults_3metNH", "r")
info5 = fileResults5.readlines()
settings5 = json.loads(info5[0])
dataArray5 = json.loads(info5[1])


fileResults6 = open("simResults_20200323140842.txt", "r")
info6 = fileResults6.readlines()
settings6 = json.loads(info6[0])
dataArray6 = json.loads(info6[1])

fileResults7 = open("simResults_2 met dist kwadraat 10 flying people.txt", "r")
info7 = fileResults7.readlines()
settings7 = json.loads(info7[0])
dataArray7 = json.loads(info7[1])

fileResults8 = open("simResults_2 met dist kwadraat 100 flying people.txt", "r")
info8 = fileResults8.readlines()
settings8 = json.loads(info8[0])
dataArray8 = json.loads(info8[1])

fileResults9 = open("simResults_2 met dist kwadraat 200 flying people.txt", "r")
info9 = fileResults9.readlines()
settings9 = json.loads(info9[0])
dataArray9 = json.loads(info9[1])

fileResults10 = open("simResults_2 met dist kwadraat 500 flying people.txt", "r")
info10 = fileResults10.readlines()
settings10 = json.loads(info10[0])
dataArray10 = json.loads(info10[1])



fileResults11 = open("simResults_2 y = 1.txt", "r")
info11 = fileResults11.readlines()
settings11 = json.loads(info11[0])
dataArray11 = json.loads(info11[1])

fileResults12 = open("simResults_2 y = derde.txt", "r")
info12 = fileResults12.readlines()
settings12 = json.loads(info12[0])
dataArray12 = json.loads(info12[1])

fileResults13 = open("simResults_2 y = -derde.txt", "r")
info13 = fileResults13.readlines()
settings13 = json.loads(info13[0])
dataArray13 = json.loads(info13[1])

fileResults14 = open("simResults_2 y = -1.txt", "r")
info14 = fileResults14.readlines()
settings14 = json.loads(info14[0])
dataArray14 = json.loads(info14[1])

fileResultsA = open("simResults_2 S = 0.002.txt", "r")
infoA = fileResultsA.readlines()
settingsA = json.loads(infoA[0])
dataArrayA = json.loads(infoA[1])

fileResultsB = open("simResults_2 S = 0.002 flying 100.txt", "r")
infoB = fileResultsB.readlines()
settingsB = json.loads(infoB[0])
dataArrayB = json.loads(infoB[1])

fileResultsC = open("simResults_2 S = 0.002 flying 200.txt", "r")
infoC = fileResultsC.readlines()
settingsC = json.loads(infoC[0])
dataArrayC = json.loads(infoC[1])

fileResultsD = open("simResults_2 S = 0.002 flying 500.txt", "r")
infoD = fileResultsD.readlines()
settingsD = json.loads(infoD[0])
dataArrayD = json.loads(infoD[1])

def cleanThisArray(dataInput):
    maxT = 0
    for i in range(len(dataInput)):
        individualDuration = len(dataInput[i])
        if individualDuration > maxT:
            maxT = individualDuration
    infectedData = np.zeros((len(dataInput),maxT))
    for i in range(len(dataInput)):
        for j in range(maxT):
            if j < len(dataInput[i]):
                infectedData[i][j] = dataInput[i][j][1]
            
    
    return infectedData



def cleanThisArrayRecovered(dataInput):
    maxT = 0
    for i in range(len(dataInput)):
        individualDuration = len(dataInput[i])
        if individualDuration > maxT:
            maxT = individualDuration
    recoveredData = np.zeros((len(dataInput),maxT))
    for i in range(len(dataInput)):
        for j in range(maxT):
            if j < len(dataInput[i]):
                recoveredData[i][j] = dataInput[i][j][2]
            else:
                recoveredData[i][j] = dataInput[i][len(dataInput[i])-1][2]
    return recoveredData


def cleanThisArrayHemispheres(dataInput):
    maxT = 0
    for i in range(len(dataInput)):
        individualDuration = len(dataInput[i])
        if individualDuration > maxT:
            maxT = individualDuration
    infectedDataNH = np.zeros((len(dataInput),maxT))
    infectedDataSH = np.zeros((len(dataInput),maxT))
    for i in range(len(dataInput)):
        for j in range(maxT):
            if j < len(dataInput[i]):
                infectedDataNH[i][j] = (dataInput[i][j][4]/dataInput[i][j][3])*100
                infectedDataSH[i][j] = ((dataInput[i][j][1]-dataInput[i][j][4])/(500-dataInput[i][j][3]))*100
    return (infectedDataNH, infectedDataSH)


def confidenceIntervals(dataInput):
    nrRuns = len(dataInput)
    zalpha = 1.96
    sumData = np.zeros(len(dataInput[0]))
    sumDataSquared = np.zeros(len(dataInput[0]))
    upperCI = np.zeros(len(dataInput[0]))
    lowerCI = np.zeros(len(dataInput[0]))
    varData = np.zeros(len(dataInput[0]))
    halfwidths = np.zeros(len(dataInput[0]))
    for i in range(nrRuns):
        sumData += dataInput[i]
        sumDataSquared += np.square(dataInput[i])
    varData = sumDataSquared/nrRuns - np.square(sumData/nrRuns)
    halfwidths = np.sqrt(varData/nrRuns) * zalpha
    upperCI = sumData/nrRuns + halfwidths
    lowerCI = sumData/nrRuns - halfwidths
    return(lowerCI, sumData/nrRuns, upperCI)


def averageLengthVirus(dataInput):
    sumLengths = 0
    for i in range(len(dataInput)):
        sumLengths += len(dataInput[i])
    return (sumLengths/(len(dataInput)))-2

        
        
def histDuration(dataInput):
    simTimesArray = np.zeros(len(dataInput))
    for i in range(len(dataInput)):
        simTimesArray[i] = len(dataInput[i])
    d = np.diff(np.unique(simTimesArray)).min()
    left_of_first_bin = simTimesArray.min() - float(d)/2
    right_of_last_bin = simTimesArray.max() + float(d)/2
    plt.hist(simTimesArray, np.arange(left_of_first_bin, right_of_last_bin + d, d), density=True)
    plt.ylabel('Probability')
    plt.title('Histogram of virus termination times, n=500, p=0.8, S=0.006 ')
    plt.xlabel('Virus termination time (T)')
    plt.show()



# print(averageLengthVirus(dataArrayA))
# print(averageLengthVirus(dataArrayB))
# print(averageLengthVirus(dataArrayC))
# print(averageLengthVirus(dataArrayD))


# print(confidenceIntervals(cleanThisArrayRecovered(dataArray1))[1])
# print(confidenceIntervals(cleanThisArrayRecovered(dataArray2))[1])
# print(confidenceIntervals(cleanThisArrayRecovered(dataArray3))[1])



print(confidenceIntervals(cleanThisArrayRecovered(dataArrayA))[1])
print(confidenceIntervals(cleanThisArrayRecovered(dataArrayB))[1])
print(confidenceIntervals(cleanThisArrayRecovered(dataArrayC))[1])
print(confidenceIntervals(cleanThisArrayRecovered(dataArrayD))[1])



# fig, ax = plt.subplots() 
# cleanedData6 = confidenceIntervals(cleanThisArray(dataArray11))
# cleanedData8 = confidenceIntervals(cleanThisArray(dataArray12))
# cleanedData9 = confidenceIntervals(cleanThisArray(dataArray13))
# cleanedData10 = confidenceIntervals(cleanThisArray(dataArray14))
# ax.plot(range(len(cleanedData6[1])), cleanedData6[1] )
# ax.plot(range(len(cleanedData8[1])), cleanedData8[1] )
# ax.plot(range(len(cleanedData9[1])), cleanedData9[1] )
# ax.plot(range(len(cleanedData10[1])), cleanedData10[1] )
# ax.set_ylabel('Infected people (k)')
# ax.set_title('Number of infected people for location of patient zero, n=500')
# ax.set_xlabel('Time (t)')
# plt.legend(['y=1, p=0.5, S=0.006', 'y=1/3, p=0.5, S=0.006', 'y=-1/3, p=0.5, S=0.006', 'y=-1, p=0.5, S=0.006'], loc='upper right')
# fig.tight_layout()
# plt.show()





# plots for all parameters
# fig, ax = plt.subplots() 
# cleanedData6 = confidenceIntervals(cleanThisArray(dataArray6))
# cleanedData8 = confidenceIntervals(cleanThisArray(dataArray8))
# cleanedData9 = confidenceIntervals(cleanThisArray(dataArray9))
# cleanedData10 = confidenceIntervals(cleanThisArray(dataArray10))
# ax.plot(range(len(cleanedData6[1])), cleanedData6[1] )
# ax.plot(range(len(cleanedData8[1])), cleanedData8[1] )
# ax.plot(range(len(cleanedData9[1])), cleanedData9[1] )
# ax.plot(range(len(cleanedData10[1])), cleanedData10[1] )
# ax.set_ylabel('Infected people (k)')
# ax.set_title('Number of infected people over time with travel, n=500, d^2')
# ax.set_xlabel('Time (t)')
# plt.legend(['0 traveling people, p=0.5, S=0.006', '100 traveling people, p=0.5, S=0.006', '200 traveling people, p=0.5, S=0.006', '500 traveling people, p=0.5, S=0.006'], loc='upper right')
# fig.tight_layout()
# plt.show()




# plots for all parameters
fig, ax = plt.subplots() 
cleanedData6 = confidenceIntervals(cleanThisArray(dataArrayA))
cleanedData8 = confidenceIntervals(cleanThisArray(dataArrayB))
cleanedData9 = confidenceIntervals(cleanThisArray(dataArrayC))
cleanedData10 = confidenceIntervals(cleanThisArray(dataArrayD))
ax.plot(range(len(cleanedData6[1])), cleanedData6[1] )
ax.plot(range(len(cleanedData8[1])), cleanedData8[1] )
ax.plot(range(len(cleanedData9[1])), cleanedData9[1] )
ax.plot(range(len(cleanedData10[1])), cleanedData10[1] )
ax.set_ylabel('Infected people (k)')
ax.set_title('Number of infected people over time with travel, n=500, d^2')
ax.set_xlabel('Time (t)')
plt.legend(['0 traveling people, p=0.5, S=0.002', '100 traveling people, p=0.5, S=0.002', '200 traveling people, p=0.5, S=0.002', '500 traveling people, p=0.5, S=0.002'], loc='upper right')
fig.tight_layout()
plt.show()


# histDuration(dataArray3)












# 
# #plots for all parameters
# fig, ax = plt.subplots() 
# cleanedData1 = confidenceIntervals(cleanThisArrayHemispheres(dataArray5)[0])
# cleanedData2 = confidenceIntervals(cleanThisArrayHemispheres(dataArray5)[1])
# ax.plot(range(len(cleanedData1[1])), cleanedData1[1] )
# ax.plot(range(len(cleanedData2[1])), cleanedData2[1] )
# ax.set_ylabel('% of infected people')
# ax.set_title('Percentage of infected people per hemisphere, n=500, p=0.8, S=0.006')
# ax.set_xlabel('Time (t)')
# plt.legend(['Northern Hemisphere', 'Southern Hemisphere'], loc='upper right')
# fig.tight_layout()
# plt.show()








# plots for all parameters
# fig, ax = plt.subplots() 
# cleanedData1 = confidenceIntervals(cleanThisArray(dataArray1))
# tempD1 = np.append(cleanedData1[1], np.zeros(10))
# cleanedData2 = confidenceIntervals(cleanThisArray(dataArray2))
# cleanedData3 = confidenceIntervals(cleanThisArray(dataArray3))
# ax.plot(range(len(tempD1)), tempD1 )
# ax.plot(range(len(cleanedData2[1])), cleanedData2[1] )
# ax.plot(range(len(cleanedData3[1])), cleanedData3[1] )
# ax.set_ylabel('Infected people (k)')
# ax.set_title('Number of infected people over time, n=500')
# ax.set_xlabel('Time (t)')
# plt.legend(['p=0.2, S=0.007', 'p=0.5, S=0.006', 'p=0.8, S=0.006'], loc='upper right')
# fig.tight_layout()
# plt.show()




# fig, ax = plt.subplots() #Confidence Intervals 
# CiList = confidenceIntervals(cleanThisArray(dataArray2))
# ax.plot(range(len(CiList[0])), CiList[0] )
# ax.plot(range(len(CiList[0])), CiList[1] )
# ax.plot(range(len(CiList[0])), CiList[2] )
# ax.set_ylabel('nr of Infections (k)')
# ax.set_title('Number of infections over time, n=500, p=0.5, S=0.006')
# ax.set_xlabel('Time (t)')
# plt.legend(['Lower 95%CI', 'Average', 'Upper 95%CI'], loc='upper right')
# fig.tight_layout()
# plt.show()

