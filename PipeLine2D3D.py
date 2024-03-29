import Pipline2D as p2d
import Pipline3D as p3d
from Utils import utils as ut
import numpy as np
from numba import njit
import math as m
import sys 




# def Pipeline(tri:Tris3D,a:Vec3D,b:Vec3D,c:Vec3D,player_head:Vec3D,near:float,lighting:bool,wireFrame:bool,window:GraphWin,tan_fov,q,drawn_tri):
"""
    tri: A 3 by 3 matrix that is your triangle

    RET:
        A  'n' by 3 by 2 numpy array that will hold all 2D tirangles
"""




n =0  


test_all = "testAll" in sys.argv

@njit
def getMidPoi(tri:np.ndarray):

    sum_vec = np.zeros(3,dtype=np.float64)
    for i in range(3):
        sum_vec += tri[i]

    return sum_vec /  3

@njit
def PipeLine3D(tri:np.ndarray, a:np.ndarray,b:np.ndarray,c:np.ndarray,
            player_head:np.ndarray,near:float,q:float,tan_fov:float, 
            zbuff2D_bc:np.ndarray,uvTris:np.ndarray,uvTrisResBuff3D_AC:np.ndarray,tri_idx:int,cullFace:bool):

    # return np.empty(shape=(0,3,2),dtype=np.float64)

    # if(tri.norm.dotProd(player_head.subVec(tri.midPoi()).normalizeVec())< 0 and not(parse_3d_tris ) and not(parse_2d_tris)):
    #     return

   
    norm_tri = p3d.getNorm(tri)

    

    ph_sub_mid_poi = np.subtract(player_head,getMidPoi(tri)  )


    #ph_sub_mid_poi_normalized = p3d.norm(ph_sub_mid_poi)

    if (cullFace) and p3d.dotProd3(norm_tri,ph_sub_mid_poi)  < 0 :
        return np.empty(shape=(0,3,2),dtype=np.float64)


    #print(player_head)






    view_tri   = p3d.viewTri(tri,a,b,c,player_head)






    # if n== 0 :
    #     print(view_tri)
    # else:

    #     n = 1
    z_buff_start_idx = zbuff2D_bc[-1] 
    uvTrisResBuff3D_AC_Intrim = np.zeros(shape=(2,3,2),dtype=np.float64)

    uvTri = uvTris[int(tri_idx)]
    tri_clipped_3D = p3d.clip3D(view_tri,uvTri,uvTrisResBuff3D_AC_Intrim,near)

    res_buff  = np.empty(shape=(len(tri_clipped_3D),3,2),dtype=np.float64)

    res_idx = 0  



    for tri_c in tri_clipped_3D:

        z_buff_idx = int(3*(z_buff_start_idx +  res_idx))


        """
            Recall that each point in the 
            triangle is of the form (x,y,z) in this order


            Note that we are not using the most sensible
            coordinate system. In this case we want to actually use 
            the y value of the point as our depth value as the camera 
            is assumed to be looking along the postive y axis, once the 
            triangles are put in view space.
        """
        
        # zbuff2D_bc[z_buff_idx + 0 ] = q - near*q/tri_c[0][1] 
        # zbuff2D_bc[z_buff_idx + 1 ] = q - near*q/tri_c[1][1] 
        # zbuff2D_bc[z_buff_idx + 2 ] = q - near*q/tri_c[2][1] 

        zbuff2D_bc[z_buff_idx + 0 ] = 1/tri_c[0][1] 
        zbuff2D_bc[z_buff_idx + 1 ] = 1/tri_c[1][1] 
        zbuff2D_bc[z_buff_idx + 2 ] = 1/tri_c[2][1] 


        uvTrisResBuff3D_AC[int(z_buff_start_idx + res_idx)] = uvTrisResBuff3D_AC_Intrim[int(res_idx)]

        

        
        tri2D = p3d.projTri(tri_c,tan_fov,q,near)


        # if n == 0:
        #     print(tri_c)
        #     print(tri2D)
        

        # n+=1 
        res_buff[res_idx] = tri2D
       
        
        res_idx +=1 

   
    zbuff2D_bc[-1] += res_idx
    return res_buff




