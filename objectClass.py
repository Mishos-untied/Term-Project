#alright so we should use OOP to base the movement of different objects, we can then make 
#subclasses like rockets and planets
import math

class Object:
    def __init__(self, name, mass, cx, cy, vx, vy):
        self.name = name #include name for the hash function, everything else will change 
        self.mass = mass
        self.cx = cx
        self.cy = cy
        self.vx = vx
        self.vy = vy
    
    def __repr__(self):
        return f'Object named {self.name}'
    
    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other): #considers objects equal if at the same position
        return (isinstance(Object, other)
                and self.cx == other.cx
                and self.cy == other.cy)
    
    def location(self): #this will display the coordinates as a string
        return f'{self.name} is at coordinates(x={self.cx}, y={self.cy})'
    
    def distance(self, other):
        if isinstance(other, Object):
            return ((self.cx - other.cx)**2 + (self.cy - other.cy)**2)**0.5
        return None
    
    def angleBetween(self, other):
        if isinstance(other, Object):
            if self.cx == other.cx:
                return math.pi/2
            return math.atan((other.cy-self.cy) / (other.cx-self.cx))
