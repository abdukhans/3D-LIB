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
global calc
calc = 0 

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

p = -2
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
#lst_tris = [tri6]
# cube     = Mesh(lst_tris)
cube     = Mesh([],file_path="teapot.obj")



#cube.move(Vec3D(0,0,0))
cube.scale(0.7)
cube.rotateX_(-90)
cam      = Camera(player,norm_vec,b1,b2,win,near=1,fov=90)





"""
mesh_cube =[Vec3D(1,1+4,1)    ,Vec3D(1,1+4,-1),
             Vec3D(1,-1+4,-1),  Vec3D(1,-1+4,1),
            Vec3D(-1,1+4,1)   ,Vec3D(-1,1+4,-1),
            Vec3D(-1,-1+4,-1) ,Vec3D(-1,-1+4,1) ]
"""

def main():
    i = 0
    step = 0.1/1.3
    rot = 0.001
    
    #print(Vec3D(-1,-1,1).SDistFromPlane(Vec3D(0,1,0),Vec3D(0,-3,0)))

    profileMode = True if 'p' in sys.argv else False
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
            
        i += 1
        x,y,z = -1,1,3
        ang = 0.001
        

        """cube.rotateX_(0*ang)
        cube.rotateZ_(ang)
        cube.rotateY_(0*ang)"""
        
       
        
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


        if profileMode:
            with cProfile.Profile() as pr:
                cam.drawMesh(cube,wireFrame=False,lighting=True)
            break
        else:
            cam.drawMesh(cube,wireFrame=False,lighting=True)

        if parse_2d_tris or parse_3d_tris:
            break

        #cube.move(Vec3D(-x,-y,-z))


        #cam.printPlayer()

        update(60)

       

       
        cam.undrawMesh(cube)
        end = t.default_timer()
        print("FPS: ",str(1/(end - start)), end='\r')
    
    if profileMode:
        stats = pstats.Stats(pr)
        """numpFast2.inspect_types()    
        numpFast3.inspect_types()
        dotProd.inspect_types()    
        get_len.inspect_types()"""
        stats.sort_stats(pstats.SortKey.TIME)
        stats.reverse_order()
        stats.print_stats()

    
    win.close()


if __name__ == "__main__":
    main()
    
      

    