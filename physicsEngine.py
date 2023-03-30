from objectClass import Object
import time
#let's make constants be global
G = 6.67430 * (10 ** -11)
littleG = 9.80665
earthMass = 5.972 * 10**(24)
earthRadius = 6378.1*10**3

def almostEqual(x, y):
    return abs(x-y) < 0.1

def gravitation(object1, object2):
    return (G*object1.mass*object2.mass) / (object1.distance(object2)**2)

earth = Object("earth", earthMass, 0, 0, 0, 0)
box = Object("box", 1, earthRadius, 0, 0, 0)

def testGravitation(): #fault tolerance for gravity function
    print("at earth's surface - low mass")
    avgForce = 0
    avgAcceleration = 0
    t1 = time.time()
    for i in range(1, 1000):
        gravity = gravitation(box, earth)
        avgForce += abs(gravity - littleG*box.mass)
        avgAcceleration += abs(gravity - littleG*box.mass) / box.mass
        box.mass += 1
    t2 = time.time()
    print(f"ran in {t2-t1} seconds")
    avgForce /= 999
    print(f"average offset of {avgForce} N")
    avgAcceleration /= 999
    print(f'average Acceleration offset of {avgAcceleration}')
    box.mass = 0
    print('---------------')
    print("testing at earth's surface, high mass")
    avgForce = 0
    avgAcceleration
    t1 = time.time()
    for i in range(1, 1000):
        box.mass += 50
        gravity = gravitation(box, earth)
        avgForce += abs(gravity - littleG*box.mass)
        avgAcceleration += abs(gravity - littleG*box.mass) / box.mass
    t2 = time.time()
    print(f"ran in {t2-t1} seconds")
    avgForce /= 999
    print(f'avg offset of {avgForce} N')
    avgAcceleration /= 999
    print(f'average Acceleration offset of {avgAcceleration} m/s^2')
    
testGravitation()
    
