class vector:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.mag = (x**2 + y**2)**0.5
        
        def __repr__(self):
            return f'<{self.x},{self.y}>'
        
        def __add__(self, other):
            newX = self.x + other.x
            newY = self.y + other.y
            return vector(newX, newY)
            
        def __sub__(self,other):
            newX = self.x - other.x
            newY = self.y - other.y
            return vector(newX, newY)
        
        def __mul__(self, other):
            if not ( isinstance(other, float) or isinstance(other, int) ):
                raise TypeError('Can only multiply a vector with a scalar')
            elif (isinstance(other, float) or isinstance(other,int)):
                newX = self.x * other
                newY = self.y * other
                return vector(newX, newY)
            
        def __truediv__(self,other):
            if not ( isinstance(other, float) or isinstance(other, int) ):
                raise TypeError('Can only divide a vector with a scalar')
            elif (isinstance(other, float) or isinstance(other,int)):
                return (self * (1 / other))
class body:
        instances = []
        def __init__(self, position, radius, mass, velocity, color):
            self.position = position
            self.previousPositions = []
            self.radius = radius
            self.mass = mass
            self.velocity = velocity
            self.color = color
            self.momentum = self.velocity * self.mass
            body.instances.append(self)
