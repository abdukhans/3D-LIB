from Vec3D import Vec3D
from Vec2D import Vec2D
from Tri3D import Tris3D
from Tri2D import Tris2D
from Mesh import Mesh
from graphics import *
import numpy as np
from Utils import utils as ut
import math as m 
import PipeLine2D3D as p2D3D
import sys 

from PygameRender import  DrawTris,clear 

argc = len(sys.argv)
parse_2d_tris =  True if 'p2' in sys.argv else False
parse_3d_tris = True if 'p3' in sys.argv else False


if parse_2d_tris:
    list_2d_numpy_AC   = np.zeros(6320*6,dtype=np.float64)
    numpy_num_tris_AC  = 0 

    list_2d_numpy_BC   = np.zeros(6320*6,dtype=np.float64)
    numpy_num_tris_BC  = 0

if parse_3d_tris:
    list_3d_numpy_BC   = np.zeros(6320*9,dtype=np.float64)
    numpy_num_tris_3BC = 0

    list_3d_numpy_VC   = np.zeros(6320*9,dtype=np.float64)
    numpy_num_tris_3VC = 0

    list_3d_numpy_AC   = np.zeros(6320*9,dtype=np.float64)
    numpy_num_tris_3AC = 0 




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







def SDistFromLine (line_n:np.ndarray , line_p:np.ndarray, vec:np.ndarray):
    return (ut.dotProd(vec,line_n) -  ut.dotProd(line_p,line_n))



def ClipAgainstLine(line_n:Vec2D, line_p: Vec2D, lst_tris:list[Tris2D]):
    clipped = []
    for (tri) in lst_tris:
        
        lst_ps = [tri.p1,tri.p2,tri.p3]


        lst_vios = []
        lst_good = []
        
        for p in lst_ps:
            if SDistFromLine(line_n.numpify(),line_p.numpify(),p.numpify()) < 0:
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

            n1_tri  = Tris2D(n1_poi, gp1    , gp2 ) 
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

def view(l:Vec3D,a:Vec3D,b:Vec3D,c:Vec3D,player_head:Vec3D):
        mat_view =  np.array([
            [a.x                         ,                         c.x,                         b.x,0],
            [a.z                         ,                         c.z,                         b.z,0],
            [a.y                         ,                         c.y,                         b.y,0],
            [-player_head.dotProd(a)     ,-player_head.dotProd(c)     ,-player_head.dotProd(b)     ,1]
        ])
        vect =np.array( [l.x,l.z,l.y,1])

        vect_view = vect.dot(mat_view)

        #print(vect_view)
        return Vec3D(vect_view[0],vect_view[2],vect_view[1])
def viewTri(tri:Tris3D,a:Vec3D,b:Vec3D,c:Vec3D,player_head:Vec3D):
        view_tri =  Tris3D(view(tri.p1,a,b,c,player_head),view(tri.p2,a,b,c,player_head),view(tri.p3,a,b,c,player_head))
        """print("ORIGINAL NORM: ", tri.norm)
        print("VIEW NORM    : ", view_tri.norm) 
        print("____________")"""
        return view_tri

def calc(l:Vec3D,tan_fov,q,near):
    mat_proj = np.array([
            [tan_fov,            0,                     0,0],
            [   0        ,tan_fov,0                      ,0],
            [           0,           0,q                 ,1],
            [           0,           0,-near*q     ,0]
        ])

    vect =np.array( [l.x,l.z,l.y,1])
    vect_proj =(vect).dot(mat_proj)

    l.w = vect_proj[2]

    vect2d = Vec2D(vect_proj[0]/vect_proj[3] , vect_proj[1]/vect_proj[3],  w=1/vect_proj[3])
    return vect2d

