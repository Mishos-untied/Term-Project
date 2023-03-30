from objectClass import Object
#let's make constants be global
G = 6.67430 * (10 ** -11)

def gravitation(object1, object2):
    return (G*object1.mass*object2.mass) / object1.distance(object2)

