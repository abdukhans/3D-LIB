import numpy as np
from numba import njit
import math as m
import sys 
import matplotlib.pyplot as plt

@njit
def dotProd3(v1,v2):
    sum_ =  0
    for i in range(3):
        sum_ += v1[i]*v2[i]
    return sum_  


@njit 
def dotProdN(v1,v2,n):
    sum_ =  0
    for i in range(n):
        sum_ += v1[i]*v2[i]
    return sum_  



@njit
def mag(vec:np.ndarray):
    mag_ = 0 
    for i in vec:
        mag_ += i**2

    return mag_**0.5

@njit
def norm(vec:np.ndarray):
    return vec/mag(vec)

"""
    vect   : the vector you want to matrix multiply
    matrix : the matrix you want to multiply by 
    size   : the size of the vector you want to
             multiply. The shape is assumed to be 
             a one dimensional tensor 
    NOTE   : we do (V x M) where 'V' is a vector and  'M' is a 
             matrix

    RET:    
        Returns a numpy array that is the matrix vector product

"""
@njit
def vectMatMul(vect:np.ndarray, matrix:np.ndarray,size:int) -> np.ndarray:

    res = np.empty( size,dtype=np.float64)

    mat_trans = matrix.T 
    entry_idx = 0 
    for row in mat_trans:
        res[entry_idx] = dotProdN(vect, row,size)
        entry_idx += 1
            


    return res










"""

    tri      : is the numpy array object you want to store a 3D triangle into.
              NOTE: the shape of this object is assumed to be  a 3 by 3 matrix\

    p1/p2/p2 : These are the 3D points that make up the 3D triangle.
               NOTE: these are 1D arrays with length 3
             
"""
@njit
def populateTri(tri:np.ndarray, p1:np.ndarray,p2:np.ndarray,p3:np.ndarray):
    for row in range(3):
        if row == 0:
            cur = p1
        elif row == 1:
            cur = p2
        else:
            cur = p3

        for entry in range(3):
            tri[row][entry] = cur[entry]



@njit(cache=False)
def view(l:np.ndarray,a:np.ndarray,b:np.ndarray,c:np.ndarray,player_head:np.ndarray):

        #convention (x,y,z) 
        mat_view =  np.array([
            [a[0]                         ,                         c[0],                             b[0],0],
            [a[2]                         ,                         c[2],                             b[2],0],
            [a[1]                         ,                         c[1],                             b[1],0],
            [-dotProd3(player_head,a)     ,-dotProd3(player_head,c)     ,-dotProd3(player_head,b)         ,1]
        ])
        vect =np.array( [l[0],l[2],l[1],1])

        vect_view = vectMatMul(vect,mat_view,4)

        corrected_view = np.array([vect_view[0],vect_view[2],vect_view[1]])
        return corrected_view



@njit
def viewTri(tri:np.ndarray,a:np.ndarray,b:np.ndarray,c:np.ndarray,player_head:np.ndarray):

    p1 = tri[0]
    p2 = tri[1]
    p3 = tri[2]

    res_tri = np.empty(shape=(3,3),dtype=np.float64)

    view_p1 = view(p1,a,b,c,player_head)
    view_p2 = view(p2,a,b,c,player_head)
    view_p3 = view(p3,a,b,c,player_head)

    populateTri(res_tri,view_p1,view_p2,view_p3)

    return res_tri






@njit
def crossProd3(v1:np.ndarray,v2:np.ndarray):


    x1 = v1[0]
    y1 = v1[1]
    z1 = v1[2]

    x2 = v2[0]
    y2 = v2[1]
    z2 = v2[2]


    cross = np.empty(3,dtype=np.float64)

    cross[0] =    y1*z2 - z1*y2 
    cross[1] = -( x1*z2 - z1*x2) 
    cross[2] =    x1*y2 - y1*x2 
    return cross


@njit
def subVec3(v1:np.ndarray,v2:np.ndarray):
    res = np.empty(3,dtype=np.float64)
    for i in range (3):
        res[i] = v1[i] - v2[i]
    return res

