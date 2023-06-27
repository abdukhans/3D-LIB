import numpy as np
from numba import njit
import cProfile
import pstats
import math as m
import matplotlib.pyplot as plt

with open ("len.txt") as fp:
    lenText =  [ line.rstrip() for line in fp]


with open ("AC.txt") as fp:
    ACText =  [ line.rstrip() for line in fp]

with open ("BC.txt") as fp:
    BCText =  [ line.rstrip() for line in fp]




len_ac = int(lenText[0])
len_bc = int(lenText[1])

ac_arr = np.empty(len_ac,dtype=np.float64)
bc_arr = np.empty(len_bc,dtype=np.float64)
res_buf    = np.zeros(shape=len_ac, dtype=np.float64)

ac_id = 0 
for string in ACText:
    ac_arr[ac_id] = float(string)
    ac_id += 1 

bc_id = 0 
for string in BCText:
    bc_arr[bc_id] = float(string)

    bc_id += 1 


# ac3D_arr = np.empty(,dtype=np.float64)


@njit
def mag(vec:np.ndarray):
    mag_ = 0 
    for i in vec:
        mag_ += i**2

    return mag_**0.5

@njit
def norm(vec:np.ndarray):
    return vec/mag(vec)



@njit
def dotProd3(v1,v2):
    sum_ =  0
    for i in range(3):
        sum_ += v1[i]*v2[i]
    return sum_    

@njit
def dotProd2(v1,v2):
    sum_ =  0
    for i in range(2):
        sum_ += v1[i]*v2[i]
    return sum_   

@njit
def FindIntersectPoi3D(plane_n:np.ndarray, plane_p:np.ndarray,line_start:np.ndarray, line_end:np.ndarray):
    plane_n = norm(plane_n)
    #print("d " ,plane_n)
    plane_d:float = -dotProd3(plane_n,plane_p)
    ad:float      = dotProd3(line_start,plane_n)
    bd:float      = dotProd3(line_end,plane_n)

    #print("ad", ad + 2 )
    t = (-plane_d - ad) / (bd - ad)

    lineStartToEnd = np.subtract(line_end,line_start)
    #print("t: ", lineStartToEnd)    

    lineToIntersect = t*lineStartToEnd
    return np.add(line_start,lineToIntersect)








#print('done2')


@njit
def FindIntersectPoi2D(line_n:np.ndarray, line_p:np.ndarray,line_start:np.ndarray, line_end:np.ndarray):
    line_n = norm(line_n)
    line_d = -dotProd2(line_n,line_p)
    ad      = dotProd2(line_start,line_n)
    bd      = dotProd2(line_end,line_n)
    t = (-line_d - ad) / (bd - ad)
    
    lineStartToEnd = np.subtract( line_end,line_start)
    lineToIntersect = t*lineStartToEnd
    return np.add( line_start,lineToIntersect)




@njit
def SDistFromLine (line_n:np.ndarray, line_p:np.ndarray, vec:np.ndarray):
    line_n = norm(line_n)
    return (dotProd2(vec,line_n) -  dotProd2(line_p,line_n))





@njit
def makeTri2D(p1:np.ndarray,p2:np.ndarray,p3:np.ndarray):

    return np.array( [p1[0],p1[1],p2[0],p2[1],p3[0],p3[1]])


    
