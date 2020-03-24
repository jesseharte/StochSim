import math
import numpy as np

class Location: 
    def __init__(self, x, y, z):
        if not(self.checkRep((x, y, z))):
            raise ValueError("Location is not on the unit sphere x={}, y={}, z={}".format(x, y, z))
        
        self.position = (x, y, z)
        self.x = x
        self.y = y
        self.z = z
        self.onNorthernHem = y > 0
    
    def __str__(self):
        return "Position: ({}) on {}".format(self.position, self.getHemisphere())
    
    def checkRep(self, posTuple):
        return np.dot(posTuple, posTuple) < 1.01 and np.dot(posTuple, posTuple) > 0.99
    
    def getHemisphere(self):
        if self.onNorthernHem: 
            return "Northern Hemisphere"
        else: 
            return "Southern Hemisphere" 
    
    def computeDistance(self, otherLoc):
        return math.acos(np.dot(self.position, otherLoc.position))
    
    def getSphericalCoordinates(self):
        # (Azimuth, inclination)
        return (math.atan(self.y/self.x), math.atan(math.sqrt(self.x*self.x + self.y*self.y) / self.z))
    
    def getLatLongCoordinates(self):
        # (lat in -pi/2, pi/2, long in -pi, pi)
        return (math.acos(self.y) - math.pi /2, math.atan2(self.z, self.x))