"""
    Lst_tri: A 'n' by 3 by 3 matrix that is a list of the 3d Trignales

    RET:
            A flat numpy array object that will contain a list of 2d trianlges
        where the last elemnent in the list will be the number of 2D 
        triangles within the list. Its important to note that you  should be 
        able to figure out the size of the returned result buffer. The size
        of the result will always be  2*'num_tris'*16*3*2 + 1 where 
        'num_tris'  is the number of triangles within 'Lst_tri'. Each triangle
        within the Lst_tri is a 3D triangle  that can be broken into two 3D 
        triangles due to the clipping with the near plane. Each 3D trianlge is 
        projected into a 2D triangles. That 2D trianlge is then clipped against the edges of
        the screen. Since there a 4 screen edges and at most each tri can 
        be split up into two tris, at most there is 2^4 or 16 2D triangles. 
        Note the '+1'  in   2*'num_tris'*16*3*2 + 1  is where the number of 2D 
        triangles will be put.  
"""
@njit
def RunPipeLines(Lst_tri:np.ndarray, a:np.ndarray,b:np.ndarray,c:np.ndarray,
                player_head:np.ndarray,near:float,q:float,tan_fov:float, 
                zbuff2D_bc:np.ndarray,zbuff2D_ac:np.ndarray,uvTris:np.ndarray,uvTrisResBuff2D_AC:np.ndarray,
                cullFace:bool):
    global n 
    num_tris    = len(Lst_tri)
    res_buff_2d = np.empty(shape=(2*num_tris,3,2),dtype=np.longdouble)
    res_buff_2d_ac = np.empty(shape=(2*num_tris*16*3*2 + 1 ),dtype=np.longdouble)
    
    uvTrisResBuff3D_BC  = np.empty(shape=(2*num_tris,3,2),dtype=np.longdouble)
    

    res_buff_idx = 0 

    tri3D_idx = 0     
    for tri in Lst_tri:
        lst_2D_tris = PipeLine3D(tri,a,b,c,player_head,near,q,tan_fov,zbuff2D_bc,uvTris,uvTrisResBuff3D_BC,tri3D_idx,cullFace)
        num_2D_tris = len(lst_2D_tris)
        res_buff_2d[res_buff_idx:res_buff_idx + num_2D_tris] = lst_2D_tris
        res_buff_idx += num_2D_tris
        tri3D_idx += 1 

    #print("res buff idx: ", res_buff_idx)



    #print(zbuff2D_bc[0:3*res_buff_idx])


    if test_all:
        for i in range(res_buff_idx):
            tri2DFlat = res_buff_2d[i].reshape(-1)
            for cord in range(6):
                if abs(tri2DFlat[cord] - p2d.bc_arr[6*i + cord]) > 0.0001 and test_all:
                    print("ERR: ", i)
                    print("p2d.bc_arr: ", p2d.bc_arr[6*i + cord] )
                    print("res_buff_2d: ", tri2DFlat[cord])
                    print("BC ERROR!!!!")
                    return



    res_buff_2d_ac_idx = 0 
    tot_num_2D_tris = 0 
    for idx in  range (res_buff_idx):
        tri = res_buff_2d[idx]
        clipped_tri = p2d.clip2D(tri.reshape(-1),idx,zbuff2D_bc,zbuff2D_ac,uvTrisResBuff3D_BC[idx],uvTrisResBuff2D_AC)
        num_2D_tris = int(clipped_tri[-1   ])
        res_buff_2d_ac[res_buff_2d_ac_idx: res_buff_2d_ac_idx + 6*num_2D_tris] = clipped_tri[0:6*num_2D_tris]
        if n < -1 and test_all:
            print("2D TRIS: \n", tri.reshape(-1))
            print("Clipped Tri:\n",clipped_tri)
            print("NUM 2D tris: " , num_2D_tris)
            print("RES BUFF: \n",res_buff_2d_ac[res_buff_2d_ac_idx: res_buff_2d_ac_idx + 6*num_2D_tris])
            print("______________________")
        res_buff_2d_ac_idx+= 6*num_2D_tris
        tot_num_2D_tris+= num_2D_tris

    res_buff_2d_ac[2*num_tris*16*3*2] = tot_num_2D_tris
    return res_buff_2d_ac


if __name__ == "__main__" :

    def testPipeLine(eps=0.0001):
        BC3D_Arr = p3d.BC_3D_buff
        BC_Tri_Arr = BC3D_Arr.reshape((p3d.len_3D_bc,3,3))
        cam_a       = np.array([1.0, 0.0, 0.0])
        cam_b       = np.array([0.0, 1.0, 0.0])
        cam_c       = np.array([0  , 0.0, 1.0])
        player_head = np.array([0  ,-2.0, 0.0])



        print(BC_Tri_Arr[0])
        ac_arr = RunPipeLines(BC_Tri_Arr,cam_a,cam_b,cam_c,player_head,1.0,10/(10-1),1.0)
        tot    = 0 
        wrong  = False

        print("Nuum 2d tRIS IN AC ARR: " ,ac_arr[2*len(BC_Tri_Arr)*16*3*2])

        print(ac_arr)
        for i in range (6*int(ac_arr[2*len(BC_Tri_Arr)*16*3*2])):

            if abs(p2d.ac_arr[i] - ac_arr[i])  > eps:
                print("INCORRECT AT INDEX: ", i)
                print("AC_ARR            : ",ac_arr[i]  )
                print("p2d.ac_arr        : ",p2d.ac_arr[i]  )
                wrong = True


                tot+=1
                return
        if not(wrong):
            print("PASSED 3D to 2D test !!!!!!!")
        else:
            print("NUM WRONG: ", tot)


    def testOneTri(tri:np.ndarray,a:np.ndarray,b:np.ndarray,c:np.ndarray,player_head:np.ndarray,near:float,q:float,tan_fov:float):

        print(tri)
        tri2D = PipeLine3D(tri,a,b,c,player_head,near,q,tan_fov)


        clipped_tri2D = p2d.clip2D(tri2D.reshape(-1))

        print(clipped_tri2D)

    #     0.9576517999999999
    # -0.3587413287356612
    # 1.6742182524068334
    # 0.9673776
    # -0.34976948176601863
    # 1.651035261606393
    # 0.9799999999999999
    # -0.5031858631892998
    # 1.6028736653543345




    tri3D = np.array([ 
    0.9576517999999999,
    -0.3587413287356612,
    1.6742182524068334,
    0.9673776,
    -0.34976948176601863,
    1.651035261606393,
    0.9799999999999999,
    -0.5031858631892998,
    1.6028736653543345]).reshape(3,3)

    cam_a       = np.array([1.0, 0.0, 0.0])
    cam_b       = np.array([0.0, 1.0, 0.0])
    cam_c       = np.array([0  , 0.0, 1.0])
    player_head = np.array([0  ,-2.0, 0.0])


    #testOneTri(tri3D,cam_a,cam_b,cam_c,player_head,1.0,10/(10-1),1.0)





    testPipeLine()

    








        




