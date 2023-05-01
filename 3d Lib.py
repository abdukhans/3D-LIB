from graphics import *
import math as m
import numpy as np
import win32api
import time

global calc
calc = 0 


class Vec2D:
    def __init__(self,x,y,w=0):
        self.x = x
        self.y = y 
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
        return (self.x * other.x + self.y*other.y )

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
        return Vec3D(self.y*other.z - self.z*other.y , - (self.x*other.z - self.z*other.x), self.x*other.y - self.y*other.x)

    def normalizeVec(self):
        return (1/self.magnitude())*self

    def __str__(self):
        return ("VEC 3D: "+ "( " + str(self.x) +" , " + str(self.y) +" , "+ str(self.z) + " )" )

    def is_equal(self, other: object , epsilon = 0.00001) -> bool:
        return abs(self.x - other.x) < epsilon and abs( self.y - other.y) < epsilon and abs(self.z - other.z) < epsilon
    


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

class Tris2D:
    def __init__(self,p1:Vec2D,p2:Vec2D, p3:Vec2D):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        p_p1   = Point(self.p1.x,self.p1.y)
        p_p2   = Point(self.p2.x,self.p2.y)
        p_p3   = Point(self.p3.x,self.p3.y)
        self.poly = Polygon(p_p1,p_p2,p_p3,p_p1)



    def setFill(self,color):
        self.poly.setFill(color)

    def setOutline(self,color):
        self.poly.setOutline(color)
    def draw_tri (self, win:GraphWin):  
        self.poly.draw(win)
        

    

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

        #self.norm = (self.p1 - self.p2).crossProd(self.p2 - self.p3).normalizeVec()

        return
    def rotateY_ (self,ang):
        self.p1.rotateY_(ang)
        self.p2.rotateY_(ang)
        self.p3.rotateY_(ang)

        #self.norm = self.p1.crossProd(self.p2).normalizeVec()

        return

    def rotateX_(self,ang):
        self.p1.rotateX_(ang)
        self.p2.rotateX_(ang)
        self.p3.rotateX_(ang)


        #self.norm = self.p1.crossProd(self.p2).normalizeVec()

        return

    def updateNorm(self):
        self.norm = (self.p1 - self.p2).crossProd(self.p2 - self.p3).normalizeVec()

    def scale(self,factor):

        self.p1 = factor*self.p1
        self.p3 = factor*self.p2
        self.p3 = factor*self.p3
        self.norm = factor*self.norm

    def move(self, trans_vec):

        self.p1.transVec(trans_vec)
        self.p2.transVec(trans_vec)
        self.p3.transVec(trans_vec)

    def __str__(self):

        return (str(self.p1) +"\n" + str(self.p2) + "\n" + str(self.p3))

class Mesh:
    def __init__(self, lst3d_tris:list[Tris3D]):
        self.lst3d_tris = lst3d_tris

        self.lst_vs:set = set()
        for i in self.lst3d_tris:
            """if i.p1 not in self.lst3d_tris:
                self.lst_vs.add(i.p1)
            if i.p2 not in self.lst3d_tris:
                self.lst_vs.add(i.p2)
            if i.p3 not in self.lst3d_tris:
                self.lst_vs.add(i.p3)"""

            self.lst_vs.add(i.p1)
            self.lst_vs.add(i.p2)
            self.lst_vs.add(i.p3)
        """for i in (self.lst_vs):
            print(i)"""


        #print(len(self.lst_vs))
    def move(self,trans_vec:Vec3D):
        for i in self.lst_vs:
            i.transVec(trans_vec)

    def rotateX_(self,degrees):
        for i in self.lst_vs:
            i.rotateX_(degrees)
        self.updateNorms()

    def rotateY_(self,degrees):
        for i in self.lst_vs:
            i.rotateY_(degrees)
        self.updateNorms()


    def rotateZ_(self,degrees):
        for i in self.lst_vs:
            i.rotateZ_(degrees)
        self.updateNorms()


    def updateNorms(self):
        for tris in self.lst3d_tris:
            tris.updateNorm()

    def scale (self, factor):
        new_lst = set()
        for v in self.lst_vs:
            nv:Vec3D = v*(factor)
            v.set_coords(nv.x,nv.y,nv.z)
    

    def __mul__(self,factor):
        new_mesh = Mesh (self.lst3d_tris)
        return new_mesh.scale(factor)

    def __rmul__(self,factor):
        return self.__mul__(factor)
        

