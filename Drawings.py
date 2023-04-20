from cmu_graphics import *
from Classes import Rocket, Vector

def drawCSM(app, height, cX=None, cY=None, engineOn=False, angle = 0):
    rocketPosition = Vector(app.rocket.position.x, app.rocket.position.y)
    thrustPercent = app.rocket.thrust / 100
    width = height/4
    if cX==None:
        cX = rocketPosition.x
    if cY ==None:
        cY = rocketPosition.y
    
    drawRect(cX-width/2,cY-(height//6),width,height/3, fill='silver', border=None)
    drawPolygon(cX+width/2, cY-(height/6), cX+(width/7), cY-(height/6)-(height/7), cX-(width/7), cY-(height/6)-(height/7), cX-width/2, cY-(height/6), fill = 'lightGray' )
    drawArc(cX, cY+(height/6)+(height/8), width/2, height/4,270,90, fill = 'dimGray')
    drawArc(cX, cY+(height/6)+(height/8), width/2, height/4,0,90, fill = 'dimGray')
    drawArc(cX-(width/2)+(width/8)+(height/60), cY+(height/6), height/30, height/30, 180, 90, fill='saddlebrown')
    drawArc(cX+(width/2)-(width/8)-(height/60), cY+(height/6), height/30, height/30, 90, 180, fill='saddlebrown')
    drawRect(cX-(width/2)+(width/8)+(height/60), cY+(height/6), 2*((width/2)-(width/5)), height/60, fill='saddlebrown')
    drawPolygon(cX+width/14, cY-(height/6)-(height/7), cX+width/12, cY-(height/6)-(height/6.5), cX, cY-(height/6)-(height/5.8), cX-width/12, cY-(height/6)-(height/6.5), cX-width/14, cY-(height/6)-(height/7), fill='grey' )
    drawRect(cX-width/2, cY-height/6.4, width/4, height/22, fill='snow')
    drawRect(cX-width/2 + width/3, cY-height/6.4, width/4, height/22, fill='snow')
    drawRect(cX-width/2 + width/3 + width/3, cY-height/6.4, width/4, height/22, fill='snow')
    drawRect(cX-width/2, cY+height/16, width, height/16, fill='snow')
    drawRect(cX-width/2+width/12, cY-height/10, width/3, height/4, fill='darkGrey')

    if engineOn and thrustPercent > 0:
        thrustDecimal = thrustPercent/100
        drawPolygon((cX+width/5),(cY+height/3.4),(cX-width/5),(cY+height/3.4),cX,(cY+height/3)+ ((height/4)*thrustDecimal), fill=gradient('white', 'blue', start='top'), opacity = 50)
        drawPolygon((cX+width/6),(cY+height/3.4),(cX-width/6),(cY+height/3.4),cX,(cY+height/3)+ ((height/12)*thrustDecimal), fill=gradient('white','royalBlue', start='top'), opacity = 50)
        drawPolygon((cX+width/10),(cY+height/3.4),(cX-width/8),(cY+height/3.4),cX,(cY+height/3)+ ((height/50)*thrustDecimal), fill=gradient('white','lightSteelBlue', start='top'), opacity = 80)


def drawLander(app,height):
    rocketPosition = Vector(app.rocket.position.x, app.rocket.position.y)
    drawCSM(app, height, cX=None, cY=None, engineOn=True)
    width = height/4
    cX = rocketPosition.x
    cY = rocketPosition.y
    drawLine(cX-width/2,cY+width/3,cX-width/2-width/2,cY+height/3,lineWidth=4)
    drawLine(cX+width/2,cY+width/3,cX+width/2+width/2,cY+height/3,lineWidth=4)
    
    drawLine(cX-width/2,cY+width/3,cX-width/2-width/3,cY+height/4,lineWidth=6)
    drawLine(cX+width/2,cY+width/3,cX+width/2+width/3 ,cY+height/4,lineWidth=6)
    drawLine(cX-width/2.5,cY+height/6,cX-width/2-width/3,cY+height/4,lineWidth=4)
    drawLine(cX+width/2.5,cY+height/6,cX+width/2+width/3 ,cY+height/4,lineWidth=4)

    drawLine(cX-width/2-width/2 - width/8,cY+height/3, cX-width/2-width/2 + width/8,cY+height/3, lineWidth = 6)
    drawLine(cX+width/2+width/2 - width/8,cY+height/3, cX+width/2+width/2 + width/8, cY+height/3, lineWidth = 6)

    drawLine(cX,cY+width/3,cX,cY+height/4, lineWidth=6)
    drawLine(cX,cY+width/3,cX,cY+height/3, lineWidth=3)

    drawLine(cX-width/8,cY+height/3,cX+width/8,cY+height/3, lineWidth=6)