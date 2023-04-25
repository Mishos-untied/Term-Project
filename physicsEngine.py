#Current lines: 928, target: 1000
from cmu_graphics import *
from Classes import Vector, Body, Rocket, Projectile
from Drawings import drawCSM, drawLander, drawLaunchRocket
import math
import copy
import random

def onAppStart(app):
    app.showLoadingScreen = True
    app.runTakeoff = False
    app.runLanding = False
    app.step = 1
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
    app.fuelLeft = 50000
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
    app.runTakeoffInstructions = app.runOrbitInstructions = app.runLandingInstructions = False
    app.runOrbit = False
    app.fuelLeft = 50000

def setupGameOver(app):
    app.runTakeoff = app.runLanding = app.showLoadingScreen = False
    Body.instances = []
    app.drawTrails = False
    app.step = 1

def onSurfaceEngineStart(app):
    app.runOrbit = False
    app.showSettings = False
    app.runTakeoffInstructions = False
    app.dt = 0.07
    app.g = Vector(0,-9.8)
    app.screen[2] = app.screen[3] = app.width
    if app.runTakeoff:
        app.rocket = Projectile(position = Vector(20,app.height), mass = 7.257, angle = 90, Cd = 0.342, crossSectionalArea=(math.pi*(0.37/2)**2), velocity = Vector(0,0), thrust = 0, burnTime = app.fuelLeft, altitude=0)
        app.screen[1] = app.height//2
    else:
        app.rocket = Projectile(position = Vector(20,-2400), mass = 7.257, angle = 90, Cd = 0.342, crossSectionalArea=(math.pi*(0.37/2)**2), velocity = Vector(0,0), thrust = 0, burnTime = app.fuelLeft, altitude=3100)
        app.screen[0] = app.width//2
        app.screen[1] = app.rocket.position.y

