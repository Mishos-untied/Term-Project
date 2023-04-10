from cmu_graphics import *

class vector:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.mag = (x**2 + y**2)**0.5
        
        def __repr__(self):
            return f'<{self.x},{self.y}>'
        
        def __add__(self, other):
            newX = self.x + other.x
            newY = self.y + other.y
            return vector(newX, newY)
            
        def __sub__(self,other):
            newX = self.x - other.x
            newY = self.y - other.y
            return vector(newX, newY)
        
        def __mul__(self, other):
            if not ( isinstance(other, float) or isinstance(other, int) ):
                raise TypeError('Can only multiply a vector with a scalar')
            elif (isinstance(other, float) or isinstance(other,int)):
                newX = self.x * other
                newY = self.y * other
                return vector(newX, newY)
            
        def __truediv__(self,other):
            if not ( isinstance(other, float) or isinstance(other, int) ):
                raise TypeError('Can only divide a vector with a scalar')
            elif (isinstance(other, float) or isinstance(other,int)):
                return (self * (1 / other))
class body:
        instances = []
        def __init__(self, position, radius, mass, velocity, color):
            self.position = position
            self.previousPositions = []
            self.radius = radius
            self.mass = mass
            self.velocity = velocity
            self.color = color
            self.momentum = self.velocity * self.mass
            body.instances.append(self)


def onAppStart(app):
    restartSim(app)

def restartSim(app):
    app.paused = False
    app.drawTrails = False
    
    app.G = 1
    
    sunRadius = 10
    sunMass = 100000
    planet1Radius = 4
    planet1Mass = 200
    planet2Radius = 3
    planet2Mass = 10
    planet3Radius = 3
    planet3Mass = 15
    
    app.dt = 0.01
    
    app.trailCutoffConstant = 10
    app.cameraMoveStep = 5
    
    app.sun1 = body(position=vector(app.width//2,app.height//2), radius=sunRadius, mass=sunMass, velocity=vector(0,0), color='blue')
    app.planet1 = body(position=vector(app.width//2,60), radius=planet1Radius, mass=planet1Mass, velocity=vector(15,0), color='red')
    app.planet2 = body(position=vector(app.width//2,100), radius=planet2Radius, mass=planet2Mass, velocity=vector(-18,0), color='green')
    app.planet3 = body(position=vector(app.width//2,150), radius=planet3Radius, mass=planet3Mass, velocity=vector(25,0), color='orange')


   
def redrawAll(app):
    drawRect(0,0,app.width,app.height)
    
    for cBody in body.instances:
        drawCircle(cBody.position.x, cBody.position.y, cBody.radius, fill = cBody.color)
        if app.drawTrails == True:
            for i in range(1,len(cBody.previousPositions)):
                pos1 = cBody.previousPositions[i-1]
                pos2 = cBody.previousPositions[i]
                x1 = pos1.x
                y1 = pos1.y
                x2 = pos2.x
                y2 = pos2.y
                drawLine(x1, y1, x2, y2, fill = 'white')
    
    
def onKeyPress(app, key):
    if key == 'p':
        app.paused = not app.paused
    if key == 't':
        app.drawTrails = not app.drawTrails
    if (key == 's' and app.paused == True):
        takeStep(app)


def onKeyHold(app, keys):
    if ('up' in keys) and ('down' not in keys):
        for cBody in body.instances:
            cBody.position.y -= app.cameraMoveStep
            for prevPosition in cBody.previousPositions:
                prevPosition.y -= app.cameraMoveStep
    if ('down' in keys) and ('up' not in keys):
        for cBody in body.instances:
            cBody.position.y += app.cameraMoveStep
            for prevPosition in cBody.previousPositions:
                prevPosition.y += app.cameraMoveStep
    if ('right' in keys) and ('left' not in keys):
        for cBody in body.instances:
            cBody.position.x += app.cameraMoveStep
            for prevPosition in cBody.previousPositions:
                prevPosition.x += app.cameraMoveStep
    if ('left' in keys) and ('right' not in keys):
        for cBody in body.instances:
            cBody.position.x -= app.cameraMoveStep
            for prevPosition in cBody.previousPositions:
                prevPosition.x -= app.cameraMoveStep

def takeStep(app):
    
    for i in range(len(body.instances)):
        for j in range(i+1,len(body.instances)):
            cBod1 = body.instances[i]
            cBod2 = body.instances[j]
            
            r = cBod2.position - cBod1.position
            
            if r.mag > (cBod1.radius + cBod2.radius):
                Fg = r*(-app.G*cBod1.mass*cBod2.mass) / (r.mag**3)
                cBod1.momentum = cBod1.momentum - Fg*app.dt
                cBod2.momentum = cBod2.momentum + Fg*app.dt
                
                cBod1.previousPositions.append(cBod1.position) 
                cBod2.previousPositions.append(cBod2.position)
                if (len(cBod1.previousPositions) * app.dt) > app.trailCutoffConstant:
                    cBod1.previousPositions.pop(0)
                if (len(cBod2.previousPositions) * app.dt) > app.trailCutoffConstant:
                    cBod2.previousPositions.pop(0)
                
                cBod1.position = cBod1.position + (cBod1.momentum/cBod1.mass)*app.dt
                cBod2.position = cBod2.position + (cBod2.momentum/cBod2.mass)*app.dt

def onStep(app):
    if not app.paused:
        takeStep(app)

def main():
    runApp()

main()




    
    






# from objectClass import Object
# import time
# import math
# #let's make constants be global
# G = 6.67430 * (10 ** -11)
# littleG = 9.80665
# earthMass = 5.972 * 10**(24)
# earthRadius = 6378.1*10**3

# earth = Object("earth", earthMass, 0, 0, 0, 0)

# box = Object("box", 1, earthRadius, 0, 0, 0)

# def almostEqual(x, y):
#     return abs(x-y) < 0.1

# ############
# ###Forces###
# ############


# def gravitation(object1, object2):
#     return (G*object1.mass*object2.mass) / (object1.distance(object2)**2)


# items = [earth, box]
# forceFunctions = [gravitation]
# # apparently you can store functions in list, so these abuse this fact to sum the forces in the x and y
# # directions. Only caveat is the the function has to be defined in a line above the list

# def findXForces(o): 
#     total = 0
#     for fun in forceFunctions:
#         for obj in items:
#             if obj != o:
#                 total += math.cos(o.angleBetween(obj)) * fun(o, obj)
#     return total

# def findYForces(o):
#     total = 0
#     for fun in forceFunctions:
#         for obj in items:
#             if obj != 0:
#                 total += math.sin(o.angleBetween(obj)) * fun(o, obj)





# ############
# ###Motion###
# ############

# def updateXPos(ob):
#     acceleration = findXForces(ob) / ob.mass
#     ob.cx = ob.vx + 0.5 * acceleration

# def updateYPos(ob):
#     acceleration = findYForces(ob) / ob.mass
#     ob.cy = ob.vy + 0.5 * acceleration

# def updateObject(ob):
#     updateXPos(ob)
#     updateYPos(ob)


