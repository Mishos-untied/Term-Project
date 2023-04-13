#Current lines: 309, target: 1500, progress; 20.60%
from cmu_graphics import *
from Classes import Vector, Body, Rocket
import math

def onAppStart(app):
    app.showLoadingScreen = True
    restartSim(app)
    loadingScreenSim(app)

def loadingScreenSim(app):
    app.drawTrails = True
    sunMass = 100000
    sunRadius = 10
    app.sun1 = Body(Vector(300, 300), sunRadius, sunMass, Vector(10, -20), 'red')
    app.sun2 = Body(Vector(500, 300), sunRadius, sunMass, Vector(-20, 5), 'orange')
    app.sun3 = Body(Vector(400, 350), sunRadius, sunMass, Vector(10, 25), 'yellow')

def restartSim(app):
    app.screen = [app.width//2, app.height//2, app.width, app.height]
    app.paused = False
    app.zoomedIn = False
    app.drawTrails = False
    app.tracerStep = 10
    app.G = 1
    app.dt = 0.01
    app.trailCutoffConstant = 5
    app.cameraMoveStep = 5

def setupGame(app):
    app.drawTrails = False
    Body.instances = []
    sunRadius = 10
    sunMass = 100000
    planet1Radius = 4
    planet1Mass = 200
    planet2Radius = 3
    planet2Mass = 10
    planet3Radius = 3
    planet3Mass = 15
    app.sun1 = Body(position=Vector(app.width//2,app.height//2), radius=sunRadius, mass=sunMass, velocity=Vector(0,0), color='gold', name='sun')
    app.planet1 = Body(position=Vector(app.width//2,160), radius=planet1Radius, mass=planet1Mass, velocity=Vector(15,0), color='red', name='mars')
    app.planet2 = Body(position=Vector(app.width//2,250), radius=planet2Radius, mass=planet2Mass, velocity=Vector(-18,0), color='green', name='venus')
    app.planet3 = Body(position=Vector(app.width//2,300), radius=planet3Radius, mass=planet3Mass, velocity=Vector(25,0), color='orange', name='earth')
    app.rocket = Rocket(position=Vector(app.width//2, 300), radius=4, mass=10, velocity=Vector(0,0),color='grey', name='rocket')

def rectanglesOverlap(left1, top1, width1, height1,
                      left2, top2, width2, height2): #slightly modified version of my own code
    right1 = left1 + width1  #got this from:https://cs3-112-f22.academy.cs.cmu.edu/exercise/4581
    right2 = left2 + width2
    bottom1 = top1 + height1
    bottom2 = top2 + height2
    if right2 >= right1 >= left2 or right1 >= right2 >= left1:
        if bottom2 >= bottom1 >= top2 or bottom1 >= bottom2 >= top1:
            return True
    return False

def redrawAll(app):
    drawRect(0,0,app.width,app.height)
    scale = app.width // app.screen[2]
    boxX = app.screen[0] - app.screen[2] // 2
    boxY = app.screen[1] - app.screen[3]//2
    for cBody in Body.instances:
        cBodyLeft = cBody.position.x - cBody.radius
        cBodyTop = cBody.position.y - cBody.radius
        if rectanglesOverlap(boxX, boxY, app.screen[2], app.screen[3],
                            cBodyLeft, cBodyTop, cBody.radius*2, cBody.radius*2):
            if isinstance(cBody, Rocket):
                x1 = (cBody.position.x - boxX) * scale + 10 
                y1 = (cBody.position.y - boxY) * scale
                x2 = x3 = (cBody.position.x - boxX) * scale - 5 
                y2 = y1 - 5
                y3 = y1 + 5
                angle = cBody.angle * (180 / math.pi)
                drawPolygon(x1, y1, x2, y2, x3, y3, fill='white', rotateAngle=angle)
            else:
                xPos = (cBody.position.x - boxX) * scale 
                yPos = (cBody.position.y - boxY) * scale
                drawCircle(xPos, yPos, cBody.radius*scale, fill = cBody.color)
        if app.drawTrails == True:
            for i in range(1,len(cBody.previousPositions), app.tracerStep):
                pos1 = cBody.previousPositions[i-1]
                pos2 = cBody.previousPositions[i] 
                x1 = (pos1.x - boxX) * scale
                y1 = (pos1.y - boxY) * scale
                x2 = (pos2.x - boxX) * scale
                y2 = (pos2.y - boxY) * scale
                drawLine(x1, y1, x2, y2, fill = 'white')
    if app.showLoadingScreen:
        displayLoadingScreenText(app)
    if not app.showLoadingScreen:
        drawRect(app.width-50, 25, 25, 50, border='white', fill=None)
        thrustHeight = 50 * app.rocket.thrustMagnitude / Rocket.maxThrust
        if thrustHeight > 0:
            drawRect(app.width-50, 25+(50-thrustHeight), 25, thrustHeight, fill='white')
    if app.paused and not app.zoomedIn:
        displayFullscreen(app)

def displayFullscreen(app):
    for cBody in Body.instances:
        labelX = cBody.position.x + cBody.radius + 5
        labelY = cBody.position.y - cBody.radius - 5
        squareWidth = len(cBody.name) * 8 + 3
        drawRect(labelX-3, labelY-8, squareWidth, 16, border='white')
        drawLabel(cBody.name, labelX, labelY, font='monospace', fill='white', align='left')
        drawLine(cBody.position.x, cBody.position.y, labelX-3, labelY+8, fill='grey')

def displayLoadingScreenText(app):
    drawLabel('Voyage', app.width//2, 200, font='monospace', fill='white', size=40)
    drawLabel('By Misho Alexandrov and Sebastian Rodriguez', app.width//2, 250, font='monospace',
              fill='white', size=15)
    drawRect(app.width//2-50, app.height-200, 100, 50, border='white', fill=None)
    drawLabel('start', app.width//2, app.height-175, font='monospace', fill='white', size=20)


def onMousePress(app, mouseX, mouseY):
    if not app.showLoadingScreen:
        mainGameMousePress(app, mouseX, mouseY)
    else:
        pass
        loadingScreenMousePress(app, mouseX, mouseY)

def loadingScreenMousePress(app, mouseX, mouseY):
    if (app.width//2 - 50) <= mouseX <= (app.width//2 + 50):
        if app.height-200 <= mouseY <= app.height-150:
            app.showLoadingScreen = False
            setupGame(app)

def mainGameMousePress(app, mouseX, mouseY):
    if 50 <= mouseX <= app.width - 50:
        if 50 <= mouseY <= app.height - 50:
            if not app.zoomedIn:
                app.screen[0], app.screen[1] = mouseX, mouseY
                app.screen[2] = app.screen[3] = 100
                app.zoomedIn = True
            else:
                app.screen[0], app.screen[1] = app.width//2, app.height//2
                app.screen[2], app.screen[3] = app.width, app.height
                app.zoomedIn = False

def onKeyPress(app, key):
    if not app.showLoadingScreen:
        mainGameKeyPress(app, key)

def mainGameKeyPress(app, key):
    if key == 'p':
        app.paused = not app.paused
    if key == 't':
        app.drawTrails = not app.drawTrails
    if (key == 's' and app.paused == True):
        takeStep(app)
    if 'm' == key:
        if not app.zoomedIn:
            app.screen[2] = 100
            app.screen[3] = 100
            app.zoomedIn = True
        else:
            app.screen[0] = app.width//2
            app.screen[1] = app.height//2
            app.screen[2] = app.width
            app.screen[3] = app.height
            app.zoomedIn = False


def onKeyHold(app, keys):
    if not app.showLoadingScreen:
        mainGameKeyHold(app, keys)

def mainGameKeyHold(app, keys):
    if app.screen[2] == 100:
        if 'w' in keys and app.screen[1] > 0:
            app.screen[1] -= 2
        if 's' in keys and app.screen[1] < app.height:
            app.screen[1] += 2
        if 'a' in keys and app.screen[0] > 0:
            app.screen[0] -= 2
        if 'd' in keys and app.screen[0] < app.width:
            app.screen[0] += 2
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
    app.rocket.updateThrust()
        
def takeStep(app):
    if app.zoomedIn and not app.paused:
        app.screen[0] = app.rocket.position.x
        app.screen[1] = app.rocket.position.y
    

    # compute net gravitational forces acting on each body
    for cBod in Body.instances:
        cBod.netForceFelt = Vector(0,0)
    for i in range(len(Body.instances)):
        for j in range(i+1,len(Body.instances)):
            cBod1 = Body.instances[i]
            cBod2 = Body.instances[j]
            
            r = cBod2.position - cBod1.position

            if r.mag > (cBod1.radius + cBod2.radius):

                Fg = r*(-app.G*cBod1.mass*cBod2.mass) / (r.mag**3)

                cBod1.netForceFelt -= Fg
                cBod2.netForceFelt += Fg

    if app.showLoadingScreen == False:
    #add rocket thrust
        app.rocket.netForceFelt += app.rocket.thrustVector

    #update momentums using net force
    for cBod in Body.instances:

        cBod.momentum = cBod.momentum + (cBod.netForceFelt * app.dt)
                
        #update trail
        cBod.previousPositions.append(cBod.position)
        if (len(cBod.previousPositions) * app.dt) > app.trailCutoffConstant:
            cBod.previousPositions.pop(0)
        
        cBod.position = cBod.position + (cBod.momentum/cBod.mass)*app.dt

def onStep(app):
    if not app.paused:
        takeStep(app)

def main():
    runApp(width=700, height=700)

main()