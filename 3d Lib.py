from graphics import *
import math as m
import numpy as np
import win32api
import time

global calc
calc = 0 
class Vec3D:
    def __init__(self,x,y,z) :
        self.x = x
        self.y = y
        self.z = z

        self.mem_x = x
        self.mem_y = y 
        self.mem_z = z

    def printVec(self,update=False):
        string = "( "+ str(self.x)+", " +str(self.y)+" , "+str(self.z)+" )"    

        if (not(update)):
            print(string)
        else:
            print(string,end='\r')


    def addVec (self, other):
        return Vec3D (self.x + other.x , self.y + other.y , self.z + other.z )

    def subVec (self, other):
        return Vec3D (self.x - other.x , self.y - other.y , self.z - other.z )

    def distance (self, other):
        return m.sqrt( (self.x - other.x)**2 + (self.y- other.y)**2 + (self.z - other.z)**2     )

    def __str__(self) -> str:
        return "VEC 3D:  (" + str(self.x) +"," + str(self.y)+"," + str(self.z) + ")"

    def magnitude (self):
        return self.distance(Vec3D(0,0,0))


    def dotProd (self, other):
        return (self.x * other.x + self.y*other.y + self.z *other.z)


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
        self.add_x(transVec.x)
        self.add_x(transVec.y)
        self.add_x(transVec.z)
        pass

    def crossProd (self, other):           
        return Vec3D(self.y*other.z - self.z*other.y , - (self.x*other.z - self.z*other.x), self.x*other.y - self.y*other.x)

    def normalizeVec(self):
        return (1/self.magnitude())*self

    






class Tris3D:
    def __init__(self, p1:Vec3D,p2:Vec3D, p3:Vec3D,col="white"):
        self.p1 = p1
        self.p2 = p2 
        self.p3 = p3

        self.norm = (self.p1 - self.p2).crossProd(self.p2 - self.p3).normalizeVec()
        self.col  = col

       
    def getPoints(self) :
        return [self.p1,self.p2,self.p3]

    def setCol (self, color):
        self.col = color

    """
    def drawTri(self,window: GraphWin):
        self.l1.draw(window)
        self.l2.draw(window)
        self.l3.draw(window)
    """
    def midPoi(self):

        return 1/3*(self.p1 + self.p2 + self.p3)
        
    def rotateZ_(self,ang):

        self.p1.rotateZ_(ang)
        self.p2.rotateZ_(ang)
        self.p3.rotateZ_(ang)

        self.norm = (self.p1 - self.p2).crossProd(self.p2 - self.p3).normalizeVec()

        return
    def rotateY_ (self,ang):
        self.p1.rotateY_(ang)
        self.p2.rotateY_(ang)
        self.p3.rotateY_(ang)

        self.norm = self.p1.crossProd(self.p2).normalizeVec()

        return

    def rotateX_(self,ang):
        self.p1.rotateX_(ang)
        self.p2.rotateX_(ang)
        self.p3.rotateX_(ang)


        self.norm = self.p1.crossProd(self.p2).normalizeVec()
        return

    def updateNorm(self):
        
        self.norm = (self.p1 - self.p2).crossProd(self.p2 - self.p3).normalizeVec()

class Mesh:
    def __init__(self, lst3d_tris):
        self.lst3d_tris = lst3d_tris
    
    def move(self,trans_vec):
        pass            

    def updateNorms(self):
        for tris in self.lst3d_tris:
            tris.updateNorm()


"""        
    def draw (self, window: GraphWin):
        self.camera.draw_tris(self.lst3d_tris,window)
        pass

    def unDraw (self):
        self.camera.unDrawTris(self.lst3d_tris)
"""



