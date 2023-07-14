from Utils import utils as ut
import math as m 

class Vec2D:
    def __init__(self,x,y,w=0):
        self.x:float = x
        self.y:float = y 
        self.w = w

    def addVec (self, other):
        return Vec2D (self.x + other.x , self.y + other.y)

    def subVec (self, other):
        return Vec2D (self.x - other.x , self.y - other.y )
    
    def __mul__ (self,val):
        return Vec2D(val * self.x ,val * self.y)
    def __rmul__ (self,val):
        return self.__mul__(val)

    def __lmul__(self,val):
        return self.__mul__(val)

    def distance (self, other):
        return m.sqrt( (self.x - other.x)**2 + (self.y- other.y)**2    )

    def magnitude (self):
        return self.distance(Vec2D(0,0,0))

    def __str__(self):
        return ("VEC 2D: "+ "( " + str(self.x) +" , " + str(self.y) +" )" )

    def __sub__(self,other):
        return self.subVec(other)

    def dotProd (self, other):
        return ut.dotProd(ut.numpFast2(self.x,self.y),ut.numpFast2(other.x,other.y))

    def rotateZ_ (self, degrees):
        memx    = self.x
        memy    = self.y
        
        self.x = memx*m.cos(m.degrees(degrees))  - memy*m.sin(m.degrees(degrees))

        self.y = memx*m.sin(m.degrees(degrees))  + memy*m.cos(m.degrees(degrees))

    def rotateY_ (self,degrees):

        m_x    = self.x
        m_z    = self.z
        self.x = m_x*m.cos(m.degrees(degrees))  - m_z*m.sin(m.degrees(degrees))

        self.z = m_x*m.sin(m.degrees(degrees))  + m_z*m.cos(m.degrees(degrees))

    def rotateX_ (self,degrees):

        m_y    = self.y
        m_z    = self.z
        self.y = m_y*m.cos(m.degrees(degrees))  - m_z*m.sin(m.degrees(degrees))

        self.z = m_y*m.sin(m.degrees(degrees))  + m_z*m.cos(m.degrees(degrees))

    def normalizeVec(self):
        return (1/self.magnitude())*self    

    def numpify(self):
        return ut.numpFast2(self.x,self.y)
    
