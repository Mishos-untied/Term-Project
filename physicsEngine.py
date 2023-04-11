from cmu_graphics import *
from Classes import Vector, Body, Rocket
import math

def onAppStart(app):
    restartSim(app)

def restartSim(app):
    app.paused = False
    app.drawTrails = False
    app.tracerStep = 5
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
    app.trailCutoffConstant = 5
    app.cameraMoveStep = 5
    app.sun1 = Body(position=Vector(app.width//2,app.height//2), radius=sunRadius, mass=sunMass, velocity=Vector(0,0), color='gold')
    #app.sun2 = Body(position=Vector(app.width//2+100, app.height//2), radius=sunRadius, mass=sunMass, velocity = Vector(0,20), color='gold')
    #app.planet1 = Body(position=Vector(app.width//2,60), radius=planet1Radius, mass=planet1Mass, velocity=Vector(15,0), color='red')
    #app.planet2 = Body(position=Vector(app.width//2,100), radius=planet2Radius, mass=planet2Mass, velocity=Vector(-18,0), color='green')
    #app.planet3 = Body(position=Vector(app.width//2,150), radius=planet3Radius, mass=planet3Mass, velocity=Vector(25,0), color='orange')
    app.rocket = Rocket(position=Vector(app.width//2, 300), radius=4, mass=10, velocity=Vector(0,0),color='grey')


def redrawAll(app):
    drawRect(0,0,app.width,app.height)
    
    for cBody in Body.instances:
        if isinstance(cBody, Rocket):
            x1 = cBody.position.x + 10
            y1 = cBody.position.y
            x2 = x3 = cBody.position.x - 5
            y2 = y1 - 5
            y3 = y1 + 5
            angle = cBody.angle * (180 / math.pi)
            drawPolygon(x1, y1, x2, y2, x3, y3, fill='white', rotateAngle=angle)
        else:
            drawCircle(cBody.position.x, cBody.position.y, cBody.radius, fill = cBody.color)

        if app.drawTrails == True:
            for i in range(1,len(cBody.previousPositions), app.tracerStep):
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
    if ('w' in keys) and ('s' not in keys):
        for cBody in Body.instances:
            cBody.position.y += app.cameraMoveStep
            for prevPosition in cBody.previousPositions:
                prevPosition.y += app.cameraMoveStep
    if ('s' in keys) and ('w' not in keys):
        for cBody in Body.instances:
            cBody.position.y -= app.cameraMoveStep
            for prevPosition in cBody.previousPositions:
                prevPosition.y -= app.cameraMoveStep
    if ('a' in keys) and ('d' not in keys):
        for cBody in Body.instances:
            cBody.position.x += app.cameraMoveStep
            for prevPosition in cBody.previousPositions:
                prevPosition.x += app.cameraMoveStep
    if ('d' in keys) and ('a' not in keys):
        for cBody in Body.instances:
            cBody.position.x -= app.cameraMoveStep
            for prevPosition in cBody.previousPositions:
                prevPosition.x -= app.cameraMoveStep
    if 'up' in keys and 'down' not in keys:
        app.rocket.thrustMagnitude += 3
        app.rocket.updateThrust()
    if 'down' in keys and 'up' not in keys:
        app.rocket.thrustMagnitude -= 3
        app.rocket.updateThrust()
    if 'left' in keys and 'right' not in keys:
        app.rocket.angle -= math.pi / 60
        app.rocket.updateDirection()
    if 'right' in keys and 'left' not in keys:
        app.rocket.angle += math.pi / 60
        app.rocket.updateDirection()
        
def takeStep(app):
    for i in range(len(Body.instances)):
        for j in range(i+1,len(Body.instances)):
            cBod1 = Body.instances[i]
            cBod2 = Body.instances[j]
            
            r = cBod2.position - cBod1.position
            
            if r.mag > (cBod1.radius + cBod2.radius):
                Fg = r*(-app.G*cBod1.mass*cBod2.mass) / (r.mag**3)
                if isinstance(cBod2, Rocket):
                    Ft = cBod2.thrustVector
                else:
                    Ft = Vector(0, 0)
                Fnet = Ft + Fg

                cBod1.momentum = cBod1.momentum - Fnet*app.dt
                cBod2.momentum = cBod2.momentum + Fnet*app.dt
                
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




    
    