class Camera:
    def __init__(self, player_head: Vec3D ,mid_vec:Vec3D, norm_vec, b1:Vec3D, b2:Vec3D,  window: GraphWin, height=1 , width=1 ):

        self.mid_poi = mid_vec
        self.norm_vec = norm_vec        

        self.window = window

        self.height = height
        self.wdith = width

        self.player_head = player_head


        # Basis vectors
        self.b1 = b1
        self.b2 = b2 


    def printPlayer(self, update=False):
        print("Player POSITION: ",end = "")

        if(not(update)):
          
            self.player_head.printVec()
        else:
            pass

    def printScreen(self):
        print("Screen POSITION: ",end = "")

        self.mid_poi.printVec()


    def draw_tris (self,lst_tri3D, wireFrame= True, lighting=True):
        for tri in lst_tri3D:
            lst_tri = self.clip(tri)
            for v in  lst_tri:
                if v.norm.dotProd(self.player_head.subVec(v.midPoi())) > 0 :
                    self.draw_tri(v,wireFrame)

    def unDrawTris(self,lst_tri3D):
        for tri in lst_tri3D:
            lst_tri = self.clip(tri)
            for v in  lst_tri:
                if v.norm.dotProd(self.player_head.subVec(v.midPoi())) > 0 :
                    self.unDrawTri(v)
        

    def unDrawTri(self,tri3D:Tris3D):
        
        tri3D.poly.undraw()

        pass
    def draw_tri (self, tri3D:Tris3D, wireFrame=True ):
        lst_points = []
        for vec in tri3D.getPoints():
            lst_points.append(self.calc(vec))

        p1 = lst_points[0]
        p2 = lst_points[1]
        p3 = lst_points[2]
        

        #print (tri3D.p1,tri3D.p2,tri3D.norm)


        """
        tri3D.l1 = Line(p1,p2)
        tri3D.l2 = Line (p2,p3)
        tri3D.l3 = Line(p3,p1)

        tri3D.l1.setFill("white")
        tri3D.l2.setFill("white")
        tri3D.l3.setFill("white")
        """

        tri3D.poly = Polygon(p1, p2, p3,p1)

        if wireFrame:
            tri3D.poly.setOutline(tri3D.col)



        window = self.window
        tri3D.poly.draw(window)
        

    def draw(self, lst_vec3d):

        for i in lst_vec3d:
            print(i)
            porj_point = self.calc(i)
            porj_point.draw(self.window)


        return

    def calc(self, l:Vec3D):

        proj_x = 0 
        proj_y = 0 


        t = l.subVec(self.mid_poi)
        p = self.player_head.subVec(self.mid_poi)
        q = t.subVec(p)
        

        dotProdqn = norm_vec.dotProd(q) 
        dotProdpn = norm_vec.dotProd(p)

        
            
        #s =  -(abs(dotProdnn)**2/ (dotProdqn - abs(dotProdnn)**2))
        
        if dotProdqn == 0 :
            s = 1
        else:
            s =  -(dotProdpn)/(dotProdqn)
        
            
        dotProdbb_1 = self.b1.dotProd(b1)
        dotProdbb_2 = self.b2.dotProd(b2)



        # proj_x = s*(dotProdqb_1)/  dotProdbb_1   
        proj_x =    (p.addVec( s * q).dotProd(self.b1))
        proj_y =    (p.addVec( s * q).dotProd(self.b2))

        #print("S: ",s,end='\r') 

        #print(self.player_head)

        
        return Point(proj_x  , proj_y)
    
    def incrementY (self, incr):
        self.mid_poi.add_y(incr)
        self.player_head.add_y(incr)
    
    def incrementX (self,incr):

        Q  = self.player_head.subVec(self.mid_poi)
        self.mid_poi.add_x(incr)

        self.printPlayer()
        self.player_head.add_x(incr)

        

    def incrementZ(self, incr):


        self.mid_poi.add_z(incr)
        self.player_head.add_z(incr) 


    def drawMesh (self,mesh: Mesh, wireFrame=True ):
        self.draw_tris(mesh.lst3d_tris,wireFrame)

    def undrawMesh (self,mesh:Mesh):

        self.unDrawTris(mesh.lst3d_tris)

    def clip (self, tri : Tris3D):

        #TODO implement clipping

        

        return [tri]

    def rotateZ_(self, angle):


        self.norm_vec.rotateZ_(angle)


        Q = self.mid_poi.subVec(self.player_head)

        Q.rotateZ_(angle)

        self.mid_poi = self.player_head.addVec(Q) 




        self.b1.rotateZ_(angle)
        self.b2.rotateZ_(angle)

        return

    def rotateY_ (self,angle):

        
        self.norm_vec.rotateY_(angle)

        self.player_head = self.mid_poi.addVec(self.norm_vec) 


        self.b1.rotateY_(angle)
        self.b2.rotateY_(angle)

        return  

    def rotateX_ (self,angle):

        
        self.norm_vec.rotateX_(angle)

        self.mid_poi = self.mid_poi.subVec(self.norm_vec) 

        self.b1.rotateX_(angle)
        self.b2.rotateX_(angle)

        return  

    def forward (self,magnitude):
        dir = -1* self.norm_vec
        

        vec = magnitude * dir
        self.player_head = self.player_head.addVec(vec)
        self.mid_poi = self.mid_poi.addVec(vec)


    def backward (self,magnitude):
        dir =  self.norm_vec
        

        vec = magnitude * dir

        self.mid_poi = self.mid_poi.addVec(vec)

        self.player_head = self.player_head.addVec(vec)
    def  left (self,magnitude):
        dir =  -1*self.b1
        

        vec = magnitude * dir

        self.mid_poi = self.mid_poi.addVec(vec)

        self.player_head = self.player_head.addVec(vec)

    def  right (self,magnitude):
        dir =  self.b1
        

        vec = magnitude * dir

        self.mid_poi = self.mid_poi.addVec(vec)

        self.player_head = self.player_head.addVec(vec)






