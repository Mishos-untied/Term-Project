from cmu_graphics import *
from Classes import Vector, Body, Rocket
import math

def onAppStart(app):
    restartSim(app)

def restartSim(app):
    app.screen = [app.width//2, app.height//2, app.width, app.height]
    app.paused = False
    app.drawTrails = False
    app.tracerStep = 10
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
    app.planet1 = Body(position=Vector(app.width//2,160), radius=planet1Radius, mass=planet1Mass, velocity=Vector(15,0), color='red')
    app.planet2 = Body(position=Vector(app.width//2,250), radius=planet2Radius, mass=planet2Mass, velocity=Vector(-18,0), color='green')
    app.planet3 = Body(position=Vector(app.width//2,300), radius=planet3Radius, mass=planet3Mass, velocity=Vector(25,0), color='orange')
    #app.rocket = Rocket(position=Vector(app.width//2, 300), radius=4, mass=10, velocity=Vector(0,0),color='grey')

def rectanglesOverlap(left1, top1, width1, height1,
                      left2, top2, width2, height2): #slightly modified version of my own code
    right1 = left1 + width1  #got this from:https://cs3-112-f22.academy.cs.cmu.edu/exercise/4581
    right2 = left2 + width2
    bottom1 = top1 + height1
    bottom2 = top2 + height2
    if right1 >= left2 or right2 >= left1:
        if bottom2 >= bottom1 >= top2 or bottom1 >= bottom2 >= top1:
            return True
    return False

def redrawAll(app):
    drawRect(0,0,app.width,app.height)
    scale = app.width / app.screen[2]
    boxX = app.screen[0] - app.screen[2] // 2
    boxY = app.screen[1] - app.screen[3]//2
    drawRect(boxX, boxY, app.screen[2], app.screen[3], border='white')
    for cBody in Body.instances:
        cBodyLeft = cBody.position.x - cBody.radius
        cBodyTop = cBody.position.y - cBody.radius
        screenLeft, screenTop, screenWidth, screenHeight = app.screen
        if isinstance(cBody, Rocket):
            x1 = cBody.position.x + 10 
            y1 = cBody.position.y 
            x2 = x3 = cBody.position.x - 5 
            y2 = y1 - 5
            y3 = y1 + 5
            angle = cBody.angle * (180 / math.pi)
            drawPolygon(x1, y1, x2, y2, x3, y3, fill='white', rotateAngle=angle)
        else:
            xPos = cBody.position.x 
            yPos = cBody.position.y 
            drawCircle(xPos, yPos, cBody.radius, fill = cBody.color)

        if app.drawTrails == True:
            for i in range(1,len(cBody.previousPositions), app.tracerStep):
                pos1 = cBody.previousPositions[i-1]
                pos2 = cBody.previousPositions[i]
                x1 = pos1.x 
                y1 = pos1.y 
                x2 = pos2.x 
                y2 = pos2.y 
                drawLine(x1, y1, x2, y2, fill = 'white')
    drawRect(app.width-5, 25, 25, 50, border='white', fill=None)
    # thrustHeight = 50 * app.rocket.thrustMagnitude / Rocket.maxThrust
    # if thrustHeight > 0:
    #     drawRect(350, 25+(50-thrustHeight), 25, thrustHeight, fill='white')
    
def onKeyPress(app, key):
    if key == 'p':
        app.paused = not app.paused
    if key == 't':
        app.drawTrails = not app.drawTrails
    if (key == 's' and app.paused == True):
        takeStep(app)


def onKeyHold(app, keys):
    print(app.screen[2], app.screen[3])
    if 'w' in keys:
        app.screen[1] += 2
    if 's' in keys:
        app.screen[1] -= 2
    if 'a' in keys:
        app.screen[0] -= 2
    if 'd' in keys:
        app.screen[0] += 2
    if 'm' in keys and app.screen[2] > 100:
        app.screen[2] -= 5
        app.screen[3] -= 5
    if 'n' in keys and app.screen[2] < app.width:
        app.screen[2] += 5
        app.screen[3] += 5
    if 'up' in keys and 'down' not in keys:
        app.rocket.thrustMagnitude += 3
    if 'down' in keys and 'up' not in keys:
        app.rocket.thrustMagnitude -= 3
    if 'left' in keys and 'right' not in keys:
        app.rocket.angle -= math.pi / 60
        app.rocket.updateDirection()
    if 'right' in keys and 'left' not in keys:
        app.rocket.angle += math.pi / 60
        app.rocket.updateDirection()
    # app.rocket.updateThrust()
        
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
    runApp(width=700, height=700)

main()




    
    