@njit
def addVec3(v1:np.ndarray,v2:np.ndarray):
    res = np.empty(3,dtype=np.float64)
    for i in range (3):
        res[i] = v1[i] + v2[i]
    return res






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




"""
    vect       : the vector you want to find the signed distance from
    plane_norm : the normal of the plane you want to find the signed 
                 distance to. NOTE we assume this vector is normalized
    plane_p    : the point on the plane

    RET:    
        Returns the signed disatance from the vector to the plane

"""
@njit
def SDistFromPlane3(vect:np.ndarray,plane_norm:np.ndarray, plane_p:np.ndarray):
    return (dotProd3(vect,plane_norm) - dotProd3(plane_p,plane_norm ))



@njit
def isEqual(v1:np.ndarray, v2:np.ndarray, epsilon):
    len_v1 = len(v1)

    for i in range(len_v1):
        if abs(v1[i] - v2[i]) > epsilon:

            return False

    return True 
    




@njit
def getNorm(tri:np.ndarray):
    p1 = tri[0]
    p2 = tri[1]
    p3 = tri[2]

    side1   = np.subtract(p1,p2)
    side2   = np.subtract(p2,p3)

    norm_vect = norm(crossProd3(side1,side2))
    return norm_vect 
    

@njit
def populateTriTensor(tri_tensor:np.ndarray,tri:np.ndarray,idx:int):
    tri_ins = tri_tensor[idx]
    populateTri(tri_ins,tri[0],tri[1],tri[2])
    