win = GraphWin("Lib", 1000 ,1000,autoflush=False)
win.setBackground("black")
win.setCoords(-3,-3,3,3)




    
    
near = 3
m_z = -3
mid_poi  = Vec3D(0,m_z,0)
player   = Vec3D(0,m_z - near,0)
norm_vec = Vec3D(0,-1,0)
b1       = Vec3D (1,0,0)
b2       = Vec3D (0,0,1)
cam      = Camera( player, mid_poi, norm_vec,b1,b2,win)
v1       = Vec3D(1,1,1) 
v2       = Vec3D(1,1,-1)
v3       = Vec3D(1,-1,-1)
v4       = Vec3D(1,-1,1)
v5       = Vec3D(-1,1,1) 
v6       = Vec3D(-1,1,-1)
v7       = Vec3D(-1,-1,1)
v8       = Vec3D(-1,-1,-1)
lst_vs   = [v1,v2,v3,v4,v5,v6,v7,v8]
tri1     = Tris3D(v1,v3,v2)
tri2     = Tris3D(v1,v4,v3)
tri3     = Tris3D(v8,v7,v5)
tri4     = Tris3D(v8,v5,v6)
tri5     = Tris3D(v8,v3,v4)
tri6     = Tris3D(v8,v4,v7)    
tri7     = Tris3D(v8,v2,v3)
tri8     = Tris3D(v8,v6,v2)
tri9     = Tris3D(v7,v4,v5)
tri10    = Tris3D(v5,v4,v1)
tri11    = Tris3D(v1,v2,v6)
tri12    = Tris3D(v6,v5,v1)
tri13    = Tris3D(v8,v7,v1,col="red")
lst_tris = [tri1,tri2,tri3, tri4,tri5,tri6,tri7,tri8,tri9,tri10,tri11,tri12]
cube     = Mesh(lst_tris)

"""
mesh_cube =[Vec3D(1,1+4,1)    ,Vec3D(1,1+4,-1),
             Vec3D(1,-1+4,-1),  Vec3D(1,-1+4,1),
            Vec3D(-1,1+4,1)   ,Vec3D(-1,1+4,-1),
            Vec3D(-1,-1+4,-1) ,Vec3D(-1,-1+4,1) ]
"""


if __name__ == "__main__":
    i = 0
    step = 0.1
    rot = 0.001
    while(True):
        upArr   = win32api.GetKeyState(0x26)
        downArr = win32api.GetKeyState(0x28)
        righArr = win32api.GetKeyState(0x27)
        leftArr = win32api.GetKeyState(0x25)
        w  = win32api.GetKeyState (0x57)
        s  = win32api.GetKeyState (0x53)
        a  = win32api.GetKeyState(0x41)
        d  = win32api.GetKeyState(0x44)


        if (upArr!=0 and upArr!= 1):
            cam.forward(step)
        if(downArr !=0 and downArr != 1 ):
            cam.backward(step)
        if(righArr !=0 and righArr != 1 ):
            cam.right(step)
            
        if(leftArr !=0 and leftArr != 1 ):
            cam.left(step)
        if(w !=0 and  w != 1 ):
            cam.incrementZ(step)
        if(s !=0 and  s != 1 ):
            cam.incrementZ(-step)  

        if (a != 0 and a != 1):
            cam.rotateZ_(rot)

        if (d != 0 and d != 1):
            cam.rotateZ_(-rot)


        ang = 0.0001
        for vec in lst_vs:

            vec.rotateZ_(ang)

            
            vec.rotateX_(ang)

            #vec.rotateZ_(i*0.0005+0.01)
            vec.rotateY_(ang)


            cube.updateNorms()

        ##cam.draw(mesh_cube,win)
        ##lst_tris = [tri1,tri2,tri3, tri4,tri5,tri6,tri7,tri8,tri9,tri10,tri11,tri12]
        ##cam.draw_tris(lst_tris,win)
        cam.drawMesh(cube)

        #cam.printPlayer()

        update(30)



        cam.undrawMesh(cube)
    print("DONE!!!!!!!!!!!!!!!!!!!")
    win.getMouse()
    win.close