"""
    line_n   : the line norm
    line_p   : a point on the line 
    lst_tris : the list of triangles. The list has a very particular form. Each tri has 3 points p1,p2 and p3.
               A triangle will show up in the list as:
               [p1.x,p1.y,p2.x,p2.y,p3.x,p3.y,1].
               Note that the last element should contain the number of triangles in the lst_tris.
    num_tris : This is an integer that holds the number of triangles in lst_tris  
    len_clip : This is a variable that holds ends up holding the number of triangles that are in the
               clip buffer


    RET:
        It will return a list of 2d triangles in numpy array from. Where the last element in the 
        buffer will contain the number of triangles in the array. The size of the clipped buff will 
        always be 12x(num_tris) + 1  so the index number will be 12x(num_tris) in order to get the 
        number of triangles currently in the clipped buff. 
"""
@njit
def ClipAgainstLine2D(line_n:np.ndarray, line_p: np.ndarray, lst_tris:np.ndarray, num_tris:float):
    int_num_tris = int(num_tris)
    clipped  = np.empty(shape=int_num_tris*2*3*2 + 1 ,dtype=np.float64)
    last_elm = int_num_tris*2*3*2  
    
    # num_t iterates through triangle space in lst_tris
    num_t    = 0  
    
    len_clip = 0 
    #TODO change this into a for loop
    for num_t_int in range(int(num_tris)):
        
        num_t = float(num_t_int)

        lst_ps = np.array([lst_tris[6*num_t_int + 0],lst_tris[6*num_t_int + 1],lst_tris[6*num_t_int + 2],
                           lst_tris[6*num_t_int + 3],lst_tris[6*num_t_int + 4],lst_tris[6*num_t_int + 5]])
        
        lst_vios = np.empty(6,dtype=np.float64)
        lst_good = np.empty(6,dtype=np.float64)
        
        idx      = 0  # iterates through point space in lst_ps
        num_vios = 0  
        num_good = 0 


        # TODO change this into a for loop instead
        for idx in range(3):            
            if SDistFromLine(line_n,line_p, np.array([lst_ps[2*idx],lst_ps[2*idx+1]])) < 0:
                lst_vios[2*num_vios]    =  lst_ps[2*idx]
                lst_vios[2*num_vios + 1] = lst_ps[2*idx + 1 ]
                num_vios += 1 
            else:
                lst_good[2*num_good] = lst_ps[2*idx]
                lst_good[2*num_good + 1] = lst_ps[2*idx + 1]
                num_good += 1


        
        if num_vios == 0:
            
            for i in range(6):
                clipped[6*len_clip  + i] = lst_ps[i]

            
            #print("Before nv = 0 ", len_clip)
            len_clip += 1 
            #print("AFTER incr    ", len_clip)


        elif num_vios == 1:
            vio_px,vio_py =  lst_vios[0],lst_vios[1]
            gp1x,gp1y     =  lst_good[0],lst_good[1]
            gp2x,gp2y     =  lst_good[2],lst_good[3]

            if gp1y < gp2y:
                gp1x,gp2x= gp2x, gp1x
                gp1y,gp2y= gp2y, gp1y



            vio_p   = np.array([vio_px,vio_py])
            gp1     = np.array([gp1x,gp1y])
            gp2     = np.array([gp2x,gp2y])
            n1_poi  = FindIntersectPoi2D(line_n, line_p,vio_p , gp1  )
            n2_poi  = FindIntersectPoi2D(line_n, line_p,vio_p , gp2  )

            # n1_tri  = Tris2D (n1_poi, gp1 , gp2 )  is simulated below
            clipped[6*len_clip + 0  ] =  n1_poi[0]
            clipped[6*len_clip + 1  ] =  n1_poi[1]
            clipped[6*len_clip + 2  ] =  gp1[0]
            clipped[6*len_clip + 3  ] =  gp1[1]
            clipped[6*len_clip + 4  ] =  gp2[0]
            clipped[6*len_clip + 5  ] =  gp2[1]

            len_clip += 1 


            # n2_tri  = Tris2D(n1_poi, n2_poi , gp2 )  is simulated below
        
            clipped[6*len_clip + 0  ] =  n1_poi[0]
            clipped[6*len_clip + 1  ] =  n1_poi[1]
            clipped[6*len_clip + 2  ] =  n2_poi[0]
            clipped[6*len_clip + 3  ] =  n2_poi[1]
            clipped[6*len_clip + 4  ] =  gp2[0]
            clipped[6*len_clip + 5  ] =  gp2[1]

          

            len_clip += 1 


        elif num_vios ==2:
            vio_p1 =  np.array([lst_vios[0],lst_vios[1]])
            vio_p2 =  np.array([lst_vios[2],lst_vios[3]])
            gp     =  np.array([lst_good[0],lst_good[1]])
            if vio_p1[1] < vio_p2[1]:
                #print("VIO p1: ", vio_p1)
                #print("VIO p2: ", vio_p2)
                vio_p1[1], vio_p2[1]= vio_p2[1], vio_p1[1]
                vio_p1[0], vio_p2[0]= vio_p2[0], vio_p1[0]
                #print("VIO p1: ", vio_p1)
                #print("VIO p2: ", vio_p2)
                #print("_______________________")

            n1_poi  =   FindIntersectPoi2D(line_n,line_p,vio_p1 , gp )
            n2_poi  =   FindIntersectPoi2D(line_n,line_p,vio_p2 , gp )


            # n_tri = Tris2D(n1_poi,n2_poi,gp) is simulated below
            clipped[6*len_clip + 0  ] =  n1_poi[0]
            clipped[6*len_clip + 1  ] =  n1_poi[1]
            clipped[6*len_clip + 2  ] =  n2_poi[0]
            clipped[6*len_clip + 3  ] =  n2_poi[1]
            clipped[6*len_clip + 4  ] =  gp[0]
            clipped[6*len_clip + 5  ] =  gp[1]
            
    
            len_clip += 1 
            pass
        #elif num_vios == 3:
        #    pass


        #print(num_t)
        #num_t += 1 

    clipped[last_elm] = len_clip
    #print("Clip buff: ",clipped)
    #print("______________________________")
    #print(clipped , len_clip)
    return clipped



