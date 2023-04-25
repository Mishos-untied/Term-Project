#Current lines: 703, target: 1000
from cmu_graphics import *
from PIL import Image
from Classes import Vector, Body, Rocket, Projectile
from Drawings import drawCSM, drawLander, drawLaunchRocket
import math
import copy

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
    app.showStats = False
    app.showSettings = False
    app.screen = [app.width//2, app.height//2, app.width, app.height]
    app.paused = False
    app.zoomedIn = False
    app.zoomCounter = 0
    app.drawTrails = False
    app.G = 1
    app.dt = 0.02
    app.tracerStep = 30
    app.tracerLength = 10
    app.trailCutoffConstant = 5
    app.cameraMoveStep = 5
    app.gameOver = False
    app.runTakeoffInstructions = False

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
        app.rocket = Projectile(position = Vector(20,-1600), mass = 7.257, angle = 90, Cd = 0.342, crossSectionalArea=(math.pi*(0.37/2)**2), velocity = Vector(0,0), thrust = 0, burnTime = 10000, altitude=2300)

def setupGame(app):
    app.dt = 0.0001
    app.runLander = app.runTakeoff = False
    app.showStats = True
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
    sunRadius = 9
    sunMass = 10000000
    planetARadius = 3
    planetAMass = 5
    planetBRadius = 5
    planetBMass = 100
    planetCRadius = 4
    planetCMass = 50
    app.planet = Body(position=Vector(app.width//2,app.height//2), radius=sunRadius, mass=sunMass, velocity=Vector(0,0), color='gold', name='planet')
    app.moonA = Body(position=Vector(app.width//2,app.height//2 + 80), radius=planetARadius, mass=planetAMass, velocity=Vector(354,0), color='red', name='moon A')
    app.moonB = Body(position=Vector(app.width//2,app.height//2 - 150), radius=planetBRadius, mass=planetBMass, velocity=Vector(-260,0), color='green', name='moon B')
    app.moonC = Body(position=Vector(app.width//2 + 270,app.height//2), radius=planetCRadius, mass=planetCMass, velocity=Vector(0,-190), color='orange', name='moon C')
    app.rocket = Rocket(position=Vector(app.width//2, app.height//2-15), radius=0.00001, mass=1e-21, velocity=Vector(-820,0),color='grey', name='rocket')

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

def image(link, scale):
    # Load the PIL image
    image = Image.open(link)
    # Convert each PIL image to a CMUImage for drawing
    image = CMUImage(image)
    imageWidth, imageHeight = getImageSize(link)
    image = Image.open(link)
    image = image.resize((imageWidth//scale,imageHeight//scale))
    image = CMUImage(image)
    return image

    

def redrawAll(app):


    # # Load the PIL image
    # CSM0 = Image.open('CSM_0.png')
    # # Convert each PIL image to a CMUImage for drawing
    # CSM0 = CMUImage(CSM0)
    # imageWidth, imageHeight = getImageSize("CSM_0.png")
    # CSM0 = Image.open("CSM_0.png")
    # CSM0 = CSM0.resize((imageWidth,imageHeight))
    # CSM0 = CMUImage(CSM0)
    
    

    


    
    boxX = app.screen[0] - app.screen[2] // 2
    boxY = app.screen[1] - app.screen[3]//2
    if app.runTakeoffInstructions:
        drawTakeoffInstructions(app)
    elif app.runTakeoff or app.runLanding:
        if app.rocket.altitude < app.height//2:
            app.screen[1] = app.height//2
        else:
            app.screen[1] = app.rocket.position.y
        #app.screen[0] = app.rocket.position.x
        drawRect((-app.width-boxX)*5,app.height-boxY-20,app.width*15,app.height*20,fill='darkOliveGreen')
        drawRect((-app.width-boxX)*5, app.height-boxY-(app.height*8-680), app.width*15, app.height*7, fill=gradient('lightBlue', 'blue',
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
                    x = (cBody.position.x - boxX) * scale 
                    y = (cBody.position.y - boxY) * scale

                    x1 = (cBody.position.x - boxX) * scale + 10 
                    y1 = (cBody.position.y - boxY) * scale
                    x2 = x3 = (cBody.position.x - boxX) * scale - 5 
                    y2 = y1 - 5
                    y3 = y1 + 5

                    angle = cBody.angle * (180 / math.pi)
                    if not app.zoomedIn:
                        drawPolygon(x1, y1, x2, y2, x3, y3, fill='white', rotateAngle=angle)
                    if app.zoomedIn:
                        thrustDecimal = cBody.thrustMagnitude / cBody.maxThrust
                        print(thrustDecimal)
                        thrustLevelIndex = math.floor((thrustDecimal/2)*10)
                        if app.zoomCounter == 1:
                            scale = 200
                            drawCircle(x,y,1,fill='white')
                            drawLine(x-3,y,x+3,y,lineWidth=0.5,fill='silver')
                            drawLine(x,y+3,x,y-3,lineWidth=0.5,fill='silver')
                        elif app.zoomCounter == 2:
                            scale = 30
                        elif app.zoomCounter == 3:
                            scale = 8
                        print(scale)
                        CSM0 = image("CSM_0.png", scale)
                        CSM1 = image("CSM_1.png", scale)
                        CSM2 = image("CSM_2.png", scale)
                        CSM3 = image("CSM_3.png", scale)
                        CSM4 = image("CSM_4.png", scale)
                        CSM5 = image("CSM_5.png", scale)
                        CSMList = [CSM0, CSM1, CSM2, CSM3, CSM4, CSM5]

                        drawImage(CSMList[thrustLevelIndex], x, y, align = 'center', rotateAngle = angle+90)

                else:
                    xPos = (cBody.position.x - boxX) * scale 
                    yPos = (cBody.position.y - boxY) * scale
                    drawCircle(xPos, yPos, cBody.radius*scale, fill = cBody.color)
            if app.drawTrails == True:
                for i in range(app.tracerLength,len(cBody.previousPositions), app.tracerStep):
                    pos1 = cBody.previousPositions[i-app.tracerLength]
                    pos2 = cBody.previousPositions[i] 
                    x1 = (pos1.x - boxX) * scale
                    y1 = (pos1.y - boxY) * scale
                    x2 = (pos2.x - boxX) * scale
                    y2 = (pos2.y - boxY) * scale
                    drawLine(x1, y1, x2, y2, fill = 'white', lineWidth = 1)
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

            #projections
            if app.paused:
                for i in range(len(app.projectedPositions)):
                    position = app.projectedPositions[i]
                    color = getRainbowColor(i, len(app.projectedPositions))
                    drawCircle(position.x, position.y, 0.7, fill=color)
                for i in range(len(app.rocketProjectedPositions)):
                    position = app.rocketProjectedPositions[i]
                    color = getRainbowColor(i, len(app.rocketProjectedPositions))
                    drawCircle(position.x, position.y, 0.7, fill=color)
        

        if not app.zoomedIn and app.showStats:
            displayFullscreen(app)
        if app.gameOver:
            drawGameOverScreen(app)

def getRainbowColor(colorNum, rainbowSteps):
    stepSize = 913/rainbowSteps
    n = int(colorNum * stepSize)

    # 0 <= n <= 913
    if n <= 127: #red-orange
        return rgb(255,n,0)
    elif 127 < n <= 255: # orange-yellow
        return rgb(255,n,0)
    elif 255 < n <= 510: #yellow-green
        i = n - 255
        return rgb(255-i,255,0)
    elif 510 < n <= 765: #green-blue
        i = n - 510
        return rgb(0,255-i,i)
    elif 765 < n <= 913:
        i = n - 765
        j = 0.297*i
        return rgb(i,0,255-j)


def drawTakeoffInstructions(app):
    drawRect(0, 0, app.width, app.height, fill='black')
    titleIndex = 7 * app.step//50 if app.step < 50 else 7
    drawLabel('Takeoff'[:titleIndex], app.width//2, 100, size=50, fill='white', font='monospace')
    firstLine = 'Your current mission is to bring the rocket into low earth orbit'
    if app.step <= 50:
        firstLineIndex = 0
    else:
        firstLineIndex = len(firstLine) * (app.step - 50) // 100 if app.step < 70 else len(firstLine)
    drawLabel(firstLine[:firstLineIndex], app.width//2,
              150, fill='white', font='monospace', size=15)
    
def redrawSurfaceEngine(app, boxX, boxY):
    LaunchRocket0 = image("LAUNCHROCKET_0.png",scale = 10)
    LaunchRocket1 = image("LAUNCHROCKET_1.png",scale = 10)
    LaunchRocket2 = image("LAUNCHROCKET_2.png",scale = 10)
    print(boxX, boxY)
    # drawLander(app, dx=boxX, dy=boxY, height=50)
    angle = app.rocket.angle #* (180 / math.pi)
    print(app.rocket.position.x, app.rocket.position.y)
    drawImage(LaunchRocket0, app.rocket.position.x, app.rocket.position.y, align = 'center', rotateAngle = angle)


    drawLaunchRocket(app,height=200, dx=boxX, dy=boxY, engineOn=False)
    
def redrawLanding(app, boxX, boxY):
    Lander0 = image("Lander_0.png",scale = 10)
    Lander1 = image("Lander_1.png",scale = 10)
    Lander2 = image("Lander_2.png",scale = 10)
    Lander3 = image("Lander_3.png",scale = 10)
    Lander4 = image("Lander_4.png",scale = 10)
    Lander5 = image("Lander_5.png",scale = 10)
    Lander6 = image("Lander_6.png",scale = 10)
    Lander7 = image("Lander_7.png",scale = 10)
    print(boxX, boxY)
    # drawLander(app, dx=boxX, dy=boxY, height=50)
    angle = app.rocket.angle #* (180 / math.pi)
    print(app.rocket.position.x, app.rocket.position.y)
    drawImage(Lander0, app.rocket.position.x, app.rocket.position.y, align = 'center', rotateAngle = angle)

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
                app.runTakeoffInstructions = True
                app.step = 1
                # onSurfaceEngineStart(app)
            elif 300 <= mouseY <= 350:
                setupGame(app)
            elif 400 <= mouseY <= 450:
                app.runLanding = True
                onSurfaceEngineStart(app)
                
            

def mainGameMousePress(app, mouseX, mouseY):
    #skip to "full zoom" or "no zoom

    if not app.zoomedIn:
        app.zoomCounter = 2
        onKeyPress(app, key = 'z')
    else:
        app.zoomCounter = 3
        onKeyPress(app, key = 'z')


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
                generateProjectedPositions(app, 0.005, 380)
    if key == 't':
        app.drawTrails = not app.drawTrails
    if (key == 's' and app.paused == True):
        takeStep(app)
    if key == 'z':
        if app.zoomCounter < 3:
            app.zoomCounter += 1
            if app.zoomCounter == 1:
                app.screen[2] = app.screen[3] = 100
            if app.zoomCounter == 2:
                app.screen[2] = app.screen[3] = 10
            if app.zoomCounter == 3:
                app.screen[2] = app.screen[3] = 2
            app.zoomedIn = True

        elif app.zoomCounter == 3:
            app.zoomCounter = 0
            app.screen[0] = app.width//2
            app.screen[1] = app.height//2
            app.screen[2] = app.width
            app.screen[3] = app.height
            app.zoomedIn = False
    
    app.tracerStep = 30
    app.trailCutoffConstant = 5

    if key == '=': # '+'
        app.dt *= 2
        app.tracerStep //= 2
        app.tracerLength //= 2
        for body in Body.instances:
            body.previousPositions = []
    if key == '-':
        app.dt /= 2
        app.tracerStep *= 2
        app.tracerLength *= 2
        for body in Body.instances:
            body.previousPositions = []
    

    


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
    if not app.zoomedIn:
        if 'w' in keys:
            for body in Body.instances:
                body.position.y += 2
        if 's' in keys:
            for body in Body.instances:
                body.position.y -= 2
        if 'd' in keys:
            for body in Body.instances:
                body.position.x -= 2
        if 'a' in keys:
            for body in Body.instances:
                body.position.x += 2
    # if app.screen[2] == 100:
    #     if 'w' in keys and app.screen[1] > 0:
    #         app.screen[1] -= 2
    #     if 's' in keys and app.screen[1] < app.height:
    #         app.screen[1] += 2
    #     if 'a' in keys and app.screen[0] > 0:
    #         app.screen[0] -= 2
    #     if 'd' in keys and app.screen[0] < app.width:
    #         app.screen[0] += 2
    if 'up' in keys and 'down' not in keys:
        app.rocket.thrustMagnitude += Rocket.maxThrust / 10
    if 'down' in keys and 'up' not in keys:
        app.rocket.thrustMagnitude -= Rocket.maxThrust / 10
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
                if distance(cBody.position.x,cBody.position.y,app.rocket.position.x,app.rocket.position.y) <= cBody.radius:
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
    if app.rocket.altitude > 3300:
        setupGame(app)

def onStep(app):
    app.step += 1
    if not app.paused:
        takeStep(app)

def main():
    app.setMaxShapeCount(10000)
    runApp(width=700, height=700)

main()