from objectClass import Object
import time
import math
#let's make constants be global
G = 6.67430 * (10 ** -11)
littleG = 9.80665
earthMass = 5.972 * 10**(24)
earthRadius = 6378.1*10**3

earth = Object("earth", earthMass, 0, 0, 0, 0)

box = Object("box", 1, earthRadius, 0, 0, 0)

def almostEqual(x, y):
    return abs(x-y) < 0.1

############
###Forces###
############


def gravitation(object1, object2):
    return (G*object1.mass*object2.mass) / (object1.distance(object2)**2)


items = [earth, box]
forceFunctions = [gravitation]
# apparently you can store functions in list, so these abuse this fact to sum the forces in the x and y
# directions. Only caveat is the the function has to be defined in a line above the list

def findXForces(o): 
    total = 0
    for fun in forceFunctions:
        for obj in items:
            if obj != o:
                total += math.cos(o.angleBetween(obj)) * fun(o, obj)
    return total

def findYForces(o):
    total = 0
    for fun in forceFunctions:
        for obj in items:
            if obj != 0:
                total += math.sin(o.angleBetween(obj)) * fun(o, obj)





############
###Motion###
############

def updateXPos(ob):
    acceleration = findXForces(ob) / ob.mass
    ob.cx = ob.vx + 0.5 * acceleration

def updateYPos(ob):
    acceleration = findYForces(ob) / ob.mass
    ob.cy = ob.vy + 0.5 * acceleration

def updateObject(ob):
    updateXPos(ob)
    updateYPos(ob)


