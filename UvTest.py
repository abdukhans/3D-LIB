import pstats
from graphics import *
import math as m
import numpy as np
import win32api
import timeit as t 
import time as ti
import multi as mi
import threading as th
#from numba import jit , cuda 
import cProfile 
import sys
import PipeLine2D3D as p3D2D 
from functools import cache
from Vec3D import Vec3D 
from Vec2D import Vec2D
from Tri2D import Tris2D
from Tri3D import Tris3D
from Utils import utils as ut
from Mesh import Mesh
from Camera import Camera, parse_2d_tris,parse_3d_tris 
import pygame as pg
import os
use_numpy = 'nump' in sys.argv
use_pygame = 'pygame' in sys.argv
use_numpy = True
use_pygame = True
global calc
calc = 0 
global n
n =  0 
height = 800
width  = 800 


# if not(use_pygame):
#     win    = GraphWin("Lib", height=height ,width= width,autoflush=False)
#     win.setBackground("black")
#     win.setCoords(-1,-1,1,1)
# else:
#     win = None



near = 1
m_z = -3

p = -2
player   = Vec3D(0,0,0)
norm_vec = Vec3D(0,-1,0)
b1       = Vec3D(1,0,0)
b2       = Vec3D(0,0,1)
v1       = Vec3D(1,1,2) 
v2       = Vec3D(1,1,-1)
v3       = Vec3D(1,-1,-1)
v4       = Vec3D(1,-1,1)
v5       = Vec3D(-1,1,1) 
v6       = Vec3D(-1,1,-1)
v7       = Vec3D(-1,-1,1)
v8       = Vec3D(-1,-1,-1)
v9       = Vec3D(-0.9,-1.5,-1)
v10      = Vec3D(0,-2,-1)
v11      = Vec3D(0,4,1)
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
tri14    = Tris3D(v9,v10,v11,col="red")
lst_tris = [tri1,tri2,tri3, tri4,tri5,tri6,tri7,tri8,tri9,tri10,tri11,tri12]
lst_tris = [tri6,tri14]
# cube     = Mesh(lst_tris)
# cube.move(Vec3D(0,2,0))
# cube.createNumpObjFromVerts()

cottage_string = "C:/Users/abdul/OneDrive/Documents/CODING HOBBIES/3D Lib Py/ObjFolder/cottage_obj.obj"
video_ship     = "C:/Users/abdul/OneDrive/Documents/CODING HOBBIES/3D Lib Py/ObjFolder/VideoShip.obj"
axis           = "C:/Users/abdul/OneDrive/Documents/CODING HOBBIES/3D Lib Py/ObjFolder/Axis.obj"
Mountain       = "C:/Users/abdul/OneDrive/Documents/CODING HOBBIES/3D Lib Py/ObjFolder/Mountain.obj"
teapot         = "teapot.obj"
zDepthTest     = "C:/Users/abdul/OneDrive/Documents/CODING HOBBIES/3D Lib Py/ObjFolder/Test_obj.obj" 
shpere_obj     = "C:/Users/abdul/OneDrive/Documents/CODING HOBBIES/3D Lib Py/ObjFolder/Sphere.obj" 
cube_obj       = "C:/Users/abdul/OneDrive/Documents/CODING HOBBIES/3D Lib Py/ObjFolder/Cube.obj" 
test_raster    = "C:/Users/abdul/OneDrive/Documents/CODING HOBBIES/3D Lib Py/ObjFolder/TestRaster.obj" 
test_raster2   = "C:/Users/abdul/OneDrive/Documents/CODING HOBBIES/3D Lib Py/ObjFolder/Test2Raster.obj"

cottage_text   = "C:/Users/abdul/OneDrive/Documents/CODING HOBBIES/3D Lib Py/34-cottage_textures/cottage_textures/cottage_diffuse.png" 
test_png       = "test.png"

cube           = Mesh([],file_path=cottage_string,texturePath=cottage_text,use_numpy=use_numpy)

cube.getTri(108)

cube.rotateNumpX(90)
cube.rotateNumpZ(-90)



# cube.move(Vec3D(0,0,0))
# cube.scale(0.2)
# cube.rotateX_(-90)

