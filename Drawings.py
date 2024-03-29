from cmu_graphics import *
from Classes import Rocket, Vector

def drawCSM(app, height, dx, dy, cX=None, cY=None, engineOn=False):
    rocketPosition = Vector(app.rocket.position.x, app.rocket.position.y)
    thrustPercent = app.rocket.thrust / 100
    width = height/4
    if cX==None:
        cX = rocketPosition.x
    if cY ==None:
        cY = rocketPosition.y
    
    drawRect(cX-width/2-dx,cY-(height//6)-dy,width,height/3, fill='silver', border=None)
    drawPolygon(cX+width/2-dx, cY-(height/6)-dy, cX+(width/7)-dx, cY-(height/6)-(height/7)-dy, cX-(width/7)-dx, cY-(height/6)-(height/7)-dy, cX-width/2-dx, cY-(height/6)-dy, fill = 'lightGray' )
    drawArc(cX-dx, cY+(height/6)+(height/8)-dy, width/2, height/4,270,90, fill = 'dimGray')
    drawArc(cX-dx, cY+(height/6)+(height/8)-dy, width/2, height/4,0,90, fill = 'dimGray')
    drawArc(cX-(width/2)+(width/8)+(height/60)-dx, cY+(height/6)-dy, height/30, height/30, 180, 90, fill='saddlebrown')
    drawArc(cX+(width/2)-(width/8)-(height/60)-dx, cY+(height/6)-dy, height/30, height/30, 90, 180, fill='saddlebrown')
    drawRect(cX-(width/2)+(width/8)+(height/60)-dx, cY+(height/6)-dy, 2*((width/2)-(width/5)), height/60, fill='saddlebrown')
    drawPolygon(cX+width/14-dx, cY-(height/6)-(height/7)-dy, cX+width/12-dx, cY-(height/6)-(height/6.5)-dy, cX-dx, cY-(height/6)-(height/5.8)-dy, cX-width/12-dx, cY-(height/6)-(height/6.5)-dy, cX-width/14-dx, cY-(height/6)-(height/7)-dy, fill='grey' )
    drawRect(cX-width/2-dx, cY-height/6.4-dy, width/4, height/22, fill='snow')
    drawRect(cX-width/2 + width/3-dx, cY-height/6.4-dy, width/4, height/22, fill='snow')
    drawRect(cX-width/2 + width/3 + width/3 - dx, cY-height/6.4 - dy, width/4, height/22, fill='snow')
    drawRect(cX-width/2 - dx, cY+height/16 - dy, width, height/16, fill='snow')
    drawRect(cX-width/2+width/12 - dx, cY-height/10-dy, width/3, height/4, fill='darkGrey')

    if engineOn and thrustPercent > 0:
        thrustDecimal = thrustPercent/100
        drawPolygon((cX+width/5)-dx,(cY+height/3.4)-dy,(cX-width/5)-dx,(cY+height/3.4)-dy,cX-dx,(cY+height/3)+ ((height/4)*thrustDecimal)-dy, fill=gradient('white', 'blue', start='top'), opacity = 50)
        drawPolygon((cX+width/6)-dx,(cY+height/3.4)-dy,(cX-width/6)-dx,(cY+height/3.4)-dy,cX-dx,(cY+height/3)+ ((height/12)*thrustDecimal)-dy, fill=gradient('white','royalBlue', start='top'), opacity = 50)
        drawPolygon((cX+width/10)-dx,(cY+height/3.4)-dy,(cX-width/8)-dx,(cY+height/3.4)-dy,cX-dx,(cY+height/3)+ ((height/50)*thrustDecimal)-dy, fill=gradient('white','lightSteelBlue', start='top'), opacity = 80)


def drawLander(app,height, dx, dy):
    rocketPosition = Vector(app.rocket.position.x, app.rocket.position.y)
    drawCSM(app, height, dx=dx, dy=dy, cX=None, cY=None, engineOn=True)
    width = height/4
    cX = rocketPosition.x
    cY = rocketPosition.y
    drawLine(cX-width/2-dx,cY+width/3-dy,cX-width/2-width/2-dx,cY+height/3-dy,lineWidth=4)
    drawLine(cX+width/2-dx,cY+width/3-dy,cX+width/2+width/2-dx,cY+height/3-dy,lineWidth=4)
    
    drawLine(cX-width/2-dx,cY+width/3-dy,cX-width/2-width/3-dx,cY+height/4-dy,lineWidth=6)
    drawLine(cX+width/2-dx,cY+width/3-dy,cX+width/2+width/3-dx,cY+height/4-dy,lineWidth=6)
    drawLine(cX-width/2.5-dx,cY+height/6-dy,cX-width/2-width/3-dx,cY+height/4-dy,lineWidth=4)
    drawLine(cX+width/2.5-dx,cY+height/6-dy,cX+width/2+width/3-dx,cY+height/4-dy,lineWidth=4)

    drawLine(cX-width/2-width/2 - width/8-dx,cY+height/3-dy, cX-width/2-width/2 + width/8-dx,cY+height/3-dy, lineWidth = 6)
    drawLine(cX+width/2+width/2 - width/8-dx,cY+height/3-dy, cX+width/2+width/2 + width/8-dx, cY+height/3-dy, lineWidth = 6)

    drawLine(cX-dx,cY+width/3-dy,cX-dx,cY+height/4-dy, lineWidth=6)
    drawLine(cX-dx,cY+width/3-dy,cX-dx,cY+height/3-dy, lineWidth=3)

    drawLine(cX-width/8-dx,cY+height/3-dy,cX+width/8-dx,cY+height/3-dy, lineWidth=6)

def drawLaunchRocket(app,height, dx, dy, cX=None, cY=None, engineOn=False):
    width = height/18
    if cX==None:
        cX = app.rocket.position.x
    if cY ==None:
        cY = app.rocket.position.y
    #mainFuselage
    drawRect(cX-width/2-dx, cY-height/3-dy, width, height/1.5, fill='snow', border=None)
    CSMWidth = width
    CSMHeight = CSMWidth *4
    drawCSM(app, height=CSMHeight, dx=dx, dy=dy, cX=cX, cY=cY-height/2.5, engineOn=False)
    drawRect(cX-width/2-dx, cY-(height/2.75)-dy, CSMWidth, CSMHeight/4, fill='dimGray')
    drawPolygon(cX-width/2-dx,cY+(height/3)-(width/10)-dy,cX-width/2-dx,cY+(height/3)-height/15-dy,cX-width/2-width/1.6-dx,cY+(height/3)-(width/2)-dy,cX-width/2-width/1.6-dx,cY+(height/3)-(width/10)-dy,fill='darkGray')
    drawPolygon(cX+width/2-dx,cY+(height/3)-(width/10)-dy,cX+width/2-dx,cY+(height/3)-height/15-dy,cX+width/2+width/1.6-dx,cY+(height/3)-(width/2)-dy,cX+width/2+width/1.6-dx,cY+(height/3)-(width/10)-dy,fill='darkGray')
    drawLine(cX-dx,cY+(height/3)-(width/10)-dy,cX-dx,cY+(height/3)-height/15-dy, lineWidth=width/9, fill='darkGray')
    drawLine(cX-width/2.5-dx,cY+(height/2.976)-dy,cX+width/2.5-dx,cY+(height/2.976)-dy,lineWidth=width/25,fill='silver')
    drawArc(cX-width/5-dx, cY+(height/2.81)-dy, width/3.5, width/1.6,270,90, fill = 'dimGray')
    drawArc(cX-width/5-dx, cY+(height/2.81)-dy, width/3.5, width/1.6,0,90, fill = 'dimGray')
    drawArc(cX+width/5-dx, cY+(height/2.81)-dy, width/3.5, width/1.6,270,90, fill = 'dimGray')
    drawArc(cX+width/5-dx, cY+(height/2.81)-dy, width/3.5, width/1.6,0,90, fill = 'dimGray')
    drawRect(cX-width/2-dx,cY+(height/6)-dy, width, width/2, fill='black')
    drawRect(cX-width/2-dx,cY-dy, width, width/3, fill='grey')
    drawRect(cX-width/2-dx,cY-(height/5.5)-dy, width, width*2, fill='grey')
    drawRect(cX-width/2-dx,cY-(height/7)-dy, width, width/2, fill='black')
    drawRect(cX-width/2-dx,cY-(height/4)-dy, width, width*1.2, fill='black')
    drawRect(cX-width/4-dx,cY-height/3-dy, width/20, height/1.6, fill='silver')
    
    if engineOn and app.thrustPercent > 0:
        thrustDecimal = app.thrustPercent/100
        drawPolygon(cX-width/12, cY+(height/2.81),cX-width/12 - width/3.5, cY+(height/2.81), cX-width/12 - width/7,cY+(height/2.81)+width*2.2*(thrustDecimal), fill=gradient('white', 'gold', start='top'), opacity = 80)
        drawPolygon(cX+width/12, cY+(height/2.81),cX+width/12 + width/3.5, cY+(height/2.81), cX+width/12 + width/7,cY+(height/2.81)+width*2.2*(thrustDecimal), fill=gradient('white', 'gold', start='top'), opacity = 80)