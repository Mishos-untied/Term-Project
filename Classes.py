import math

scale = 1.3e-9
dt = 0.00001
dtsPerSecond = 0.0001


class Vector:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.mag = (x**2 + y**2)**0.5
        
        def __repr__(self):
            return f'<{self.x},{self.y}>'
        
        def __add__(self, other):
            newX = self.x + other.x
            newY = self.y + other.y
            return Vector(newX, newY)
            
        def __sub__(self,other):
            newX = self.x - other.x
            newY = self.y - other.y
            return Vector(newX, newY)
        
        def __mul__(self, other):
            if not ( isinstance(other, float) or isinstance(other, int) ):
                raise TypeError('Can only multiply a vector with a scalar')
            elif (isinstance(other, float) or isinstance(other,int)):
                newX = self.x * other
                newY = self.y * other
                return Vector(newX, newY)
            
        def __truediv__(self,other):
            if not ( isinstance(other, float) or isinstance(other, int) ):
                raise TypeError('Can only divide a vector with a scalar')
            elif (isinstance(other, float) or isinstance(other,int)):
                return (self * (1 / other))
class Body:
        instances = []
        def __init__(self, position, radius, mass, velocity, color, name=None):
            self.position = position
            self.previousPositions = []
            self.radius = radius
            self.mass = mass
            self.velocity = velocity
            self.color = color
            self.netForceFelt = Vector(0,0)
            self.momentum = self.velocity * self.mass
            Body.instances.append(self)
            if name != None:
                self.name = name
            else:
                self.name = Body.instances.index(self)

class Rocket(Body):
    def __init__(self, position, radius, mass, velocity, color, angle=0, maxThrust = 91.19e3, burnTime = 750, fuelMass = 18410,  name='Apollo CSM'):
        self.burnTime = burnTime
        self.outOfFuel = False
        self.maxThrust = maxThrust * scale
        self.fuelMass = fuelMass
        self.fuelPerSec = self.fuelMass / self.burnTime
        self.rocketAngle = angle
        super().__init__(position, radius, mass, velocity, color, name)
        self.angle = 0
        self.directionVector = Vector(math.cos(self.angle), math.sin(self.angle))
        self.thrustMagnitude = 0
        if 0 <= self.thrustMagnitude <= self.maxThrust:
            self.thrustMagnitude = self.thrustMagnitude
        elif self.thrustMagnitude > self.maxThrust:
            self.thrustMagnitude = self.maxThrust
        elif self.thrustMagnitude < 0:
            self.thrustMagnitude = 0
        self.thrustVector = self.directionVector * self.thrustMagnitude
    
    def updateThrust(self):
        if not self.outOfFuel:
            if 0 <= self.thrustMagnitude <= self.maxThrust:
                self.thrustMagnitude = self.thrustMagnitude
            elif self.thrustMagnitude > self.maxThrust:
                self.thrustMagnitude = self.maxThrust
            elif self.thrustMagnitude < 0:
                self.thrustMagnitude = 0
            self.thrustVector = self.directionVector * self.thrustMagnitude
        
    def updatePropellant(self):
        currentPercentDecimal = (self.thrustMagnitude / self.maxThrust)
        timeInterval = dt / dtsPerSecond
        fuelUsedInTimeInterval = currentPercentDecimal * self.fuelPerSec * timeInterval
        if self.fuelMass - fuelUsedInTimeInterval > 0:
            self.fuelMass -= fuelUsedInTimeInterval
            self.mass -= fuelUsedInTimeInterval
        elif self.fuelMass - fuelUsedInTimeInterval < 0:
            self.thrustMagnitude = 0
            self.thrustVector = Vector(0,0)
            self.outOfFuel = True
        print(self.fuelMass)
    


    def updateDirection(self):
        self.directionVector = Vector(math.cos(self.angle), math.sin(self.angle)) 

        

    