"""        
    def draw (self, window: GraphWin):
        self.camera.draw_tris(self.lst3d_tris,window)
        pass

    def unDraw (self):
        self.camera.unDrawTris(self.lst3d_tris)
"""

def SDistFromLine (line_n:Vec2D, line_p:Vec2D, vec:Vec2D):
    line_n = line_n.normalizeVec()
    return (vec.dotProd(line_n) -  line_p.dotProd(line_n))
    
def ClipAgainstLine(line_n:Vec2D, line_p: Vec2D, lst_tris:list[Tris2D]):
    clipped = []
    for (tri) in lst_tris:
        
        lst_ps = [tri.p1,tri.p2,tri.p3]


        lst_vios = []
        lst_good = []
        
        for p in lst_ps:
            if SDistFromLine(line_n,line_p,p) < 0:
                lst_vios.append(p)
            else:
                lst_good.append(p)
        if len(lst_vios) == 0:
            clipped.append(tri)
        elif len(lst_vios) == 1:
            vio_p =  lst_vios[0]
            gp1   =  lst_good[0]
            gp2   = lst_good[1]

            if gp1.y < gp2.y:
                gp1,gp2= gp2, gp1


            n1_poi  = FindIntersectPoi2D(line_n, line_p,vio_p , gp1 )
            n2_poi  = FindIntersectPoi2D(line_n,line_p,vio_p , gp2 )

            n1_tri  = Tris2D(n1_poi, gp1 , gp2 ) 
            n2_tri  = Tris2D(n1_poi, n2_poi , gp2 ) 

            clipped.append(n1_tri)
            clipped.append(n2_tri)



        elif len(lst_vios) ==2:
            vio_p1 =  lst_vios[0]
            vio_p2 =  lst_vios[1]
            gp     = lst_good[0]
            if vio_p1.y < vio_p2.y:
                vio_p1, vio_p2= vio_p2, vio_p1


            n1_poi  =   FindIntersectPoi2D(line_n,line_p,vio_p1 , gp )
            n2_poi  =   FindIntersectPoi2D(line_n,line_p,vio_p2 , gp )


            n_tri = Tris2D(n1_poi,n2_poi,gp)

            clipped.append(n_tri)

            pass
        elif len(lst_vios) == 3:
            pass

        

    
    return clipped



