#Current lines: 637, target: 1200, progress; 53.08%
from cmu_graphics import *
from Classes import Vector, Body, Rocket, Projectile
from Drawings import drawCSM, drawLander
import math

def onAppStart(app):
    app.showLoadingScreen = True
    app.runTakeoff = False
    app.runLanding = False
    restartSim(app)
    loadingScreenSim(app)

def loadingScreenSim(app):
    app.drawTrails = True
    sunMass = 100000
    sunRadius = 10
    app.sun1 = Body(Vector(300, 300), sunRadius, sunMass, Vector(10, -20), 'red', name='1')
    app.sun2 = Body(Vector(500, 300), sunRadius, sunMass, Vector(-20, 5), 'orange', name='2')
    app.sun3 = Body(Vector(400, 350), sunRadius, sunMass, Vector(10, 25), 'yellow', name='3')

def restartSim(app):
    app.showStats = False
    app.showSettings = False
    app.screen = [app.width//2, app.height//2, app.width, app.height]
    app.paused = False
    app.zoomedIn = False
    app.drawTrails = False
    app.tracerStep = 10
    app.G = 1
    app.dt = 0.01
    app.trailCutoffConstant = 5
    app.cameraMoveStep = 5
    app.gameOver = False

def setupGameOver(app):
    app.runTakeoff = app.runLanding = app.showLoadingScreen = False
    Body.instances = []
    app.drawTrails = False
    app.step = 1

def onSurfaceEngineStart(app):
    app.dt = 0.07
    app.g = Vector(0,-9.8)
    if app.runTakeoff:
        app.rocket = Projectile(position = Vector(20,app.height), mass = 7.257, angle = 90, Cd = 0.342, crossSectionalArea=(math.pi*(0.37/2)**2), velocity = Vector(0,0), thrust = 0, burnTime = 10000, altitude=0)
    else:
        app.rocket = Projectile(position=Vector(20, -1600), mass=7.257, angle=90, Cd = 0.342, crossSectionalArea=(math.pi*(0.37/2)**2), velocity = Vector(0, 0), thrust=50, burnTime=10000, altitude = 2300)


def setupGame(app):
    app.dt = 0.01
    app.runLanding = False
    app.runTakeoff = False
    app.showStats = True
    app.step = 1
    app.showLoadingScreen = False
    app.showSettings = False
    app.zoomedIn = False
    app.gameOver = False
    app.screen = [app.width//2, app.height//2, app.width, app.height]
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
    app.planet2 = Body(position=Vector(app.width//2,250), radius=planet2Radius, mass=planet2Mass, velocity=Vector(-18,0), color='green', name='earth')
    app.planet3 = Body(position=Vector(app.width//2,300), radius=planet3Radius, mass=planet3Mass, velocity=Vector(25,0), color='orange', name='venus')
    app.rocket = Rocket(position=Vector(app.width//2, 500), radius=2, mass=10, velocity=Vector(0,0),color='grey', name='rocket')

def scalePosition(unscaledPosition):
    scale = 1
    newX = unscaledPosition.x / scale
    newY = unscaledPosition.y / scale
    scaledPosition = Vector(newX,newY)
    return scaledPosition

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

def distance(x1, y1, x2, y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

def redrawAll(app):
    boxX = app.screen[0] - app.screen[2] // 2
    boxY = app.screen[1] - app.screen[3]//2
    if app.runTakeoff or app.runLanding:
        if app.rocket.altitude < app.height//2:
            app.screen[1] = app.height//2
        else:
            app.screen[1] = app.rocket.position.y
        #app.screen[0] = app.rocket.position.x
        drawRect((-app.width-boxX)*5,app.height-boxY-20,app.width*15,app.height*20,fill='darkOliveGreen')
        drawRect((-app.width-boxX)*5, app.height-boxY-2820, app.width*15, app.height*4, fill=gradient('lightBlue', 'blue',
                                                                                        'midnightblue', 'darkBlue', 'black', start='bottom'))
        labelColor = 'white' if app.rocket.altitude > 1000 else 'black'
        drawLabel(f'Altitude: {rounded(app.rocket.altitude)} meters', 80, 40, fill=labelColor)
        redrawSurfaceEngine(app, boxX, boxY) if app.runTakeoff else redrawLanding(app, boxX, boxY)
        if app.gameOver:
            drawGameOverScreen(app)
    else:
        drawRect(0,0,app.width,app.height, fill='black')
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
        if not app.showLoadingScreen and not app.gameOver:
            nearest = findNearestBody(app.rocket)
            drawRect(app.width-50, 25, 25, 50, border='white', fill=None)
            thrustHeight = 50 * app.rocket.thrustMagnitude / Rocket.maxThrust
            if thrustHeight > 0:
                drawRect(app.width-50, 25+(50-thrustHeight), 25, thrustHeight, fill='white')
            drawCircle(app.width-100, 50, 25, border='white')
            drawCircle(app.width-100, 50, 5, fill='white')
            velocity = app.rocket.getVelocityMagnitude()
            if velocity > 50:
                extraAngle = 3 * math.pi / 2
            else:
                extraAngle = (3 * math.pi /2)  * (velocity / 100)
            lineFinalX = (app.width-100) + 25*math.cos(2*math.pi / 3 + extraAngle)
            lineFinalY = 50 + 25*math.sin(2 * math.pi / 3 + extraAngle)
            drawLine(app.width-100, 50, lineFinalX, lineFinalY, fill='white')
            drawLabel(f'x: {int(app.rocket.position.x)}', app.width-150, 25, font='monospace', fill='white', align='right')
            drawLabel(f'y: {int(app.rocket.position.y)}', app.width-150, 50, font='monospace', fill='white', align='right')
            drawLabel(f'nearestBody: {nearest}', app.width-150, 75, font='monospace', fill='white', align='right')
        if not app.zoomedIn and app.showStats:
            displayFullscreen(app)
        if app.gameOver:
            drawGameOverScreen(app)

def redrawSurfaceEngine(app, boxX, boxY):
    drawCSM(app, height=50, dx=boxX, dy=boxY, engineOn=True)

def redrawLanding(app, boxX, boxY):
    drawLander(app, dx=boxX, dy=boxY, height=50)

def drawGameOverScreen(app):
    squareWidth = 280
    if 40 > app.step:
        labelIndex = app.step // 5
        curLength = app.step * 7
    else:
        labelIndex = 10
        curLength = 280
    scaling = squareWidth/curLength
    drawRect(app.width//2, app.height//2, 280/scaling, 50, border='red', align='center')
    drawLabel('You died'[:labelIndex], app.width//2, app.height//2, fill='red', font='monospace', size=50)
    if app.step > 50:
        squareWidth = 98
        if 64 > app.step:
            labelIndex = (app.step - 50) // 2
            curLength = (app.step - 50) * 7
        else:
            labelIndex = 8
            curLength = 98
        scaling = squareWidth/curLength
        drawRect(app.width//2, app.height//2+100, squareWidth/scaling, 20, border='white', align='center', borderWidth=1)
        drawLabel('restart'[:labelIndex], app.width//2, app.height//2+100, fill='white', font='monospace', size=20)

def displayFullscreen(app):
    for cBody in Body.instances:
        if cBody.name != 'rocket':
            if len(cBody.name) * 2 > app.step:
                labelIndex = app.step // 2
            else:
                labelIndex = len(cBody.name)
            labelX = cBody.position.x + cBody.radius + 5
            labelY = cBody.position.y - cBody.radius - 5
            squareWidth = len(cBody.name) * 8 + 3
            if squareWidth > app.step:
                curLength = app.step
            else:
                curLength = squareWidth
            scaling = squareWidth/curLength
            drawRect(labelX-3, labelY-8, curLength, 16/scaling, border='silver', borderWidth=1)
            drawLabel(cBody.name[:labelIndex], labelX, labelY, font='monospace', fill='silver', align='left',
                    size=12/scaling)
            drawLine(cBody.position.x, cBody.position.y, labelX-3/scaling, labelY+8/scaling, fill='silver')
    cyclePosition = app.step % 50
    if not app.gameOver:
        drawCircle(app.rocket.position.x, app.rocket.position.y, (cyclePosition//2)+1, border='white',
                fill=None, opacity=100- cyclePosition*2)

def displayLoadingScreenText(app):
    if not app.showSettings:
        drawLabel('Voyage', app.width//2, 200, font='monospace', fill='white', size=40)
        drawLabel('By Misho Alexandrov and Sebastian Rodriguez', app.width//2, 250, font='monospace',
                fill='white', size=15)
        drawRect(app.width//2-50, app.height-200, 100, 50, border='white', fill=None)
        drawLabel('start', app.width//2, app.height-175, font='monospace', fill='white', size=20)
    else:
        for i in range(3):
            drawRect(app.width//2-100, 200+100*i, 200, 50, border='white')
        drawLabel('Stage 1: Takeoff', app.width//2, 225, fill='white', font='monospace', size=19)
        drawLabel('Stage 2: Orbit', app.width//2, 325, fill='white', font='monospace', size=19)
        drawLabel('Stage 3: Landing', app.width//2, 425, fill='white', font='monospace', size=19)


def findNearestBody(cBody):
    nearest = float('inf')
    best = None
    for entity in Body.instances:
        if entity != cBody:
            currentDistance = distance(cBody.position.x, cBody.position.y,
                                       entity.position.x, entity.position.y)
            if currentDistance < nearest:
                nearest = currentDistance
                best = entity
    return best.name

def onMousePress(app, mouseX, mouseY):
    if not app.gameOver:
        if not app.showLoadingScreen:
            mainGameMousePress(app, mouseX, mouseY)
        else:
            loadingScreenMousePress(app, mouseX, mouseY)
    else:
        gameOverMousePress(app, mouseX, mouseY)

def gameOverMousePress(app, mouseX, mouseY):
    if 301 <= mouseX <= 399:
        if 440 <= mouseY <= 460:
            app.showLoadingScreen = True
            app.runTakeoff = False
            app.runLanding = False
            restartSim(app)
            loadingScreenSim(app)

def loadingScreenMousePress(app, mouseX, mouseY):
    if not app.showSettings:
        if (app.width//2 - 50) <= mouseX <= (app.width//2 + 50):
            if app.height-200 <= mouseY <= app.height-150:
                app.showSettings = True
    else:
        if (app.width//2 - 100) <= mouseX <= (app.width // 2 + 100):
            if 200 <= mouseY <= 250:
                app.runTakeoff = True
                onSurfaceEngineStart(app)
            elif 300 <= mouseY <= 350:
                setupGame(app)
            elif 400 <= mouseY <= 450:
                app.runLanding = True
                onSurfaceEngineStart(app)
                
            

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
    if not app.showLoadingScreen and not app.gameOver:
        mainGameKeyPress(app, key)

def mainGameKeyPress(app, key):
    if key == 'i':
        app.showStats = not app.showStats
        app.step = 1
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
    if not app.showLoadingScreen and not app.gameOver:
        mainGameKeyHold(app, keys)
    elif app.runTakeoff or app.runLanding:
        rocketKeyHold(app, keys)

def rocketKeyHold(app, keys):
    if 'left' in keys:
        app.rocket.angle += 5
    if 'right' in keys:
        app.rocket.angle -= 5
    app.rocket.updateDirection()

    if 'down' in keys:
        app.rocket.thrust -= 10
    if 'up' in keys:
        app.rocket.thrust += 10

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
    if app.runTakeoff or app.runLanding:
        takeStepForSurfaceEngine(app)
    elif not app.gameOver:
        mainTakeStep(app)

def mainTakeStep(app):
    if app.zoomedIn and not app.paused:
        app.screen[0] = app.rocket.position.x
        app.screen[1] = app.rocket.position.y
    
    if not app.showLoadingScreen:
        rocketLeft = app.rocket.position.x - app.rocket.radius
        rocketTop = app.rocket.position.y - app.rocket.radius
        for cBody in Body.instances:
            if not isinstance(cBody, Rocket):
                cBodyLeft = cBody.position.x - cBody.radius
                cBodyTop = cBody.position.y - cBody.radius
                if rectanglesOverlap(rocketLeft, rocketTop, app.rocket.radius*2, app.rocket.radius*2,
                                    cBodyLeft, cBodyTop, cBody.radius*2, cBody.radius*2):
                    app.gameOver = True
                    setupGameOver(app)


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
        cBod.updateVelocity()

def takeStepForSurfaceEngine(app):
    Fg = app.g * app.rocket.mass
    
    if (app.rocket.thrust > 0) and (app.rocket.velocity.y > 0): #for now, only worry about drag if rocket is ascending or in powered descent
        H = 8000 # "scale height"
        p0 = 1.225 # air density at sea level 
        p = p0 * math.e ** (-app.rocket.altitude / H) #air density at current altitude
        Fd =  (app.rocket.directionVector * (-1) * ((1/2) * p * (app.rocket.velocity.mag**2) * app.rocket.crossSectionalArea * app.rocket.Cd)).roundVector(1)
    else: # figure out falling back down drag force later
       Fd = Vector(0,0)

    if app.rocket.burnTime > 0:
        Ft = app.rocket.directionVector * app.rocket.thrust
        app.rocket.burnTime -= 1
    elif app.rocket.burnTime == 0:
        app.rocket.thrust = 0
        Ft = Vector(0,0)

    app.rocket.netForceFelt = Fg + Fd + Ft 
    #update momentum using net force
    app.rocket.momentum = app.rocket.momentum + (app.rocket.netForceFelt * app.dt)
    app.rocket.velocity = app.rocket.momentum / app.rocket.mass
    deltaPosition = (app.rocket.momentum/app.rocket.mass)*app.dt
    if app.rocket.altitude <= 0:
        deltaPosition = Vector(0, 0) if deltaPosition.y < 0 else deltaPosition
        if app.rocket.getVelocity() >= 100:
            app.gameOver = True
            app.step = 1
            setupGameOver(app)
    app.rocket.position = app.rocket.position - deltaPosition
    app.rocket.altitude += deltaPosition.y
    if app.rocket.altitude > 2300:
        setupGame(app)

def onStep(app):
    if not app.showLoadingScreen:
        app.step += 1
    if not app.paused:
        takeStep(app)

def main():
    runApp(width=700, height=700)

main()