def setupGame(app):
    app.dt = 0.01
    app.runLander = app.runTakeoff = False
    app.showStats = True
    app.runOrbit = True
    app.step = 1
    app.showLoadingScreen = False
    app.showSettings = False
    app.zoomedIn = False
    app.gameOver = False
    app.screen = [app.width//2, app.height//2, app.width, app.height]
    app.drawTrails = False
    Body.instances = []
    app.projectedPositions = []
    app.rocketProjectedPositions = []
    app.projected = False
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
    app.planet2 = Body(position=Vector(app.width//2,550), radius=planet2Radius, mass=planet2Mass, velocity=Vector(-18,0), color='green', name='earth')
    app.planet3 = Body(position=Vector(app.width//2,300), radius=planet3Radius, mass=planet3Mass, velocity=Vector(25,0), color='orange', name='venus')
    app.rocket = Rocket(position=Vector(app.width//2, 530), radius=2, mass=10, velocity=Vector(-18,0),color='grey', name='rocket', burnTime=app.fuelLeft)

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
    if app.runTakeoffInstructions:
        drawTakeoffInstructions(app)
    elif app.runOrbitInstructions:
        drawOrbitInstructions(app)
    elif app.runLandingInstructions:
        drawLandingInstructions(app)
    elif app.runTakeoff or app.runLanding:
        if app.rocket.altitude < app.height//2:
            app.screen[1] = app.height//2
        else:
            app.screen[1] = app.rocket.position.y
        app.screen[0] = app.width//2
        groundColor = 'darkOliveGreen' if app.runTakeoff else 'fireBrick'
        drawRect((-app.width-boxX)*5,app.height-boxY-20,app.width*15,app.height*20,fill=groundColor)
        drawRect((-app.width-boxX)*5, app.height-boxY-(app.height*8-680), app.width*15, app.height*7, fill=gradient('lightBlue', 'blue',
                                                                                        'midnightblue', 'darkBlue', 'black', start='bottom'))
        labelColor = 'white' if app.rocket.altitude > 1000 else 'black'
        drawLabel(f'Altitude: {rounded(app.rocket.altitude)} meters', 80, 40, fill=labelColor)
        rocketVelocity = int(app.rocket.getVelocity())
        rocketVelocity = -rocketVelocity if app.rocket.velocity.y < 0 else rocketVelocity
        drawLabel(f'Velocity: {rocketVelocity} m/s', 80, 80, fill=labelColor)
        drawLabel(f'Fuel: {app.rocket.burnTime}', 80, 120, fill=labelColor)
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
            if velocity > 100:
                extraAngle = 3 * math.pi / 2
            else:
                extraAngle = (3 * math.pi /2)  * (velocity / 100)
            lineFinalX = (app.width-100) + 25*math.cos(2*math.pi / 3 + extraAngle)
            lineFinalY = 50 + 25*math.sin(2 * math.pi / 3 + extraAngle)
            drawLine(app.width-100, 50, lineFinalX, lineFinalY, fill='white')
            drawLabel(f'x: {int(app.rocket.position.x)}', app.width-150, 25, font='monospace', fill='white', align='right')
            drawLabel(f'y: {int(app.rocket.position.y)}', app.width-150, 50, font='monospace', fill='white', align='right')
            drawLabel(f'nearestBody: {nearest}', app.width-150, 75, font='monospace', fill='white', align='right')
            fuelColor = 'white' if app.rocket.burnTime > 10000 else 'red'
            drawLabel(f'fuel left: {app.rocket.burnTime}', app.width-150, 100, fill=fuelColor, font='monospace', align='right')
            if app.paused:
                for position in app.projectedPositions:
                    drawCircle(position.x, position.y, 1, fill='lightBlue')
                for position in app.rocketProjectedPositions:
                    drawCircle(position.x, position.y, 1, fill='lightGreen')
        
        if not app.zoomedIn and app.showStats:
            displayFullscreen(app)
        if app.gameOver:
            drawGameOverScreen(app)

def drawTakeoffInstructions(app):
    drawRect(0, 0, app.width, app.height, fill='black')
    titleIndex = getLineIndex(app, 1, 10, 'Takeoff')
    drawLabel('Takeoff'[:titleIndex], app.width//2, 100, size=50, fill='white', font='monospace')
    firstLine = 'Your current mission is to bring the rocket into low earth orbit'
    firstLineIndex = getLineIndex(app, 50, 2, firstLine)
    drawLabel(firstLine[:firstLineIndex], app.width//2,
              150, fill='white', font='monospace', size=15)
    secondLine = '1. Press up and down to increase / decrease thrust'
    secondLineIndex = getLineIndex(app, 180, 2, secondLine)
    drawLabel(secondLine[:secondLineIndex], app.width//2, 300, size=13, fill='white', font='monospace')
    thirdLine = '2. Your goal is to pass the Karman line, approximately 100 km above the surface'
    thirdLineIndex = getLineIndex(app, 170, 3, thirdLine)
    drawLabel(thirdLine[:thirdLineIndex], app.width//2, 350, size=13, fill='white', font='monospace')
    fourthLine = '3. Be wary not to run out of fuel'
    fourthLineIndex = getLineIndex(app, 175, 2, fourthLine)
    drawLabel(fourthLine[:fourthLineIndex], app.width//2, 400, size=13, fill='white', font='monospace')
    fifthLine = '4. at aout 80 km, begin to turn laterally in order to enter earth orbit'
    fifthLineIndex = getLineIndex(app, 180, 2, thirdLine)
    drawLabel(fifthLine[:fifthLineIndex], app.width//2, 450, size=13, fill='white', font='monospace')
    if app.step > 200:
        buttonMessage = 'start'
        buttonMessageIndex = getLineIndex(app, 200, 10, buttonMessage)
        scaling = (app.step-200) / 50 if app.step < 250 else 1
        drawRect(app.width//2, 550, 100*scaling, 50, border='white', align='center')
        drawLabel(buttonMessage[:buttonMessageIndex], app.width//2, 550, fill='gold', font='monospace', size=20)

def drawOrbitInstructions(app):
    drawRect(0, 0, app.width, app.height, fill='black')
    title = 'orbit'
    titleIndex = getLineIndex(app, 1, 10, title)
    drawLabel(title[:titleIndex], app.width//2, 100, fill='white', font='monospace', size=50)
    firstLine = 'You must pilot the rocket to mars'
    firstLineIndex = getLineIndex(app, 50, 2, firstLine)
    drawLabel(firstLine[:firstLineIndex], app.width//2, 150, fill='white', font='monospace', size=15)
    secondLine = '1. Use the up and down keys to increase \ decrease thrust'
    secondLineIndex = getLineIndex(app, 100, 3, secondLine)
    drawLabel(secondLine[:secondLineIndex], app.width//2, 300, fill='white', font='monospace', size=13)
    thirdLine = '2. Use the left and right keys to rotate the rocket'
    thirdLineIndex = getLineIndex(app, 90, 2, thirdLine)
    drawLabel(thirdLine[:thirdLineIndex], app.width//2, 350, fill='white', font='monospace', size=13)
    fourthLine = '3. press p to project orbits and i to display planet names'
    fourthLineIndex = getLineIndex(app, 98, 2, fourthLine)
    drawLabel(fourthLine[:fourthLineIndex], app.width//2, 400, fill='white', font='monospace', size=13)
    fifthLine = '4. x/y coordinates, velocity, and thrust are all displayed in the top right'
    fifthLineIndex = getLineIndex(app, 110, 1, fifthLine)
    drawLabel(fifthLine[:fifthLineIndex], app.width//2, 450, fill='white', font='monospace', size=13)
    sixthLine = '5. as always, be sure to conserve fuel'
    sixthLineIndex = getLineIndex(app, 100, 2, sixthLine)
    drawLabel(sixthLine[:sixthLineIndex], app.width//2, 500, fill='white', font='monospace', size=13)
    if app.step > 130:
        buttonMessage = 'start'
        buttonMessageIndex = getLineIndex(app, 130, 10, buttonMessage)
        scaling = (app.step-130) / 50 if app.step < 180 else 1
        drawRect(app.width//2, 550, 100*scaling, 50, border='white', align='center')
        drawLabel(buttonMessage[:buttonMessageIndex], app.width//2, 550, fill='gold', font='monospace', size=20)

def drawLandingInstructions(app):
    drawRect(0, 0, app.width, app.height, fill='black')
    title = 'Landing'
    titleIndex = getLineIndex(app, 1, 10, title)
    drawLabel(title[:titleIndex], app.width//2, 100, fill='white', size=50, font='monospace')
    firstLine = 'You must now pilot the lander onto the surface of the planet'
    firstLineIndex = getLineIndex(app, 55, 2, firstLine)
    drawLabel(firstLine[:firstLineIndex], app.width//2, 150, fill='white', font='monospace', size=15)
    secondLine = '1. The up and down keys will increase and decrease thrust'
    secondLineIndex = getLineIndex(app, 80, 1, secondLine)
    drawLabel(secondLine[:secondLineIndex], app.width//2, 300, fill='white', font='monospace', size=13)
    thirdLine = '2. In order to safely touch down, you must approach with a velocity < 100 m/s'
    thirdLineIndex = getLineIndex(app, 75, 2, thirdLine)
    drawLabel(thirdLine[:thirdLineIndex], app.width//2, 350, fill='white', font='monospace', size=13)
    fourthLine = '3. Fuel is exceedingly low at this stage, use the remainder wisely'
    fourthLineIndex = getLineIndex(app, 80, 2, fourthLine)
    drawLabel(fourthLine[:fourthLineIndex], app.width//2, 400, fill='white', font='monospace', size=13)
    if app.step > 120:
        buttonMessage = 'start'
        buttonMessageIndex = getLineIndex(app, 130, 10, buttonMessage)
        scaling = (app.step-120) / 50 if app.step < 170 else 1
        drawRect(app.width//2, 550, 100*scaling, 50, border='white', align='center')
        drawLabel(buttonMessage[:buttonMessageIndex], app.width//2, 550, fill='gold', font='monospace', size=20)

def getLineIndex(app, startTime, speed, message):
    if app.step < startTime:
        return 0
    else:
        return ((app.step - startTime) // speed if 
                app.step < startTime * len(message) * speed else len(message))
    
def redrawSurfaceEngine(app, boxX, boxY):
    drawLaunchRocket(app,height=200, dx=boxX, dy=boxY, engineOn=False)

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
    deathMessageIndex = getLineIndex(app, 20, 3, app.deathMessage)
    drawLabel(app.deathMessage[:deathMessageIndex], app.width//2, app.height//2+50, fill='white', font='monospace', size=15)

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
    if not app.gameOver and not app.paused:
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


def onMouseDrag(app, mouseX, mouseY):
    if app.runTakeoffInstructions:
        if (app.width//2 - 50) <= mouseX <= (app.width//2 + 50):
            if 500 <= mouseY <= 550:
                app.takeoffButtonColor = 'white'
        else:
            app.takeoffButtonColor = 'grey'

def onMousePress(app, mouseX, mouseY):
    if not app.gameOver:
        if not app.showLoadingScreen and app.runOrbit:
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
    if (not app.showSettings and not app.runTakeoffInstructions 
        and not app.runOrbitInstructions and not app.runLandingInstructions):
        if (app.width//2 - 50) <= mouseX <= (app.width//2 + 50):
            if app.height-200 <= mouseY <= app.height-150:
                app.showSettings = True
    elif app.showSettings:
        if (app.width//2 - 100) <= mouseX <= (app.width // 2 + 100):
            if 200 <= mouseY <= 250:
                if not app.runTakeoffInstructions:
                    app.runTakeoffInstructions = True
                    app.step = 1
                    app.showSettings = False
                    app.takeoffButtonColor = 'grey'
            elif 300 <= mouseY <= 350:
                app.runOrbitInstructions = True
                app.step = 1
                app.showSettings = False
            elif 400 <= mouseY <= 450:
                app.runLandingInstructions = True
                app.step = 1
                app.showSettings = False
    else:
        if app.width//2 - 50 <= mouseX <= app.width//2 + 50:
            if 525 <= mouseY <= 575:
                if app.runTakeoffInstructions:
                     app.runTakeoff = True
                     onSurfaceEngineStart(app)
                elif app.runOrbitInstructions:
                    app.runOrbitInstructions = False
                    app.zoomedIn = True
                    setupGame(app)
                elif app.runLandingInstructions:
                    app.runLandingInstructions = False
                    app.showLoadingScreen = False
                    app.runLanding = True
                    onSurfaceEngineStart(app)

    
                
       
def mainGameMousePress(app, mouseX, mouseY):
    if 50 <= mouseX <= app.width - 50:
        if 50 <= mouseY <= app.height - 50:
            if not app.zoomedIn and not app.paused:
                app.screen[0], app.screen[1] = app.rocket.position.x, app.rocket.position.y
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

        if app.paused == False:
            app.projected = False
        elif app.paused:
            app.zoomedIn = False
            app.screen[0] = app.width // 2
            app.screen[1] = app.height // 2
            app.screen[2] = app.width
            app.screen[3] = app.height
            if app.projected == False:
                generateProjectedPositions(app, 0.1, 100)

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
    if not app.showLoadingScreen and not app.gameOver and app.runOrbit:
        mainGameKeyHold(app, keys)
    elif app.runLanding or app.runTakeoff:
        rocketKeyHold(app, keys)

def rocketKeyHold(app, keys):
    if 'left' in keys:
        app.rocket.angle += 5
    if 'right' in keys:
        app.rocket.angle -= 5
    app.rocket.updateDirection()

    if 'down' in keys and app.rocket.burnTime > 0 and app.rocket.thrust > 0:
        app.rocket.thrust -= 10
    if 'up' in keys and app.rocket.burnTime > 0:
        app.rocket.thrust += 10

def generateProjectedPositions(app, stepDt, steps):

    app.projectedPositions = []
    app.rocketProjectedPositions = []


    newBodiesList = copy.deepcopy(Body.instances)
    
    for i in range(steps):
        # compute net gravitational forces acting on each body
        for cBod in newBodiesList:
            cBod.netForceFelt = Vector(0,0)
        for i in range(len(newBodiesList)):
            for j in range(i+1,len(Body.instances)):
                cBod1 = newBodiesList[i]
                cBod2 = newBodiesList[j]
                
                r = cBod2.position - cBod1.position

                if r.mag > (cBod1.radius + cBod2.radius):

                    Fg = r*(-app.G*cBod1.mass*cBod2.mass) / (r.mag**3)

                    cBod1.netForceFelt -= Fg
                    cBod2.netForceFelt += Fg

        for cBod in newBodiesList:

            cBod.momentum = cBod.momentum + (cBod.netForceFelt * stepDt)
                    
            cBod.velocity = cBod.momentum / cBod.mass

            cBod.position = cBod.position + (cBod.momentum/cBod.mass)*stepDt
            if isinstance(cBod, Rocket):
                app.rocketProjectedPositions.append(cBod.position)
            else:
                app.projectedPositions.append(cBod.position)

    app.projected = True


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
    if 'up' in keys and 'down' not in keys and app.rocket.burnTime > 0:
        app.rocket.thrustMagnitude += 3
    if 'down' in keys and 'up' not in keys and app.rocket.burnTime > 0:
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
        app.screen[2] = app.screen[3] = 100
    
    if not app.showLoadingScreen:
        rocketLeft = app.rocket.position.x - app.rocket.radius
        rocketTop = app.rocket.position.y - app.rocket.radius
        # check for collisions + out of bounds
        for cBody in Body.instances:
            if not isinstance(cBody, Rocket):
                cBodyLeft = cBody.position.x - cBody.radius
                cBodyTop = cBody.position.y - cBody.radius
                if rectanglesOverlap(rocketLeft, rocketTop, app.rocket.radius*2, app.rocket.radius*2,
                                    cBodyLeft, cBodyTop, cBody.radius*2, cBody.radius*2):
                    app.gameOver = True
                    app.deathMessage = f'You crashed into {cBody.name}'
                    setupGameOver(app)
        app.rocket.burnTime -= app.rocket.thrustMagnitude // 5
        if (-100 >= app.rocket.position.x or 800 <= app.rocket.position.x
            or -100 >= app.rocket.position.y or 800 <= app.rocket.position.y):
            app.gameOver = True
            app.deathMessage = 'You flew out of bounds'
            setupGameOver(app)
        if app.rocket.burnTime <= 0:
            app.rocket.thrustVector = Vector(0, 0)
            app.rocket.thrustMagnitude = 0
            app.rocket.burnTime = 0


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
    #check if the rocket is close to mars
    if app.runOrbit:
        rocketCx, rocketCy = app.rocket.position.x, app.rocket.position.y
        marsCx, marsCy = app.planet1.position.x, app.planet1.position.y
        if distance(rocketCx, rocketCy, marsCx, marsCy) < 10:
            app.step = 1
            app.fuelLeft = app.rocket.burnTime
            app.showSettings = False
            app.showLoadingScreen = True
            app.runLandingInstructions = True
    

def takeStepForSurfaceEngine(app):
    Fg = app.g * app.rocket.mass
    
    if (app.rocket.thrust > 0) and (app.rocket.velocity.y > 0): #for now, only worry about drag if rocket is ascending or in powered descent
        H = 8000 # "scale height"
        p0 = 1.225 # air density at sea level 
        p = p0 * math.e ** (-app.rocket.altitude / H) #air density at current altitude
        Fd =  (app.rocket.directionVector * (-1) * ((1/2) * p * (app.rocket.velocity.mag**2) * app.rocket.crossSectionalArea * app.rocket.Cd)).roundVector(1)
    else: # figure out falling back down drag force later
       Fd = Vector(0,0)
    app.rocket.burnTime -= app.rocket.thrust // 20
    if app.rocket.burnTime > 0:
        Ft = app.rocket.directionVector * app.rocket.thrust
    else:
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
            chance = random.randint(1, 10)
            if chance == 5:
                app.deathMessage = "helpful tip: don't crash"
            else:
                app.deathMessage = 'Your descent velocity was too high'
            setupGameOver(app)
        app.rocket.momentum = Vector(0, 0) if deltaPosition == Vector(0, 0) else app.rocket.momentum
        app.rocket.velocity = app.rocket.momentum / app.rocket.mass
        # if the rocket ends up under the surface, redraw it so it isn't
        app.rocket.position.y = 680
        app.rocket.altitude = 0
    app.rocket.position = app.rocket.position - deltaPosition
    app.rocket.altitude += deltaPosition.y
    if app.rocket.altitude > 3300:
        if app.runTakeoff:
            app.step = 1
            app.fuelLeft = app.rocket.burnTime
            app.runOrbitInstructions = True
            app.runTakeoff = False
        else:
            app.deathMessage = 'you went the wrong way'
            app.gameOver = True
            setupGameOver(app)

def onStep(app):
    app.step += 1
    if not app.paused:
        takeStep(app)

def main():
    runApp(width=700, height=700)

main()