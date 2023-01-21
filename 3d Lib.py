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


class Tris3D:
    def __init__(self, p1:Vec3D,p2:Vec3D, p3:Vec3D):
        self.p1 = p1
        self.p2 = p2 
        self.p3 = p3
       
    def getPoints(self) :
        return [self.p1,self.p2,self.p3]

    def drawTri(self,window: GraphWin):
        self.l1.draw(window)
        self.l2.draw(window)
        self.l3.draw(window)

        


class Camera:
    def __init__(self, mid_vec:Vec3D, norm_vec, b1:Vec3D, b2:Vec3D, height=1 , width=1 ):

        self.mid_poi = mid_vec
        self.norm_vec = norm_vec

        self.height = height
        self.wdith = width

        self.player_head = mid_vec.addVec(norm_vec)


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


    def draw_tris (self,lst_tri3D, window: GraphWin):
        for tri in lst_tri3D:
            self.draw_tri(tri,window)


    def unDrawTris(self,lst_tri3D):

        for tri in lst_tri3D:
            self.unDrawTri(tri) 
        

    def unDrawTri(self,tri3D):
        
        tri3D.l1.undraw()
        tri3D.l2.undraw()
        tri3D.l3.undraw()


        pass
    def draw_tri (self, tri3D, window: GraphWin ):
        lst_points = []
        for vec in tri3D.getPoints():
            #TODO implement clipping
            lst_points.append(self.calc(vec))

        p1 = lst_points[0]
        p2 = lst_points[1]
        p3 = lst_points[2]

        tri3D.l1 = Line(p1,p2)
        tri3D.l2 = Line (p2,p3)
        tri3D.l3 = Line(p3,p1)

        tri3D.l1.draw(window)
        tri3D.l2.draw(window)
        tri3D.l3.draw(window)   



        
        

    def draw(self, lst_vec3d, window):

        for i in lst_vec3d:
            print(i)
            porj_point = self.calc(i)
            porj_point.draw(window)


        return

    def calc(self, l:Vec3D):

        proj_x =  0 

        proj_y = 0 
        
        q = l.subVec(self.player_head)


        dotProdqn = norm_vec.dotProd(q) 
        dotProdnn = norm_vec.dotProd(norm_vec) 

        if(dotProdqn != dotProdnn):
            
            s =  -(abs(dotProdnn)**2/ (dotProdqn - abs(dotProdnn)**2))
            pass
        else:
            #print("EXception")
            if(s > 1):
                print("S:",s,end='r')

          


        dotProdqb_1 =q.dotProd(self.b1) 
        dotProdqb_2 = q.dotProd(self.b2)

        dotProdbb_1 = self.b1.dotProd(b1)
        dotProdbb_2 = self.b2.dotProd(b2)

        proj_x = s*(dotProdqb_1)/  dotProdbb_1        

        proj_y = s*(dotProdqb_2)/(dotProdbb_2)   

        print("S: ",s,end='\r') 
        print(self.player_head)
        if(0<= s <= 1):
            
            #print(Point(proj_x , proj_y))
            
            return Point(proj_x , proj_y)
        else:

         

            return Point(proj_x  , proj_y)
    def incrementY (self, incr):
        self.mid_poi.add_y(incr)
        self.player_head.add_y(incr)

    def incrementX (self,incr):
        self.mid_poi.add_x(incr)
        self.player_head.add_x(incr)

    def incrementZ(self, incr):
        self.mid_poi.add_z(incr)
        self.player_head.add_z(incr)


class Mesh:
    def __init__(self, lst3d_tris, cam: Camera):
        self.lst3d_tris = lst3d_tris
        self.camera = cam
    
    def move(self,trans_vec):
        pass

    def draw (self, window: GraphWin):
        self.camera.draw_tris(self.lst3d_tris,window)
        pass

    def unDraw (self):
        self.camera.unDrawTris(self.lst3d_tris)





    
mid_poi  = Vec3D(0,-3,0)
norm_vec = Vec3D(0,-1,0)
b1       = Vec3D (1,0,0)
b2       = Vec3D (0,0,1)
cam      = Camera(mid_poi, norm_vec,b1,b2)
v1       = Vec3D(1,1,1) 
v2       = Vec3D(1,1,-1)
v3       = Vec3D(1,-1,-1)
v4       = Vec3D(1,-1,1)
v5       = Vec3D(-1,1,1) 
v6       = Vec3D(-1,1,-1)
v7       = Vec3D(-1,-1,1)
v8       = Vec3D(-1,-1,-1)
lst_vs   = [v1,v2,v3,v4,v5,v6,v7,v8]
tri1     = Tris3D(v1,v2,v3)
tri2     = Tris3D(v3,v4,v1)
tri3     = Tris3D(v8,v7,v5)
tri4     = Tris3D(v8,v5,v6)
tri5     = Tris3D(v8,v3,v4)
tri6     = Tris3D(v7,v8,v4)
tri7     = Tris3D(v8,v3,v2)
tri8     = Tris3D(v8,v2,v6)
tri9     = Tris3D(v7,v4,v5)
tri10    = Tris3D(v5,v4,v1)
tri11    = Tris3D(v1,v2,v6)
tri12    = Tris3D(v6,v1,v5)
tri13    = Tris3D(v8,v7,v1)
lst_tris = [tri1,tri2,tri3, tri4,tri5,tri6,tri7,tri8,tri9,tri10,tri11,tri12,tri13]
cube     = Mesh(lst_tris,cam)

"""
mesh_cube =[Vec3D(1,1+4,1)    ,Vec3D(1,1+4,-1),
             Vec3D(1,-1+4,-1),  Vec3D(1,-1+4,1),
            Vec3D(-1,1+4,1)   ,Vec3D(-1,1+4,-1),
            Vec3D(-1,-1+4,-1) ,Vec3D(-1,-1+4,1) ]
"""

win = GraphWin("Lib", 1000 ,1000,autoflush=False)
win.setBackground("white")
win.setCoords(-3,-3,3,3)
i = 0
step = 0.1
while(True):
    upArr = win32api.GetKeyState(0x26)
    downArr = win32api.GetKeyState(0x28)
    righArr = win32api.GetKeyState(0x27)
    leftArr = win32api.GetKeyState(0x25)
    w  = win32api.GetKeyState (0x57)
    s  = win32api.GetKeyState (0x53)
    if (upArr!=0 and upArr!= 1):
        cube.camera.incrementY(step)
    if(downArr !=0 and downArr != 1 ):
        cube.camera.incrementY(-step)
    if(righArr !=0 and righArr != 1 ):
        cube.camera.incrementX(step)
    if(leftArr !=0 and leftArr != 1 ):
        cube.camera.incrementX(-step)
    if(w !=0 and  w != 1 ):
        cube.camera.incrementZ(step)
    if(s !=0 and  s != 1 ):
        cube.camera.incrementZ(-step)   

    ang = 0.00005 
    for vec in lst_vs:

        vec.rotateZ_(ang)
        vec.rotateX_(ang)

        #vec.rotateZ_(i*0.0005+0.01)
        vec.rotateY_(ang)
    i += 1 
    ##cam.draw(mesh_cube,win)
    ##lst_tris = [tri1,tri2,tri3, tri4,tri5,tri6,tri7,tri8,tri9,tri10,tri11,tri12]
    ##cam.draw_tris(lst_tris,win)
    cube.draw(win)

    update(30)

    cube.unDraw()
print("DONE!!!!!!!!!!!!!!!!!!!")
win.getMouse()
win.close()