"""
    tri      : A triangle in numpy array form. We assume that 
               that there is only one tri in the array.
    len_clip : A variable that will hold the the 
               number of triangles in the 
               clip buff 
"""
@njit
def clip2D(tri:np.ndarray) -> np.ndarray:



    # ClipAgainstLine(line_n:Vec2D, line_p: Vec2D, lst_tris:list[Tris2D])
    # ClipAgainstLine2D(line_n:np.ndarray, line_p: np.ndarray, lst_tris:np.ndarray, num_tris:float) 

    # x_neg = ClipAgainstLine(Vec2D(1,0),Vec2D(-1,0),lst_tri) is simulated below 
    x_neg_n        = np.array([1,0])
    x_neg_p        = np.array([-1,0])
    x_neg          = ClipAgainstLine2D(x_neg_n,x_neg_p,tri,1.0)
    x_neg_num_tris = x_neg[12*1]


    #print("x_neg: ", x_neg_num_tris)
    #print("______________________________")

    if int(x_neg_num_tris) == 0:
        #print("run1")
        res =  np.zeros(shape=1, dtype=np.float64)
        res[0]  = 0.0
        return res

    # y_pos = ClipAgainstLine(Vec2D(0,-1),Vec2D(0,1),x_neg) is simulated below 
    y_pos_n        = np.array([0,-1])
    y_pos_p        = np.array([0, 1])
    y_pos          = ClipAgainstLine2D(y_pos_n,y_pos_p,x_neg,x_neg_num_tris)
    y_pos_num_tris = y_pos[int(x_neg_num_tris) * 12]
    
    #print("y_pos: ", y_pos_num_tris)
    if int(y_pos_num_tris) == 0:
        #print("run2")
        res =  np.zeros(shape=1, dtype=np.float64)
        res[0]  = 0.0
        return res


    #  ClipAgainstLine(Vec2D(-1,0),Vec2D(1,0),y_pos) is simulated below
    x_pos_n        = np.array([-1,0])
    x_pos_p        = np.array([1 ,0])
    x_pos          = ClipAgainstLine2D(x_pos_n,x_pos_p,y_pos,y_pos_num_tris)
    x_pos_num_tris = x_pos[12*int(y_pos_num_tris)]

    #print("x_pos: ", x_pos_num_tris)
    if int(x_pos_num_tris) == 0 :
        #print("run3")
        res =  np.zeros(shape=1, dtype=np.float64)
        res[0]  = 0.0
        return res


    #y_neg = ClipAgainstLine(Vec2D(0,1),Vec2D(0,-1),x_pos) is simulated below
    y_neg_n        = np.array([0,1])
    y_neg_p        = np.array([0,-1])
    y_neg          = ClipAgainstLine2D(y_neg_n,y_neg_p,x_pos,x_pos_num_tris)
    y_neg_num_tris = y_neg[12*int(x_pos_num_tris)]
    #print("y_neg: ", y_neg_num_tris)
    if y_neg_num_tris == 0 :
        #print("run4")
        res =  np.zeros(shape=1, dtype=np.float64)
        res[0]  = 0.0
        return res

    

    return y_neg



