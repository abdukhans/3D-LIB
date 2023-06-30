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
    

class Vec3D:
    def __init__(self,x,y,z) :
        self.x = x
        self.y = y
        self.z = z
        self.w = 1

        """self.mem_x = x
        self.mem_y = y 
        self.mem_z = z"""

    def printVec(self,update=False):
        string = "( "+ str(self.x)+", " +str(self.y)+" , "+str(self.z)+" )"    

        if (not(update)):
            print(string)
        else:
            print(string,end='\r')
    def set_coords(self,x,y,z):
        self.x = x
        self.y = y 

        self.z = z 


    def addVec (self, other):
        return Vec3D (self.x + other.x , self.y + other.y , self.z + other.z )

    def subVec (self, other):
        return Vec3D (self.x - other.x , self.y - other.y , self.z - other.z )

    def distance (self, other):
        return m.sqrt( (self.x - other.x)**2 + (self.y- other.y)**2 + (self.z - other.z)**2     )
    


    def magnitude (self):
        return self.distance(Vec3D(0,0,0))


    def dotProd (self, other):
        return ut.dotProd(ut.numpFast3(self.x,self.y,self.z),ut.numpFast3(other.x,other.y,other.z))


    def __mul__ (self,val):
        return Vec3D(val * self.x ,val * self.y, val * self.z)
    def __rmul__ (self,val):
        return self.__mul__(val)

    def __lmul__(self,val):
        return self.__mul__(val)

    def __add__ (self, other):
        return self.addVec(other)

    def __sub__(self,other):

        return self.subVec(other)
    def rotateZ_ (self, degrees):
        

        memx    = self.x
        memy    = self.y
        
        self.x = memx*m.cos(m.degrees(degrees))  - memy*m.sin(m.degrees(degrees))

        self.y = memx*m.sin(m.degrees(degrees))  + memy*m.cos(m.degrees(degrees))

        pass

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

    def add_z (self, z):
        self.z += z

    def add_y (self,y):
        self.y += y

    def add_x (self,x):
        self.x+= x

    def transVec (self,transVec):
        #print("BEFORE: " , self)
        self.add_x(transVec.x)
        self.add_y(transVec.y)
        self.add_z(transVec.z)
        #print("AFTER : " , self)

        pass

    """
        This returns the signed distance from a plan defined by
        a normal as well as a point on the plane
    """
    def SDistFromPlane(self,plane_n , point_plane):
        plane_norm = plane_n.normalizeVec()
        return (self.dotProd(plane_norm) -  point_plane.dotProd(plane_norm))

    def crossProd (self, other):           
        return Vec3D(
            self.y*other.z - self.z*other.y , 
        - ( self.x*other.z - self.z*other.x),
            self.x*other.y - self.y*other.x)

    def normalizeVec(self):
        return (1/self.magnitude())*self

    def __str__(self):
        return ("VEC 3D: "+ "( " + str(self.x) +" , " + str(self.y) +" , "+ str(self.z) + " )" )

    def is_equal(self, other: object , epsilon = 0.00001) -> bool:
        return abs(self.x - other.x) < epsilon and abs( self.y - other.y) < epsilon and abs(self.z - other.z) < epsilon
    def numpify(self):
        return ut.numpFast3(self.x,self.y,self.z)


def FindIntersectPoi(plane_n:Vec3D, plane_p:Vec3D,line_start:Vec3D, line_end:Vec3D):

    plane_n = plane_n.normalizeVec()
    plane_d = -plane_n.dotProd(plane_p)
    ad      = line_start.dotProd(plane_n)
    bd      = line_end.dotProd(plane_n)
    t = (-plane_d - ad) / (bd - ad)
    
    lineStartToEnd = line_end.subVec(line_start)
    lineToIntersect = t*lineStartToEnd
    return line_start.addVec(lineToIntersect)

def FindIntersectPoi2D(line_n:Vec2D, line_p:Vec2D,line_start:Vec2D, line_end:Vec3D):
    line_n = line_n.normalizeVec()
    line_d = -line_n.dotProd(line_p)
    ad      = line_start.dotProd(line_n)
    bd      = line_end.dotProd(line_n)
    t = (-line_d - ad) / (bd - ad)
    
    lineStartToEnd = line_end.subVec(line_start)
    lineToIntersect = t*lineStartToEnd
    return line_start.addVec(lineToIntersect)
    



def isNumBetween(start,end,num):

    if start <= num and num <= end:
        return True
    elif end <= num and num <= start:
        return True
    return False


"""def Clip2DLine (lc_p1:Vec2D , lc_p2:Vec2D, lp_p1:Vec2D, lp_p2:Vec2D ):

    m1 =(lc_p1.y - lc_p2.y )/(lc_p1.x - lc_p2.x )
    m2 =(lp_p2.y - lc_p2.y )/(lp_p1.x - lp_p1.x )

    
    b1 = lc_p1.y   -(lc_p1.x)*m1
    b2 = lp_p1.y   -(lp_p1.x)*m2



    x_bar = (b1 - b2) / (m1 - m2 )


    if isNumBetween(lc_p1.x, lc_p1.x, x_bar) and isNumBetween(lp_p1.x, lp_p1.x, x_bar):
        pass
    else:



    pass
"""