class Camera:
    def __init__(self, player_head: Vec3D, norm_vec, b1:Vec3D, b2:Vec3D,  window: GraphWin, 
                near=1, far=10,fov=90):
        self.player_head = player_head

        self.zaw   = 0 
        self.pitch = 0 
        self.tan_fov = 1/m.tan(m.radians(fov/2))
        self.q       = far/(far- near)  
        self.near    = near

        self.a = Vec3D(1,0,0)
        self.b = Vec3D(0,1,0)
        self.c = Vec3D(0,0,1)


        self.scale = near


        self.mid_poi = self.player_head + Vec3D(0,near,0)
        print("MID POI: ", self.mid_poi)
        print("Player head: ", self.player_head)
        self.drawn_tri = []
        self.norm_vec = norm_vec        

        self.window = window

        print(window.getWidth())

        self.height = window.getHeight()
        self.wdith = window.getWidth()


    
        


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
        l_d = []
        l_c:list[Tris3D] = []

        l_v  = []

        for tri in lst_tri3D:
            l_v.append(self.viewTri(tri))

        for tri in l_v:
            l_c+= self.clip3D(tri)

        for tri in l_c:
            dot  = tri.norm.dotProd((Vec3D(0,0,0).subVec(tri.midPoi())).normalizeVec())
            #print("NORM: " ,tri.norm," VEC: ",tri.midPoi())
            #dot  = tri.norm.dotProd(self.player_head.subVec(self.mid_poi).normalizeVec())
            if dot >= 0 and lighting :
                light  = tri.norm.dotProd(Vec3D(0,0,0).subVec(Vec3D(0,1,0)).normalizeVec())
                if light <= 0:
                    light = 0.1

                l_d+= self.draw_tri(tri, light,wireFrame)
            elif not (lighting):
                l_d+= self.draw_tri(tri,wireFrame,lighting=False)


      
        for tri in l_d:
            self.drawn_tri.append(tri)
            tri.draw_tri(self.window)

        

    def unDrawTris(self,lighting=True):
        for tri in self.drawn_tri:
            tri.poly.undraw()      

        self.drawn_tri = []  

    def unDrawTri(self,tri3D:Tris3D):
        
        tri3D.poly.undraw()

        pass
    def draw_tri (self, tri3D:Tris3D, light , wireFrame=True,lighting=True ):
        lst_points = []
        for vec in tri3D.getPoints():
            lst_points.append(self.calc(vec))

        v2_p1 = lst_points[0]
        v2_p2 = lst_points[1]
        v2_p3 = lst_points[2]
        

        #print (tri3D.p1,tri3D.p2,tri3D.norm)

        l_c = self.clip2D(Tris2D(v2_p1, v2_p2, v2_p3))



        """
        tri3D.l1 = Line(p1,p2)
        tri3D.l2 = Line (p2,p3)
        tri3D.l3 = Line(p3,p1)

        tri3D.l1.setFill("white")
        tri3D.l2.setFill("white")
        tri3D.l3.setFill("white")
        """

        """p1 = Point (v2_p1.x,v2_p1.y)
        p2 = Point (v2_p2.x,v2_p2.y)
        p3 = Point (v2_p3.x,v2_p3.y)


        tri3D.poly = Polygon(p1, p2, p3,p1)"""

        
        
        if lighting:
            red    = int(light * 255)
            green  = int(light * 255)
            blue   = int(light * 255)
            
            
            for tri_c in l_c:
                tri_c.setFill(color_rgb(red,green,blue))
                tri_c.setOutline(color_rgb(red,green,blue))


            """tri3D.poly.setFill(color_rgb(red,green,blue))
            if not(wireFrame): 
                tri3D.poly.setOutline(color_rgb(red,green,blue))
            """
        if wireFrame:
            for tri_c in l_c:
                tri_c.setOutline("white")





        
        return l_c
        

    def draw(self, lst_vec3d):

        for i in lst_vec3d:
            print(i)
            porj_point = self.calc(i)[0]
            porj_point.draw(self.window)


        return


    def view(self,l:Vec3D):
        mat_view =  np.array([
            [self.a.x                         ,                         self.c.x,                         self.b.x,0],
            [self.a.z                         ,                         self.c.z,                         self.b.z,0],
            [self.a.y                         ,                         self.c.y,                         self.b.y,0],
            [-self.player_head.dotProd(self.a),-self.player_head.dotProd(self.c),-self.player_head.dotProd(self.b),1]
        ])

        vect =np.array( [l.x,l.z,l.y,1])

        vect_view = vect.dot(mat_view)

        #print(vect_view)
        return Vec3D(vect_view[0],vect_view[2],vect_view[1])

    def viewTri(self,tri:Tris3D):
        view_tri =  Tris3D(self.view(tri.p1),self.view(tri.p2),self.view(tri.p3))
        """print("ORIGINAL NORM: ", tri.norm)
        print("VIEW NORM    : ", view_tri.norm) 
        print("____________")"""
        return view_tri


    def calc(self, l:Vec3D):



        mat_proj = np.array([
            [self.tan_fov,            0,                     0,0],
            [   0        ,self.tan_fov,0                      ,0],
            [           0,           0,self.q                 ,1],
            [           0,           0,-self.near* self.q     ,0]
        ])



        """mat_view =  np.array([
            [self.a.x                         ,                         self.c.x,                         self.b.x,0],
            [self.a.z                         ,                         self.c.z,                         self.b.z,0],
            [self.a.y                         ,                         self.c.y,                         self.b.y,0],
            [-self.player_head.dotProd(self.a),-self.player_head.dotProd(self.c),-self.player_head.dotProd(self.b),1]
        ])

        

        vect_view  = vect.dot(mat_view)"""

        vect =np.array( [l.x,l.z,l.y,1])
        vect_proj =(vect).dot(mat_proj)

        l.w = vect_proj[2]

    
        """t = l.subVec(self.mid_poi)
        p = self.player_head.subVec(self.mid_poi)
        q = t.subVec(p)"""
        

        """dotProdqn = norm_vec.dotProd(q) 
        dotProdpn = norm_vec.dotProd(p)"""

    
            
        #s =  -(abs(dotProdnn)**2/ (dotProdqn - abs(dotProdnn)**2))
        
        """if dotProdqn == 0 :
            s = 1
        else:
            s =  -(dotProdpn)/(dotProdqn)
        """
        #s = self.calcS(l)     



        # proj_x = s*(dotProdqb_1)/  dotProdbb_1   
        #proj_x =    (p.addVec( s * q).dotProd(self.b1))
        #proj_y =    (p.addVec( s * q).dotProd(self.b2))

        #print("S: ",s,end='\r') 

        #print(self.player_head)

        #print("y:" ,vect_proj[3])


        vect2d = Vec2D(vect_proj[0]/vect_proj[3] , vect_proj[1]/vect_proj[3],  w=1/vect_proj[3])
        return vect2d
    
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


    def drawMesh (self,mesh: Mesh, wireFrame=True,lighting=True ):
        self.draw_tris(mesh.lst3d_tris,wireFrame,lighting)

    def undrawMesh (self,mesh:Mesh):
        self.unDrawTris()

    def calcS(self, l : Vec3D):


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

        return s 


    def TriPolyPoint(self,poly:Polygon):

        return (poly.points[0],poly.points[1],poly.points[2])
    """ x and y denote the edge we are clipping 
        against """
    def clipTriEdge(self,tri:Polygon , x,y):

        poly_points = self.TriPolyPoint(tri)
        p1_proj = poly_points[0]
        p2_proj = poly_points[1]
        p3_proj = poly_points[2]

        proj_list = [p1_proj,p2_proj,p3_proj]
        if x == -1 :
            violations =  [ p_proj for p_proj in [p1_proj,p2_proj,p3_proj] if p_proj.x < x ]
            val_pois   =  [ i for i in proj_list if i not in violations ]
            if len (violations) == 0: 
                return [tri]
            elif len(violations) == 1:

                vp1 = val_pois[0]
                vp2 = val_pois[1]
                wp3 = violations[0]
                t1  = (wp3.getX() - vp1.getX() , wp3.getY() - vp1.getY() )   
                t2  = (wp3.getX() - vp2.getX() , wp3.getY() - vp2.getY() ) 







                return [tri]
            elif len(violations) == 3:
                return []
        elif x == 1:
            return [tri]
        elif y == -1:
            return [tri]
        elif y == 1:
            return [tri]





        
        raise Exception("The edge you are clipping against does not exist.")


    def clip3D (self, tri : Tris3D):

        #TODO implement clipping
        """tri.updateNorm()
        return [tri]
        """

        #clip against the near plane
        o_norm            = tri.norm
        lst_p:list[Vec3D] =  [(tri.p1,0) ,(tri.p2,1),(tri.p3,2)] 

        plane_p = Vec3D(0,self.near,0)
        #lst_dist = [  i.SDistFromPlane(Vec3D(0,1,0), plane_p) for i in lst_p ]
        lst_vios = []
        lst_good = []

        for p in lst_p: 
            """print("_______________________")
            print("p       : ", p)
            print("self.b  : ", self.b)
            print("plane_p : ",plane_p)
            print("sd      : ",p.SDistFromPlane(self.b,plane_p) )
            print("_______________________")"""
            if p[0].SDistFromPlane(Vec3D(0,1,0),plane_p) < 0 :
                lst_vios.append(p)
            else:
                lst_good.append(p)

        if len(lst_vios) == 1:
            vio_p = lst_vios[0][0]
            idx = lst_vios[0][1]
            """print(vio_p)
            print("VIO 1")"""

            pg1  = lst_good[0][0]
            pg2  = lst_good[1][0]

            pg1_idx = lst_good[0][1]
            pg2_idx = lst_good[1][1]
            if pg1.z < pg2.z:
                pg1,pg2 = pg2,pg1
                pg1_idx,pg2_idx= pg2_idx,pg1_idx
            n_poi1 = FindIntersectPoi(Vec3D(0,1,0), plane_p,vio_p, pg1)
            n_poi2 = FindIntersectPoi(Vec3D(0,1,0), plane_p,vio_p, pg2)

            """if n_poi1.is_equal(n_poi2):
                print("EQULAI")"""
            """if n_poi1.z < n_poi2.z:
                n_poi1,n_poi2 = n_poi2, n_poi1"""


            """print(n_poi1)
            print(n_poi2)
            print("_____")    """

           
            

            n_tri1 = Tris3D(n_poi1, pg1 ,pg2)

            n_tri2 = Tris3D( n_poi1, n_poi2 ,pg2)

            #n_tri1.col = "red"
            if not(n_tri1.norm.is_equal(o_norm,epsilon=0.01)):
                """print("NO 1")
                print(n_tri1.norm) """
            
                n_tri1 = Tris3D(pg1, n_poi1 ,pg2)
                #n_tri1.col = "purple"
                #print(n_tri1.norm)
                
            #n_tri2.col = "green"
            if not(n_tri2.norm.is_equal(o_norm,epsilon=0.01)): 
                #print("NO 2") 
                n_tri2 = Tris3D(n_poi2, n_poi1 ,pg2)
                #n_tri2.col = "purple"
            
                pass
            #print("O NORM: " , o_norm)

                
            
            
            return [n_tri1,n_tri2]
        elif len(lst_vios) == 2:
            vio_p1 = lst_vios[0][0]
            vio_p2 = lst_vios[1][0]

            n_poi1 = FindIntersectPoi(Vec3D(0,1,0), plane_p,vio_p1, lst_good[0][0])
            n_poi2 = FindIntersectPoi(Vec3D(0,1,0), plane_p,vio_p2, lst_good[0][0])

            n_tri = Tris3D(n_poi1,n_poi2, lst_good [0][0])

            if not(n_tri.norm.is_equal(o_norm,epsilon=0.01)):
                n_tri = Tris3D(n_poi2,n_poi1, lst_good[0][0])


            
            #n_tri.col = "blue"
            return [n_tri]  
        elif len(lst_vios) == 3:
            return []
        #print(self.player_head.subVec(self.mid_poi).magnitude())
        tri.updateNorm()
        return [tri]

        clip_tri_x_neg = []
        clip_tri_x_neg +=  self.clipTriEdge(tri.poly, -1,0)
      
        clip_tri_x_pos = []
        for tri_ in clip_tri_x_neg:
            clip_tri_x_pos += self.clipTriEdge(tri_, 1,0 )
        
    

        clip_tri_y_neg = []
        for tri_ in clip_tri_x_pos:
            clip_tri_y_neg += self.clipTriEdge(tri_, 0,-1 )


        clip_tri_y_pos = []
        for tri_ in clip_tri_y_neg:
            clip_tri_y_pos += self.clipTriEdge(tri_, 0,1 )
    
        return tri


    def clip2D(self, tri:Tris2D):
        #clip aginst x =  - 1

        """lst_ps = [tri.p1,tri.p2,tri.p3]

        lst_vios_y_neg = []
        lst_good_y_neg = []

        for i in lst_ps:
            if i.y < -1 :
                lst_vios_y_neg.append(i)
            else:
                lst_good_y_neg.append(i)


        lst_p2 = []
        if len(lst_vios_y_neg) == 1:
            vio_p =  lst_vios_y_neg[0]
            gp1   =  lst_good_y_neg[0]
            gp2   = lst_good_y_neg[1]

            if gp1.y < gp2.y:
                gp1.y,gp2.y= gp2.y, gp1.y


            n1_poi  = FindIntersectPoi2D(Vec2D(0,-1),Vec2D(-1,0),vio_p , gp1 )
            n2_poi  = FindIntersectPoi2D(Vec2D(0,-1),Vec2D(-1,0),vio_p , gp2 )

            n1_tri  = Tris2D(n1_poi, gp1 , gp2 ) 
            n2_tri  = Tris2D(n1_poi, n2_poi , gp2 ) 

            lst_p2.append(n1_tri)
            lst_p2.append(n2_tri)



        elif len(lst_vios_y_neg) ==2:
            vio_p1 =  lst_vios_y_neg[0]
            vio_p2 =  lst_vios_y_neg[1]
            gp     = lst_good_y_neg[0]
            if vio_p1.y < vio_p2:
                vio_p1.y , vio_p2= vio_p2.y , vio_p1


            n1_poi  =   FindIntersectPoi2D(Vec2D(0,-1),Vec2D(-1,0),vio_p1 , gp )
            n2_poi  =   FindIntersectPoi2D(Vec2D(0,-1),Vec2D(-1,0),vio_p2 , gp )


            n_tri = Tris2D(n1_poi,n2_poi,gp)

            lst_p2.append(n_tri)

            pass
        elif len(lst_vios_y_neg) == 3:
            return []"""


        #ClipAgainstLine(line_n:Vec2D, line_p: Vec2D, lst_tris:list[Tris2D])

        lst_tri = [tri]

        x_neg = ClipAgainstLine(Vec2D(1,0),Vec2D(-1,0),lst_tri)
        y_pos = ClipAgainstLine(Vec2D(0,-1),Vec2D(0,1),x_neg)
        x_pos = ClipAgainstLine(Vec2D(-1,0),Vec2D(1,0),y_pos)
        y_neg = ClipAgainstLine(Vec2D(0,1),Vec2D(0,-1),x_pos)







            



        return y_neg

    def clipTris(self, lst_tris):

        clipped = []

        for tri in lst_tris:
            lst_clip = self.clip(tri)

            for cli_tri in lst_clip:
                clipped.append(cli_tri)

        return clipped

    def rotateZ_(self, angle):



        self.a.rotateZ_(angle)
        self.b.rotateZ_(angle)
        self.c.rotateZ_(angle)


        self.norm_vec.rotateZ_(angle)


        Q = self.mid_poi.subVec(self.player_head)

        Q.rotateZ_(angle)

        self.mid_poi = self.player_head.addVec(Q) 

        self.zaw  += angle 



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
        dir = self.b
        
        vec = magnitude * dir
        self.player_head = self.player_head.addVec(vec)
        self.mid_poi = self.mid_poi.addVec(vec)


    def backward (self,magnitude):
        dir =  -1 * self.b
        

        vec = magnitude * dir

        self.mid_poi = self.mid_poi.addVec(vec)

        self.player_head = self.player_head.addVec(vec)
    def  left (self,magnitude):
        dir =  -1*self.a
        

        vec = magnitude * dir

        self.mid_poi = self.mid_poi.addVec(vec)

        self.player_head = self.player_head.addVec(vec)

    def  right (self,magnitude):
        dir =  self.a
        

        vec = magnitude * dir

        self.mid_poi = self.mid_poi.addVec(vec)

        self.player_head = self.player_head.addVec(vec)