#@njit
def test(res_buf:np.ndarray):
    tri_idx    = 0 
    append_idx:int = 0 
    while tri_idx < len_bc//6:
        
        tri_c                = np.array([bc_arr[6*tri_idx + 0], bc_arr[6*tri_idx + 1],bc_arr[6*tri_idx + 2]
                                        ,bc_arr[6*tri_idx + 3], bc_arr[6*tri_idx + 4],bc_arr[6*tri_idx + 5]])
        clip_buff:np.ndarray = clip2D(tri_c)
        # print("____________")
        len_clip             = clip_buff[len(clip_buff) - 1]
        
        for i in range(6*int(len_clip)):
            res_buf[append_idx + i] = clip_buff[i]

        append_idx += int(6*len_clip)
        # print(append_idx)
        tri_idx += 1 

    num_err = 0 
    for i in range(len_ac):
        num_ac = ac_arr[i]
        res_ac = res_buf[i]


    if not(m.isclose(num_ac,res_ac,abs_tol=0.00000)):
            print("NUM_AC_ARR: ", num_ac)
            print("NUM_RE_ARR: ", res_ac)
            print("Index Fail: ", i )
            num_err += 1 


    print("NUM ERR: ", num_err)



    plt.plot([i for idx,i in np.ndenumerate(res_buf) if idx[0]%10 == 0],label='res_buff')
    plt.plot([i for idx,i in np.ndenumerate(ac_arr) if idx[0]%10 == 0],label= 'ac_arr')
    plt.legend()
    plt.show()
    


def test_BC_arr_AC(abs_tot,len_bc_arr):

    with open("BC.txt", "r") as fp:
        text = fp.read().split('\n')
        for i in range(len_bc_arr):
            num_text = float(text[i])
            num_bc   = bc_arr[i]

            if not(m.isclose(num_text,num_bc,abs_tol=abs_tot)):
                print("NUM_BC_TXT: ", num_text)
                print("NUM_BC_ARR: ", num_bc)
                print("Index Fail: ", i )
                break

        










def main():

    #test_BC_arr_AC(0.001,len_bc)
    print("d")
    test(res_buf)

     
    pass



if __name__ == "__main__":
    main()

    

            
            

"""#print(SDistFromLine(plane_p,plane_n,le))
@njit
def view(l:np.ndarray,a:np.ndarray,b:np.ndarray,c:np.ndarray,player_head:np.ndarray):

        #convention (x,y,z) 
        mat_view =  np.array([
            [a[0]                         ,                         c[0],                             b[0],0],
            [a[2]                         ,                         c[2],                             b[2],0],
            [a[1]                         ,                         c[1],                             b[1],0],
            [-dotProd3(player_head,a)     ,-dotProd3(player_head,c)     ,-dotProd3(player_head,b)         ,1]
        ])
        vect =np.array( [l[0],l[2],l[3],1])

        vect_view = vect.dot(mat_view)

        #print(vect_view)
        return vect_view/vect_view[3]
        
plane_n = np.array([0.0,1.0,0.0])
plane_p = np.array([0.0,1.0,0.0])
ls = np.array([1.0,0.0,0.0])
le = np.array([1.0,3.0,5.0,1.0,3.0,5.0,1.0,3.0,5.0,1.0,3.0,5.0])
num_cli = 0 
print(ClipAgainstLine2D(plane_p,plane_n,le,2,num_cli))
num_cli = 0 
with cProfile.Profile() as pr:
    ClipAgainstLine2D(plane_p,plane_n,le,2,num_cli)
print(num_cli)
stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.TIME)
stats.reverse_order()
stats.print_stats()"""