# Player head:  VEC 3D: ( 10.22822918990669 , -3.2413355319984967 , 9.199999999999985 )
# a          :  VEC 3D: ( 0.9414891461705163 , 0.3370433023264332 , 0 )
# b          :  VEC 3D: ( -0.3370433023264332 , 0.9414891461705163 , 0 )
# c          :  VEC 3D: ( 0.0 , 0.0 , 1 )
pixelArr = np.zeros(shape=(width*height*3),dtype=np.uint8)
cam      = Camera(player,norm_vec,b1,b2,height=height,width=width,near=1,far=80,fov=90,usePygame=use_pygame,pixelArray=pixelArr)


cam.player_head = Vec3D( 10.22822918990669 , -3.2413355319984967 , 9.199999999999985 )
cam.a           = Vec3D( 0.9414891461705163 , 0.3370433023264332 , 0 ) 
cam.b           = Vec3D( -0.3370433023264332 , 0.9414891461705163 , 0 )
cam.c           = Vec3D( 0.0 , 0.0 , 1 )


# cam.forward(-30)
# cam.incrementZ(5)

def main():
    i = 0
    step = 0.1
    rot = 0.001
    
    #print(Vec3D(-1,-1,1).SDistFromPlane(Vec3D(0,1,0),Vec3D(0,-3,0)))

    profileMode = True if 'p' in sys.argv else False

    win = cam.window if not(cam.usePygame) else pg.display.set_mode((width,height))
    clock = pg.time.Clock()
 

    pos = Vec3D(1,0,4)
    while( True):
        start  = t.default_timer()
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


        # print( "Player head: ", cam.player_head )
        # print( "a          : ", cam.a )
        # print( "b          : ", cam.b)
        # print( "c          : ", cam.c )
        
        
        
            
        i += 1
        x,y,z = 1,1,3
        ang = 0.001

        # print(id(cam.player_head))
        # cam.player_head.add_z(0.0001)
        # print(id(cam.player_head))
        # cube.rotateX_(ang)
        # cube.move(-1*pos)
        

        #time.sleep(1)
        # cube.rotateY_(ang)
        # pos+= Vec3D(x/100,y/100,0)
        # cube.move(pos)
        if profileMode:
            with cProfile.Profile() as pr:
                cam.drawMesh(cube,wireFrame=False,lighting=True)
            
        else:
            cam.drawMesh(cube,wireFrame=False,lighting=True,FillCol=True,cullFace=False)
      
        if parse_2d_tris or parse_3d_tris:
            break

        
        #cube.move(Vec3D(-x,-y,-z))


        #cam.printPlayer()
        # if n ==0:
        #     print(len(cam.drawn_tri),"/n")
        
        
        # print(f"Player head: {cam.player_head}a          : {cam.a}b          : {cam.b}c          : {cam.c}" ,end='\r', flush=True)

        
        if not(use_pygame):
            update(60)

        else:

            
            # win.fill((0,0,0))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                   pg.quit()
                   exit(0)
        

            surf = pg.image.frombuffer(cam.pixelArray,(width,height),"RGB")
            win.blit(surf,(0,0))
            pg.display.update()
            clock.tick(60)
            
        # n+= 1

     



       

       
        cam.undrawMesh(cube)
        end = t.default_timer()
        fps ="FPS: " + str(1/(end - start))

        # os.system('cls')




        

        # print(f"Player head: {cam.player_head}" ,end='\r', flush=True)
        if not(use_pygame):
            win.master.title(fps)
        else:
            pg.display.set_caption(fps)
        


    if profileMode:
        stats = pstats.Stats(pr)
        """
        numpFast2.inspect_types()    
        numpFast3.inspect_types()
        dotProd.inspect_types()    
        get_len.inspect_types()
        """
        stats.sort_stats(pstats.SortKey.TIME)
        stats.reverse_order()
        stats.print_stats()

     
    if isinstance(win,GraphWin):
        win.close()


if __name__ == "__main__":
    main()
    
      

    """cube.rotateX_(0*ang)
        cube.rotateZ_(ang)
        cube.rotateY_(0*ang)
"""
        
       
        
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
#cube.move(Vec3D(x,y,z))