def clip3D (tri : Tris3D,near:int):

        #TODO implement clipping

        """tri.updateNorm()
        return [tri]
        """

        #clip against the near plane
        o_norm            = tri.norm
        lst_p:list[Vec3D] =  [tri.p1 ,tri.p2,tri.p3] 

        plane_p = Vec3D(0,near,0)
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

            # p.SDistFromPlane(Vec3D(0,1,0),plane_p)
            if p.y  < 1 :
                lst_vios.append(p)
            else:
                lst_good.append(p)

        if len(lst_vios) == 0 :
           return [tri]
        elif len(lst_vios) == 1:
            vio_p = lst_vios[0]
            """print(vio_p)
            print("VIO 1")"""

            pg1  = lst_good[0]
            pg2  = lst_good[1]

            
            if pg1.z < pg2.z:
                pg1,pg2 = pg2,pg1
   
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
            vio_p1 = lst_vios[0]
            vio_p2 = lst_vios[1]

            n_poi1 = FindIntersectPoi(Vec3D(0,1,0), plane_p,vio_p1, lst_good[0])
            n_poi2 = FindIntersectPoi(Vec3D(0,1,0), plane_p,vio_p2, lst_good[0])


            n_tri = Tris3D(n_poi1,n_poi2, lst_good [0])

            if not(n_tri.norm.is_equal(o_norm,epsilon=0.01)):
                n_tri = Tris3D(n_poi2,n_poi1, lst_good[0])


            
            #n_tri.col = "blue"
            return [n_tri]  
        else:
            return []



def clip2D(tri:Tris2D):
    lst_tri = [tri]

    global numpy_num_tris_BC

    if parse_2d_tris:
        list_2d_numpy_BC[6*numpy_num_tris_BC+ 0] = tri.p1.x
        list_2d_numpy_BC[6*numpy_num_tris_BC+ 1] = tri.p1.y
        list_2d_numpy_BC[6*numpy_num_tris_BC+ 2] = tri.p2.x
        list_2d_numpy_BC[6*numpy_num_tris_BC+ 3] = tri.p2.y
        list_2d_numpy_BC[6*numpy_num_tris_BC+ 4] = tri.p3.x
        list_2d_numpy_BC[6*numpy_num_tris_BC+ 5] = tri.p3.y
        numpy_num_tris_BC += 1

    x_neg = ClipAgainstLine(Vec2D(1,0),Vec2D(-1,0),lst_tri)
    if len(x_neg) == 0:
        return []
    y_pos = ClipAgainstLine(Vec2D(0,-1),Vec2D(0,1),x_neg)
    if len(y_pos) == 0:
        return []
    x_pos = ClipAgainstLine(Vec2D(-1,0),Vec2D(1,0),y_pos)
    if len(x_pos) == 0 :
        return []
    y_neg = ClipAgainstLine(Vec2D(0,1),Vec2D(0,-1),x_pos)


        
    
    return y_neg

def draw_tri (tri3D:Tris3D, light , window:GraphWin,tan_fov,q,near,drawn_tri,wireFrame=True,lighting=False ):
    lst_points = []
    for vec in tri3D.getPoints():
        lst_points.append(calc(vec,tan_fov,q,near))

    v2_p1 = lst_points[0]
    v2_p2 = lst_points[1]
    v2_p3 = lst_points[2]
        

    #print (tri3D.p1,tri3D.p2,tri3D.norm)

    l_c:list[Tris2D] = clip2D(Tris2D(v2_p1, v2_p2, v2_p3))

    


            
    if wireFrame and lighting:
            for tri_c in l_c:



                tri_c.setOutline("white")
                red    = int(light * 255)
                green  = int(light * 255)
                blue   = int(light * 255)
                tri_c.setFill(color_rgb(red,green,blue))
    elif wireFrame:
            for tri_c in l_c:
                tri_c.setOutline("white")
    elif lighting :
            for tri_c in l_c:
                
                red    = int(light * 255)
                green  = int(light * 255)
                blue   = int(light * 255)
                tri_c.setOutline(color_rgb(red,green,blue))
                tri_c.setFill(color_rgb(red,green,blue))


    for tri_c in l_c:
        

            #sema.acquire()
            #tri_c.draw_tri(window)
            drawn_tri.append(tri_c)
            


first_tri = 0 
check_first = True