"""
def viewTri(tri:Tris3D,a:Vec3D,b:Vec3D,c:Vec3D,player_head:Vec3D):
        view_tri =  Tris3D(view(tri.p1,a,b,c,player_head),view(tri.p2,a,b,c,player_head),view(tri.p3,a,b,c,player_head))
    
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


def clip3D (tri : Tris3D,near):

        #TODO implement clipping

    

        #clip against the near plane
        o_norm            = tri.norm
        lst_p:list[Vec3D] =  [tri.p1 ,tri.p2,tri.p3] 

        plane_p = Vec3D(0,near,0)
        #lst_dist = [  i.SDistFromPlane(Vec3D(0,1,0), plane_p) for i in lst_p ]
        lst_vios = []
        lst_good = []

        for p in lst_p: 
        
            if p.SDistFromPlane(Vec3D(0,1,0),plane_p) < 0 :
                lst_vios.append(p)
            else:
                lst_good.append(p)

        if len(lst_vios) == 0 :
           return [tri]
        elif len(lst_vios) == 1:
            vio_p = lst_vios[0]
      

            pg1  = lst_good[0]
            pg2  = lst_good[1]

            
            if pg1.z < pg2.z:
                pg1,pg2 = pg2,pg1
   
            n_poi1 = FindIntersectPoi3D(Vec3D(0,1,0), plane_p,vio_p, pg1)
            n_poi2 = FindIntersectPoi3D(Vec3D(0,1,0), plane_p,vio_p, pg2)

         
    
            

            n_tri1 = Tris3D(n_poi1, pg1 ,pg2)

            n_tri2 = Tris3D( n_poi1, n_poi2 ,pg2)

            #n_tri1.col = "red"
            if not(n_tri1.norm.is_equal(o_norm,epsilon=0.01)):
           
            
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
            pass

            #sema.acquire()
            #tri_c.draw_tri(window)
            drawn_tri.append(tri_c)


def Pipeline(tri:Tris3D,a:Vec3D,b:Vec3D,c:Vec3D,player_head:Vec3D,near:float,lighting:bool,wireFrame:bool,window:GraphWin,tan_fov,q,drawn_tri):

    
    view_tri = viewTri(tri,a,b,c,player_head)

    tri_3D_clipped = clip3D(view_tri,near)
    #tri_3D_clipped = [tri]

    for tri2 in tri_3D_clipped:
        
        dot  = tri2.norm.dotProd((Vec3D(0,0,0).subVec(tri2.midPoi())).normalizeVec())
        #print("NORM: " ,tri.norm," VEC: ",tri.midPoi())
        #dot  = tri.norm.dotProd(self.player_head.subVec(self.mid_poi).normalizeVec())
        if dot >= 0 and lighting :
            light  = tri2.norm.dotProd(Vec3D(0,0,0).subVec(Vec3D(0,1,0)).normalizeVec())
            if light <= 0:
                light = 0.1
            
            draw_tri(tri2,light,window,tan_fov,q,near,drawn_tri,wireFrame,lighting )
        elif not (lighting):
            light  = 1
                
            draw_tri(tri2,light,window,tan_fov,q,near,drawn_tri,wireFrame,lighting )

    pass


def runPipeLine(tri:Tris3D,a:Vec3D,b:Vec3D,c:Vec3D,player_head:Vec3D,near:float,lighting:bool,wireFrame:bool,window:GraphWin,tan_fov,q,drawn_tri,lst_3D_Tris):
    pass
"""