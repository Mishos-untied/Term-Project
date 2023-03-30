from objectClass import Object
#let's make constants be global
G = 6.67430 * (10 ** -11)
earthMass = 5.972 * 10**(24)
earthRadius = 6378.1*10**3

def almostEqual(x, y):
    return abs(x-y) < 0.1

def gravitation(object1, object2):
    return (G*object1.mass*object2.mass) / (object1.distance(object2)**2)

earth = Object("earth", earthMass, 0, 0, 0, 0)
box = Object("box", 1, earthRadius, 0, 0, 0)

assert(almostEqual(gravitation(earth, box), 9.8))