def Pipeline(tri:Tris3D,a:Vec3D,b:Vec3D,c:Vec3D,player_head:Vec3D,near:float,lighting:bool,wireFrame:bool,window:GraphWin,tan_fov,q,drawn_tri):
    
    if(tri.norm.dotProd(player_head.subVec(tri.midPoi())) < 0 and not(parse_3d_tris ) and not(parse_2d_tris)):
        return
    # if(tri.norm.dotProd(b)) > 0 and not(parse_3d_tris ) and not(parse_2d_tris):
    #     return


    global numpy_num_tris_3BC
    
    if parse_3d_tris:
        for point in range(3):
            for cord in range(3):
                list_3d_numpy_BC[9*numpy_num_tris_3BC + 3*point + cord] = tri.getPoints()[point].numpify()[cord]
    
        numpy_num_tris_3BC += 1 

            


    view_tri       = viewTri(tri,a,b,c,player_head)
    tri_3D_clipped = clip3D(view_tri,near)

    global numpy_num_tris_3VC
    global numpy_num_tris_3AC
    global first_tri 
    global check_first
    



    if parse_3d_tris:

        for point in range(3):
            for cord in range(3):
                list_3d_numpy_VC[9*numpy_num_tris_3VC + 3*point + cord] = view_tri.getPoints()[point].numpify()[cord] 
        numpy_num_tris_3VC += 1 

        for num_tris in range(len(tri_3D_clipped)):
            for point in range(3):
                for cord in range(3):
                    list_3d_numpy_AC[9*numpy_num_tris_3AC + 3*point + cord] = tri_3D_clipped[num_tris].getPoints()[point].numpify()[cord]
            numpy_num_tris_3AC += 1 


    # if len(tri_3D_clipped) > 0 and check_first:
    #     print("first: ", first_tri)
    #     check_first = False


    if first_tri == 0 and len(tri_3D_clipped) > 0:
        print("INPUT TRI: \n\n" , tri,"\n\n")
        print("OUTPUT TRI: \n\n" , "\n".join(  str(i) for i in tri_3D_clipped ),"\n\n")
        print("LEN CLIP: " , len(tri_3D_clipped))
    first_tri +=1 
    #tri_3D_clipped = [tri]

    for tri2 in tri_3D_clipped:
        
        #dot  = tri2.norm.dotProd((Vec3D(0,0,0).subVec(tri2.midPoi())).normalizeVec())
        #print("NORM: " ,tri.norm," VEC: ",tri.midPoi())
        #dot  = tri.norm.dotProd(self.player_head.subVec(self.mid_poi).normalizeVec())
        if lighting :
            light  = -1*tri2.norm.y
            if light <= 0:
                light = 0.1
            
            draw_tri(tri2,light,window,tan_fov,q,near,drawn_tri,wireFrame,lighting )
        elif not (lighting):
            light  = 1
                
            draw_tri(tri2,light,window,tan_fov,q,near,drawn_tri,wireFrame,lighting )

    pass


def runPipeLine(tri:Tris3D,a:Vec3D,b:Vec3D,c:Vec3D,player_head:Vec3D,near:float,lighting:bool,wireFrame:bool,window:GraphWin,tan_fov,q,drawn_tri,lst_3D_Tris):
    pass



