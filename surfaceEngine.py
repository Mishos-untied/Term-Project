from cmu_graphics import *
import math


class Vector:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.mag = (x**2 + y**2)**0.5
        
        def __repr__(self):
            return f'<{self.x},{self.y}>'
        
        def __add__(self, other):
            if type(other) != Vector:
                return self
            else:
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
        
        def roundVector(self, decimalPlaces):
            x = pythonRound(self.x,decimalPlaces)
            y = pythonRound(self.y,decimalPlaces)
            return Vector(x, y)


class Projectile:
    def __init__(self, position, mass, angle, Cd, crossSectionalArea, velocity, thrust, burnTime):
        self.position = position
        self.mass = mass 
        self.velocity = velocity
        self.momentum = velocity * mass
        self.netForceFelt = Vector(0,0)
        self.burnTime = burnTime
        self.altitude = 0

        self.thrust = thrust
        self.angle = angle
        self.crossSectionalArea = crossSectionalArea
        self.Cd = Cd
        self.directionVector = Vector(-math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)))

        
    
    def updateDirection(self):
        self.directionVector = Vector(-math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)))
    





def onAppStart(app):
    app.dt = 0.07
    app.g = Vector(0,-9.8)
    app.p1 = Projectile(position = Vector(20,app.height), mass = 7.257, angle = 90, Cd = 0.342, crossSectionalArea=(math.pi*(0.37/2)**2), velocity = Vector(0,0), thrust = 200, burnTime = 10000)

def restartSim(app):
    pass

def redrawAll(app):
    rocketPosition = scalePosition(app.p1.position)
    drawRect(0,app.height-20,app.width,app.height,fill='green')
    drawRect(rocketPosition.x, rocketPosition.y, 5, 15, fill = 'black', rotateAngle = 90 - app.p1.angle)
    drawLabel(f'Altitude: {rounded(app.p1.altitude)} meters',80,40)

def scalePosition(unscaledPosition):
    scale = 1
    newX = unscaledPosition.x / scale
    newY = unscaledPosition.y / scale
    scaledPosition = Vector(newX,newY)
    return scaledPosition

def onKeyHold(app, keys):
    if 'left' in keys:
        app.p1.angle += 5
    if 'right' in keys:
        app.p1.angle -= 5
    app.p1.updateDirection()

    if 'down' in keys:
        app.p1.thrust -= 10
    if 'up' in keys:
        app.p1.thrust += 10

def takeStep(app):

    Fg = app.g * app.p1.mass
    
    if (app.p1.thrust > 0) and (app.p1.velocity.y > 0): #for now, only worry about drag if rocket is ascending or in powered descent
        H = 8000 # "scale height"
        p0 = 1.225 # air density at sea level 
        p = p0 * math.e ** (-app.p1.altitude / H) #air density at current altitude
        Fd =  (app.p1.directionVector * (-1) * ((1/2) * p * (app.p1.velocity.mag**2) * app.p1.crossSectionalArea * app.p1.Cd)).roundVector(1)
    else: # figure out falling back down drag force later
       Fd = Vector(0,0)

    print(f'Fd: {Fd}')
    print(f'Fg: {Fg}')
    if app.p1.burnTime > 0:
        Ft = app.p1.directionVector * app.p1.thrust
        app.p1.burnTime -= 1
    elif app.p1.burnTime == 0:
        app.p1.thrust = 0
        Ft = Vector(0,0)

    app.p1.netForceFelt = Fg + Fd + Ft 
    #update momentum using net force
    app.p1.momentum = app.p1.momentum + (app.p1.netForceFelt * app.dt)
    app.p1.velocity = app.p1.momentum / app.p1.mass
    deltaPosition = (app.p1.momentum/app.p1.mass)*app.dt
    app.p1.position = app.p1.position - deltaPosition
    app.p1.altitude += deltaPosition.y
    
  




def onStep(app):
    takeStep(app)

def runSurfaceEngine():
    runApp(width=700, height=700)

runSurfaceEngine()