"""
    tri      : this is a 3 by 3 numpy array that is the triangle you want to clip
    near     : the near plane value

    RET   :
            Returns  a 3 dimensional tensor whose elements are 3 by 3 matrices corresponding
            to new 3D triangles
"""
@njit
def clip3D(tri:np.ndarray,near:float):


    # p1     = np.array([tri[0],tri[1],tri[2]],dtype=np.float64)
    # p2     = np.array([tri[3],tri[4],tri[5]],dtype=np.float64)
    # p3     = np.array([tri[6],tri[7],tri[8]],dtype=np.float64)


    p1     = np.array([tri[0][0],tri[0][1],tri[0][2]],dtype=np.float64)
    p2     = np.array([tri[1][0],tri[1][1],tri[1][2]],dtype=np.float64)
    p3     = np.array([tri[2][0],tri[2][1],tri[2][2]],dtype=np.float64)

    side1   = np.subtract(p1,p2)
    side2   = np.subtract(p2,p3)
    plane_p = np.array([0.0,near,0.0],dtype=np.float64)

    o_norm = norm(crossProd3(side1,side2))

    lst_p = np.empty(shape=(3,3),dtype=np.float64)

    

    for row in range(3):
        if row == 0:
            cur = p1
        elif row == 1:
            cur = p2
        else:
            cur = p3

        for entry in range(3):
            lst_p[row][entry] = cur[entry]
   

    

    lst_vios = np.empty(shape=(3,3),dtype=np.float64)
    lst_good = np.empty(shape=(3,3),dtype=np.float64)

    # lst_vios[3] = 0 
    # lst_good[3] = 0 

    num_vios  = 0 
    num_good  = 0




    plane_norm = np.array([0.0,1.0,0.0],dtype=np.float64)
    for p in lst_p:
        if SDistFromPlane3(p,plane_norm,plane_p) < 0:
            
            for entry in range(3):
                lst_vios[num_vios][entry] = p[entry] 

            num_vios+=1 

        else:
            for entry in range(3):
                lst_good[num_good][entry] = p[entry] 

            num_good +=1  


    # epsilon value for comparing norms
    eps = 0.01
    if num_vios == 0:
        res_buff = np.empty(shape=(1,3,3),dtype=np.float64)        
        populateTriTensor(res_buff,tri,0)

        # if idx == inspect:
        #     pass
        #     #print(res_buff)

        return res_buff
    elif num_vios == 1:

        vio_p = lst_vios[0]

        pg1 = lst_good[0]
        pg2 = lst_good[1]


        if pg1[2] < pg2[2]:            
            pg1,pg2 = pg2,pg1

        n_poi1 = FindIntersectPoi3D(plane_norm, plane_p,vio_p, pg1)
        n_poi2 = FindIntersectPoi3D(plane_norm, plane_p,vio_p, pg2)


        n_tri1 = np.empty(shape=(3,3),dtype=np.float64)

        n_tri2 = np.empty(shape=(3,3),dtype=np.float64)

        # for row in range(3):
        #     if row == 0:
        #         cur = n_poi1
        #     elif row == 1:
        #         cur = pg1
        #     else:
        #         cur = pg2
        #     for entry in range(3):
        #         n_tri1[row][entry] = cur[entry]

    

        populateTri(n_tri1,n_poi1,pg1,pg2)
        populateTri(n_tri2,n_poi1,n_poi2,pg2)


        n_tri1_norm = getNorm(n_tri1)
        n_tri2_norm = getNorm(n_tri2)

        
        if not(isEqual(o_norm,n_tri1_norm,eps)):
            populateTri(n_tri1,pg1,n_poi1,pg2)


        if not(isEqual(o_norm,n_tri2_norm,eps)):
            populateTri(n_tri2,n_poi2,n_poi1,pg2)
        

        res_buff = np.empty(shape=(2,3,3),dtype=np.float64)
        populateTriTensor(res_buff,n_tri1,0)
        populateTriTensor(res_buff,n_tri2,1)



        return res_buff
    elif num_vios ==2:

        vio_p1 = lst_vios[0]
        vio_p2 = lst_vios[1]
        n_poi1 = FindIntersectPoi3D(plane_norm, plane_p,vio_p1, lst_good[0])
        n_poi2 = FindIntersectPoi3D(plane_norm, plane_p,vio_p2, lst_good[0])

        n_tri1 = np.zeros(shape=(3,3),dtype=np.float64)

        populateTri(n_tri1,n_poi1,n_poi2,lst_good[0])
        n_tri1_norm = getNorm(n_tri1)
        if not(isEqual(n_tri1_norm,o_norm,eps)):
            populateTri(n_tri1,n_poi2,n_poi1,lst_good[0])
        
        res_buff = np.zeros(shape=(1,3,3),dtype=np.float64)
        
        populateTriTensor(res_buff,n_tri1,0)
        # if idx == inspect:
        #     n_tri1[0][0]= 1.1
        #     print(n_tri1)
        #     print("________jhkj__________")
        return res_buff
    else:
        res_buff = np.empty(shape=(0,3,3),dtype=np.float64)
        # if idx == inspect:
        #     print(res_buff)
        #     print("____________________")
        return res_buff


@njit
def perspectiveProj(vec:np.ndarray,tan_fov:float,q:float,near:float):
    mat_proj = np.array([
            [tan_fov,            0,                     0,0],
            [   0        ,tan_fov,0                      ,0],
            [           0,           0,q                 ,1],
            [           0,           0,-near*q     ,0]
        ])
    vect      = np.array([vec[0],vec[2],vec[1],1.0],dtype=np.float64)
    vect_proj = vectMatMul(vect,mat_proj,4)
    #print("vect: ",vect)
    #print("Vect proj: ",vect_proj)
    perspective_vect = vect_proj/vect_proj[3] 
    #print("Perspective proj: ",perspective_vect)
    return perspective_vect



@njit
def projTri(tri:np.ndarray,tan_fov:float,q:float,near:float):
    tri2D = np.empty(shape=(3,2))
    tri2d_idx = 0
    for point in tri:
        proj_point = perspectiveProj(point,tan_fov,q,near)
        tri2D[tri2d_idx][0]= proj_point[0]
        tri2D[tri2d_idx][1]= proj_point[1]
        tri2d_idx +=1 

    return tri2D











with open("len3D.txt") as fp:
    len3DText = [line.rstrip() for line in fp]

