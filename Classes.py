import math

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
    maxThrust = 200
    def __init__(self, position, radius, mass, velocity, color, angle=0, name=None):
        self.rocketAngle = angle
        super().__init__(position, radius, mass, velocity, color, name)
        self.angle = 0
        self.directionVector = Vector(math.cos(self.angle), math.sin(self.angle))
        self.thrustMagnitude = 0
        if 0 <= self.thrustMagnitude <= Rocket.maxThrust:
            self.thrustMagnitude = self.thrustMagnitude
        elif self.thrustMagnitude > Rocket.maxThrust:
            self.thrustMagnitude = Rocket.maxThrust
        elif self.thrustMagnitude < 0:
            self.thrustMagnitude = 0
        self.thrustVector = self.directionVector * self.thrustMagnitude
    
    def updateThrust(self):
        if 0 <= self.thrustMagnitude <= Rocket.maxThrust:
            self.thrustMagnitude = self.thrustMagnitude
        elif self.thrustMagnitude > Rocket.maxThrust:
            self.thrustMagnitude = Rocket.maxThrust
        elif self.thrustMagnitude < 0:
            self.thrustMagnitude = 0
        self.thrustVector = self.directionVector * self.thrustMagnitude
    
    def updateDirection(self):
        self.directionVector = Vector(math.cos(self.angle), math.sin(self.angle)) 
    
        

    
