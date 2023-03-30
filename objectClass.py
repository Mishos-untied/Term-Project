#alright so we should use OOP to base the movement of different objects, we can then make 
#subclasses like rockets and planets

class Object:
    def __init__(self, name, mass, cx, cy, velocity):
        self.name = name#include name for the hash function, everything else will change 
        self.mass = mass
        self.cx = cx
        self.cy = cy
        self.velocity = velocity
    
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
        if isinstance(Object, other):
            return ((self.cx - other.cx)**2 + (self.cy - other.cy)**2)**0.5
        return None