with open("VC_3D.txt") as fp:
    VC3DText = [line.rstrip() for line in fp]

with open("BC_3D.txt") as fp:
    BC3DText = [line.rstrip() for line in fp]

with open("AC_3D.txt") as fp:
    AC3DText = [line.rstrip() for line in fp]



len_3D_bc =  int(len3DText[0])
len_3D_vc =  int(len3DText[1])
len_3D_ac =  int(len3DText[2])


BC_3D_buff      = np.zeros(9*len_3D_bc,dtype=np.float64)
VC_3D_buff      = np.zeros(9*len_3D_vc,dtype=np.float64)
AC_3D_buff      = np.zeros(9*len_3D_ac,dtype=np.float64)


BC_3D_id = 0 
for string in BC3DText:
    BC_3D_buff[BC_3D_id] = float(string)
    BC_3D_id+= 1


VC_3D_id = 0 
for string in VC3DText:
    VC_3D_buff[VC_3D_id] = float(string)
    VC_3D_id+= 1


AC_3D_id = 0 
for string in AC3DText:
    AC_3D_buff[AC_3D_id] = float(string)
    AC_3D_id+=1 




if __name__ == '__main__' and 'test' in sys.argv :

    # with open("len3D.txt") as fp:
    #     len3DText = [line.rstrip() for line in fp]

    # with open("VC_3D.txt") as fp:
    #     VC3DText = [line.rstrip() for line in fp]

    # with open("BC_3D.txt") as fp:
    #     BC3DText = [line.rstrip() for line in fp]

    # with open("AC_3D.txt") as fp:
    #     AC3DText = [line.rstrip() for line in fp]


    
    # len_3D_bc =  int(len3DText[0])
    # len_3D_vc =  int(len3DText[1])
    # len_3D_ac =  int(len3DText[2])


    # BC_3D_buff      = np.zeros(9*len_3D_bc,dtype=np.float64)
    # VC_3D_buff      = np.zeros(9*len_3D_vc,dtype=np.float64)
    # AC_3D_buff      = np.zeros(9*len_3D_ac,dtype=np.float64)
    
    res_VC_3D_buff  = np.zeros(9*len_3D_vc,dtype=np.float64)
    res_AC_3D_buff  = np.empty(9*len_3D_ac,dtype=np.float64)








    #@njit
    def test_VC_3D():
        # self.a = Vec3D(1,0,0)
        # self.b = Vec3D(0,1,0)
        # self.c = Vec3D(0,0,1)

        res_buf_idx = 0 
        cam_a       = np.array([1.0, 0.0, 0.0])
        cam_b       = np.array([0.0, 1.0, 0.0])
        cam_c       = np.array([0  , 0.0, 1.0])
        player_head = np.array([0  ,-2.0, 0.0])
        vect3d      = np.zeros(3,dtype=np.float64)
        #vect3d[3]   = 1 
        
        for tri3D_idx in range ( len_3D_bc):
            
            for point in range (3):
                for cord in range (3):
                    vect3d[cord] = BC_3D_buff[9*tri3D_idx + 3*point + cord ]


                veiw_vect =  view(vect3d,cam_a,cam_b,cam_c,player_head)

                res_VC_3D_buff[res_buf_idx] = veiw_vect[0]
                res_buf_idx+=1

                res_VC_3D_buff[res_buf_idx] = veiw_vect[1]
                res_buf_idx+=1




                res_VC_3D_buff[res_buf_idx] = veiw_vect[2]
                res_buf_idx+=1 


        for i  in range (int(len_3D_vc)):        
            if VC_3D_buff[i] != res_VC_3D_buff[i]:
                print("Incorrect at index:", i)
                print("VC 3D             :", VC_3D_buff[i]     )
                print("Res_VC_3D_Buff    :", res_VC_3D_buff[i]  )
                return


        print("PASSED!!! VC TEST")


    def test_AC_3D():

        near = 1.0

        inspect = 0.2

        inspect_tri  = None
        num_tris_ins = 0 

        res_buff_idx = 0 
        bc_buff_idx  = 0 

        eps = 0.00001
        cam_a       = np.array([1.0, 0.0, 0.0])
        cam_b       = np.array([0.0, 1.0, 0.0])
        cam_c       = np.array([0  , 0.0, 1.0])
        player_head = np.array([0  ,-2.0, 0.0])
        for tri_idx in range(len_3D_bc):
            bc_buff_idx = 9 * tri_idx
            cur_tri = BC_3D_buff[bc_buff_idx: bc_buff_idx + 9 ].reshape(3,3)


            view_tri     = viewTri(cur_tri,cam_a,cam_b,cam_c,player_head)
            clipped_tris = clip3D(view_tri,near)

            num_tris = len(clipped_tris)


            # if tri_idx < 1000 :
            #     print(clipped_tris)
            #     print(clipped_tris.reshape(-1))
            #     print("NUM TRIS: " , num_tris)
            #     # print("______________________")
            
            res_AC_3D_buff[res_buff_idx: res_buff_idx + 9*num_tris] =  clipped_tris.reshape(-1) 

            # if tri_idx < 1000:
            #     print("res_buff_idx: ", res_buff_idx)
            #     print("______________________")
 


            # for i in range(9*num_tris):
            #     res_AC_3D_buff[res_buff_idx+i] = clipped_tris.reshape(-1)[i]
                      
            #print("RES BUFF: ", res_AC_3D_buff[res_buff_idx: res_buff_idx + 9*num_tris] )
            res_buff_idx =  res_buff_idx + 9*num_tris
            # bc_buff_idx += 9 
            #print("_________________")


            if tri_idx == inspect:
                inspect_tri = clipped_tris
                num_tris_ins = num_tris
            
                
        if isinstance(inspect,int):          
            print("INPUT TRI: \n" , BC_3D_buff[inspect:inspect+9].reshape(3,3))
            print("\n")
            print("CLIIPED TRIs: \n",res_AC_3D_buff[inspect:inspect+9*num_tris_ins].reshape(num_tris_ins,3,3))       
            print("\n")
            print(res_AC_3D_buff[inspect])
            

        for i in range(len_3D_ac):
            if abs(AC_3D_buff[i]-res_AC_3D_buff[i]) > eps:
                print("Incorrect at index: ", i)
                print("AC 3D             : ", AC_3D_buff[i]     )
                print("Res_AC_3D_Buff    : ", res_AC_3D_buff[i]  )

                print(AC_3D_buff)        
                print(res_AC_3D_buff)

                print("____________________________")    
                return

        


        print("PASSED AC 3D test!!!!!!!")


        

    # test_VC_3D()

    # test_AC_3D()

    #inp = np.array([[ 0.9576518,  -0.35874133,  1.67421825,], [ 0.9673776,  -0.34976948,  1.65103526],[ 0.98,       -0.50318586,  1.60287367]])

    inp = np.array([[0,0,0],[1,1.9,1],[2,3,2]]) 
    

    tensor = np.empty(shape=(1,3,3),dtype=np.float64)

    vec = np.array([1,2,3],dtype=np.float64)
    cam_a       = np.array([1.0, 0.0, 0.0])
    cam_b       = np.array([0.0, 1.0, 0.0])
    cam_c       = np.array([0  , 0.0, 1.0])
    player_head = np.array([0  ,-2.0, 0.0])


    q = 10 / (10-1)
    perspectiveProj(vec,90.0,q,1)


    # populateTriTensor(tensor,inp,0)

    # print(tensor)
    # print(clip3D(inp,1.0))


    #print(clip3D(np.array([0,0,0,1,1,1,2,3,2],dtype=np.float64),1.0))




















# print(len_3D_bc,len_3D_vc)



# with open("AC_3D.txt") as fp:
#     AC3DText = [line.rstrip() for line in fp]

# with open("BC_3D.txt") as fp:
#     BC3DText = [line.rstrip() for line in fp]