height = 500
width  = 500 
win    = GraphWin("Lib", height=height ,width= width,autoflush=False)
win.setBackground("black")
win.setCoords(-1,-1,1,1)



"""
for i in range (500):
    p = Point(i/(85),1)
    p.setFill("Red")
    p.draw(win)
"""
near = 1
m_z = -3

p = -4
player   = Vec3D(0,p,0)
norm_vec = Vec3D(0,-1,0)
b1       = Vec3D(1,0,0)
b2       = Vec3D(0,0,1)
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
lst_tris = [tri6]
cube     = Mesh(lst_tris)



cube.move(Vec3D(0,0,0))
#cube.rotateY_(0.005969999999999925)
cam      = Camera(player,norm_vec,b1,b2,win,near=1,fov=90)


"""
mesh_cube =[Vec3D(1,1+4,1)    ,Vec3D(1,1+4,-1),
             Vec3D(1,-1+4,-1),  Vec3D(1,-1+4,1),
            Vec3D(-1,1+4,1)   ,Vec3D(-1,1+4,-1),
            Vec3D(-1,-1+4,-1) ,Vec3D(-1,-1+4,1) ]
"""

if __name__ == "__main__":
    i = 0
    step = 0.1/1.3
    rot = 0.001
    
    print(Vec3D(-1,-1,1).SDistFromPlane(Vec3D(0,1,0),Vec3D(0,-3,0)))
    while(True):
        upArr   = win32api.GetKeyState(0x26)
        downArr = win32api.GetKeyState(0x28)
        righArr = win32api.GetKeyState(0x27)
        leftArr = win32api.GetKeyState(0x25)
        w       = win32api.GetKeyState(0x57)
        s       = win32api.GetKeyState(0x53)
        a       = win32api.GetKeyState(0x41)
        d       = win32api.GetKeyState(0x44)


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

        x,y,z = -1,1,3
        ang = 0.0001
        i += ang

        cube.rotateX_(0*ang)
        cube.rotateZ_(0*ang)
        cube.rotateY_(ang)
        
       
        
        """for vec in lst_vs:
            pass
            
            #vec.rotateZ_(ang)

            
            #vec.rotateX_(ang)

            #vec.rotateZ_(i*0.0005+0.01)
            #vec.rotateY_(ang)


            #cube.updateNorms()"""

        ##cam.draw(mesh_cube,win)
        ##lst_tris = [tri1,tri2,tri3, tri4,tri5,tri6,tri7,tri8,tri9,tri10,tri11,tri12]
        ##cam.draw_tris(lst_tris,win)
        cube.move(Vec3D(x,y,z))
        cam.drawMesh(cube,wireFrame=True,lighting=False)
        cube.move(Vec3D(-x,-y,-z))

        #cam.printPlayer()

        update(30)

       

       
        cam.undrawMesh(cube)
    print("DONE!!!!!!!!!!!!!!!!!!!")
    win.getMouse()
    win.close