class Camera:
    def __init__(self, player_head: Vec3D, norm_vec, b1:Vec3D, b2:Vec3D,  height=600,width=600, 
                near=1, far=800,fov=90,usePygame=False,pixelArray=np.empty(shape=(0),dtype=np.uint8)):
        self.player_head = player_head
        self.usePygame = usePygame
        self.zaw   = 0 
        self.pitch = 0 
        self.tan_fov = 1/m.tan(m.radians(fov/2))
        self.q       = far/(far- near)  
        self.near    = near
        self.far = far
        self.a = Vec3D(1,0,0)
        self.b = Vec3D(0,1,0)
        self.c = Vec3D(0,0,1)
        self.pixelArray = pixelArray
        """self.mat_view =  np.array([
            [self.a.x                         ,                         self.c.x,                         self.b.x,0],
            [self.a.z                         ,                         self.c.z,                         self.b.z,0],
            [self.a.y                         ,                         self.c.y,                         self.b.y,0],
            [-self.player_head.dotProd(self.a),-self.player_head.dotProd(self.c),-self.player_head.dotProd(self.b),1]
        ])"""

        self.scale = near


        self.mid_poi = self.player_head + Vec3D(0,near,0)
        print("Use Pygame: ", self.usePygame)
        if not(self.usePygame):
            print("MID POI: ", self.mid_poi)
            print("Player head: ", self.player_head)
            self.window    = GraphWin("Lib", height=height ,width= width,autoflush=False)
            self.window.setBackground("black")
            self.window.setCoords(-1,-1,1,1)

        else:
            pass
            

        self.drawn_tri = []
        self.norm_vec = norm_vec        


 

        self.height = height
        self.width = width


        self.DepthBuffer = np.zeros(shape=(height,width),dtype=np.float32)
        
        self.useNumpy = False

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
        """l_d = []
        l_c:list[Tris3D] = []

        l_v  = []"""

        
        """
        for i in range(len(lst_tri3D)):

            tri = lst_tri3D[i]
            
            l_c = self.clip3D(self.viewTri(tri))


            
            for j in range(len(l_c)):
                tri2 = l_c[j]
                dot  = tri2.norm.dotProd((Vec3D(0,0,0).subVec(tri2.midPoi())).normalizeVec())

                #print("NORM: " ,tri.norm," VEC: ",tri.midPoi())
                #dot  = tri.norm.dotProd(self.player_head.subVec(self.mid_poi).normalizeVec())
                if dot >= 0 and lighting :
                    light  = tri2.norm.dotProd(Vec3D(0,0,0).subVec(Vec3D(0,1,0)).normalizeVec())

                    if light <= 0:
                        light = 0.1

                    self.draw_tri(tri2, light,wireFrame,lighting=True)
                elif not (lighting):
                    pass
                    self.draw_tri(tri2,wireFrame,lighting=False)"""

    
        
        for tri in lst_tri3D:
            
            # Pipeline(tri:Tris3D,a:Vec3D,b:Vec3D,c:Vec3D,player_head:Vec3D,near:float,lighting:bool,wireFrame:bool,window:GraphWin,drawn_tri,sema):
            # th.Thread(target=Pipeline,args=(tri,self.a,self.b,self.c,self.player_head,self.near,lighting,wireFrame,self.window,self.tan_fov,self.q,self.drawn_tri,bs)).start()
            Pipeline(tri,self.a,self.b,self.c,self.player_head,self.near,lighting,wireFrame,self.window,self.tan_fov,self.q,self.drawn_tri)
        
            #print(len(self.drawn_tri))
            pass
            
        #print(lst_tri3D[0])

        global numpy_num_tris_AC
        global parse_2d_tris
        
        #self.drawn_tri = []
        for tri in self.drawn_tri:
            tri:Tris2D
            tri.draw_tri(self.window)

            if parse_2d_tris:
                list_2d_numpy_AC[6*numpy_num_tris_AC+ 0] = tri.p1.x
                list_2d_numpy_AC[6*numpy_num_tris_AC+ 1] = tri.p1.y
                list_2d_numpy_AC[6*numpy_num_tris_AC+ 2] = tri.p2.x
                list_2d_numpy_AC[6*numpy_num_tris_AC+ 3] = tri.p2.y
                list_2d_numpy_AC[6*numpy_num_tris_AC+ 4] = tri.p3.x
                list_2d_numpy_AC[6*numpy_num_tris_AC+ 5] = tri.p3.y
                
                numpy_num_tris_AC += 1 
        
        if parse_2d_tris:
            with open('AC.txt', 'w+') as fp:
                fp.write("\n".join(str(item) for (idx, item) in enumerate(list_2d_numpy_AC) if idx < 6*numpy_num_tris_AC ))

            with open('BC.txt', 'w+') as fp:
                fp.write("\n".join(str(item) for (idx,item) in enumerate(list_2d_numpy_BC) if idx < 6*numpy_num_tris_BC ))


            with open('len.txt','w+') as fp:
                fp.write(str(numpy_num_tris_AC*6)+"\n")
                fp.write(str(numpy_num_tris_BC*6)+"\n")


            print("NUM TRIS AC: ", len(self.drawn_tri))

        if parse_3d_tris:
            with open('VC_3D.txt','w+') as fp:
                fp.write("\n".join(str(item) for (idx,item) in enumerate(list_3d_numpy_VC) if idx < 9*numpy_num_tris_3VC))

            with open('AC_3D.txt','w+')   as fp :
                fp.write("\n".join(str(item) for (idx,item) in enumerate(list_3d_numpy_AC) if idx < 9*numpy_num_tris_3AC))

            with open('len3D.txt','w+') as fp:
                fp.write(str(numpy_num_tris_3BC)+'\n')
                fp.write(str(numpy_num_tris_3VC)+'\n')
                fp.write(str(numpy_num_tris_3AC)+'\n')


            print("len of list_3d_numpy_BC: ", len(list_3d_numpy_BC)) 
            print("numpy_num_tris_3BC     : ", numpy_num_tris_3BC)
            # print("NUM 3d TRIS            : ", len(self.lst3d_tris))
        
            #print("numpy_num_tris_3BC: ", numpy_num_tris_3BC)
            with open('BC_3D.txt', 'w+') as fp:
                fp.write("\n".join(str(item) for (idx, item) in enumerate(list_3d_numpy_BC) if idx < 9*numpy_num_tris_3BC ))


    def draw_tris_nump (self, lst_tri3D:np.ndarray,lstUvTris:np.ndarray,textBuff:np.ndarray,wireFrame=True,FillCol=True,cullFace=True,lighting=True):

        self.useNumpy = True


        self.DepthBuffer = np.zeros(shape=(self.height,self.width),dtype=np.longdouble)

        # self.DepthBuffer =np.ones(shape=(self.height,self.width),dtype=np.longdouble)
        zbuff2D_bc = np.zeros(shape=(len(lst_tri3D)*2*3 + 1),dtype=np.longdouble)
        zbuff2D_ac = np.zeros(shape=(2*len(lst_tri3D)*1*3*16 + 1),dtype=np.longdouble)

        
        uvTrisResBuff2D_AC = np.zeros(shape=(2*len(lst_tri3D)*16,3,2),dtype = np.float64)

        pla = self.player_head.numpify()
        lst_2D = p2D3D.RunPipeLines(lst_tri3D,self.a.numpify(),self.b.numpify(),self.c.numpify(),
                                    pla,self.near,self.q,self.tan_fov,zbuff2D_bc,zbuff2D_ac,lstUvTris, uvTrisResBuff2D_AC,
                                    cullFace)

        # print("Player head: ",self.player_head.numpify())


        #print("zbuff2D_bc[-1]: " ,zbuff2D_bc[-1])
        tot2DTris = int(lst_2D[-1])

        # print("Lst 2D: ", lst_2D)
        # print("TOT 2D TRIS: ",tot2DTris, "\n\n\n\n" )


        #tot2DTris = 0 

        if not( self.usePygame):
            tri_idx= 0
            while tri_idx < tot2DTris:
                lst_ps:list[Point] = [] 
                for point in range(3):
                    lst_ps.append(Point(lst_2D[6*tri_idx + 2*point + 0], lst_2D[6*tri_idx + 2*point + 1] ))

                poly = Polygon(lst_ps[0],lst_ps[1],lst_ps[2],lst_ps[0])
                
                poly.setFill("white")
                poly.setOutline("blue")
                self.drawn_tri.append(poly)

                poly.draw(self.window)
                tri_idx+=1    
        else:
            DrawTris(lst_2D,self.pixelArray,self.width,self.height,tot2DTris,zbuff2D_ac,self.DepthBuffer,uvTrisResBuff2D_AC,textBuff,self.q, self.near, outLine=wireFrame,FillCol=FillCol)



    def getDrawnList(self,numpList):

        pass


    def drawMesh (self,mesh: Mesh, wireFrame=True,lighting=True , FillCol=True , cullFace=True):
        if not (mesh.isNumpy):
            self.draw_tris(mesh.lst3d_tris,wireFrame,lighting)

        else:
            self.draw_tris_nump(mesh.numpListTri,mesh.UVtris,mesh.TextBuff,cullFace=cullFace,FillCol=FillCol,wireFrame=wireFrame)
    def unDrawTris(self,lighting=True):
        if self.useNumpy and self.usePygame:
            clear(self.pixelArray,self.width*self.height*3, 100)
            return
        if self.useNumpy:
            for poly in self.drawn_tri:
                poly.undraw()      

        else:
            for tri in self.drawn_tri:
                tri.poly.undraw()

        self.drawn_tri = []  

    def unDrawTri(self,tri3D:Tris3D): 
        tri3D.poly.undraw()

        pass
    def draw_tri (self, tri3D:Tris3D, light , wireFrame=True,lighting=False ):
        lst_points = []
        for vec in tri3D.getPoints():
            lst_points.append(self.calc(vec))

        v2_p1 = lst_points[0]
        v2_p2 = lst_points[1]
        v2_p3 = lst_points[2]
        

        #print (tri3D.p1,tri3D.p2,tri3D.norm)

        l_c:list[Tris2D] = self.clip2D(Tris2D(v2_p1, v2_p2, v2_p3))

        
        if lighting:
            red    = int(light * 255)
            green  = int(light * 255)
            blue   = int(light * 255)

       

            for tri_c in l_c:
                tri_c.setFill(color_rgb(red,green,blue))
                tri_c.setOutline(color_rgb(red,green,blue))


            
        if wireFrame and lighting:
            for tri_c in l_c:
                tri_c.setOutline("white")
                red    = int(light * 255)
                green  = int(light * 255)
                blue   = int(light * 255)
                tri_c.setFill(color_rgb(red,green,blue))
        elif wireFrame:
            for tri_c in l_c:
                tri_c.setOutline("white")
        elif lighting :
            for tri_c in l_c:
                
                red    = int(light * 255)
                green  = int(light * 255)
                blue   = int(light * 255)
                tri_c.setOutline(color_rgb(red,green,blue))
                tri_c.setFill(color_rgb(red,green,blue))


        for tri_c in l_c:
            
            tri_c.draw_tri(self.window)
            self.drawn_tri.append(tri_c)


        
        
        

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


        #self.mid_poi.add_z(incr)
        self.player_head.add_z(incr) 


    

    def undrawMesh (self,mesh:Mesh):
        self.unDrawTris()

    def calcS(self, l : Vec3D):


        t = l.subVec(self.mid_poi)
        p = self.player_head.subVec(self.mid_poi)
        q = t.subVec(p)

        norm_vec = Vec3D(0,3,3)
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
        lst_p:list[Vec3D] =  [tri.p1 ,tri.p2,tri.p3] 

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
            if p.SDistFromPlane(Vec3D(0,1,0),plane_p) < 0 :
                lst_vios.append(p)
            else:
                lst_good.append(p)

        if len(lst_vios) == 0 :
           return [tri]
        elif len(lst_vios) == 1:
            vio_p = lst_vios[0]
            """print(vio_p)
            print("VIO 1")"""

            pg1  = lst_good[0]
            pg2  = lst_good[1]

            
            if pg1.z < pg2.z:
                pg1,pg2 = pg2,pg1
   
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
            vio_p1 = lst_vios[0]
            vio_p2 = lst_vios[1]

            n_poi1 = FindIntersectPoi(Vec3D(0,1,0), plane_p,vio_p1, lst_good[0])
            n_poi2 = FindIntersectPoi(Vec3D(0,1,0), plane_p,vio_p2, lst_good[0])


            n_tri = Tris3D(n_poi1,n_poi2, lst_good [0])

            if not(n_tri.norm.is_equal(o_norm,epsilon=0.01)):
                n_tri = Tris3D(n_poi2,n_poi1, lst_good[0])


            
            #n_tri.col = "blue"
            return [n_tri]  
        else:
            return []
        #print(self.player_head.subVec(self.mid_poi).magnitude())
        



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
        if len(x_neg) == 0:
            return []
        y_pos = ClipAgainstLine(Vec2D(0,-1),Vec2D(0,1),x_neg)
        if len(y_pos) == 0:
            return []
        x_pos = ClipAgainstLine(Vec2D(-1,0),Vec2D(1,0),y_pos)
        if len(x_pos) == 0 :
            return []
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


        # self.norm_vec.rotateZ_(angle)


        # Q = self.mid_poi.subVec(self.player_head)

        # Q.rotateZ_(angle)

        # self.mid_poi = self.player_head.addVec(Q) 

        # self.zaw  += angle 



        # self.b1.rotateZ_(angle)
        # self.b2.rotateZ_(angle)

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

        #self.player_head = self.player_head.addVec(vec)

        self.player_head.add_x(vec.x)
        self.player_head.add_y(vec.y)
        self.player_head.add_z(vec.z)