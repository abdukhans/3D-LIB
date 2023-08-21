from Utils import utils as ut
import math as m 
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
        self.z = self.z +  z

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

        if self.magnitude() == 0:
            return self


        return (1/self.magnitude())*self

    def __str__(self):
        return ("VEC 3D: "+ "( " + str(self.x) +" , " + str(self.y) +" , "+ str(self.z) + " )" )

    def is_equal(self, other: object , epsilon = 0.00001) -> bool:
        return abs(self.x - other.x) < epsilon and abs( self.y - other.y) < epsilon and abs(self.z - other.z) < epsilon
    def numpify(self):
        return ut.numpFast3(self.x,self.y,self.z)


    