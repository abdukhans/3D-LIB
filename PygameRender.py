import pygame as pg 
from sys import exit
import numpy as np
from numba import njit

from Utils import utils as ut 
import Textures as tx
import random as r


@njit
def revLst(lst:np.ndarray):
    

    shape = lst.shape
    res_buff = np.zeros(shape=shape,dtype=np.int32)

    len_ = len(lst)
    for i in range(len_):
        res_buff[len_ - i - 1 ] = lst[i]
    return res_buff


@njit
def SlopeCorrectionX(x1:int, y1:int, x2:int,y2:int, res_buf:np.ndarray, step_Pos:bool  ):

    res_idx = 0 
    cur_x = x1
    cur_y = y1
    slope_error = 0

    dx = x2 - x1
    dy = y2 - y1
    slope = dy/dx

    threshold = 0.5 if step_Pos else -0.5


   
    for x in range(dx+1):
        res_buf[res_idx][0] = cur_x
        res_buf[res_idx][1] = cur_y
        res_idx +=1
        
        cur_x += 1        
        
        slope_error += slope

        if step_Pos:
            if slope_error >= threshold:
                cur_y +=1
                slope_error-=1
        else:
            if slope_error < threshold:
                cur_y -=1
                slope_error+=1






@njit
def SlopeCorrectionY(x1:int, y1:int, x2:int,y2:int, res_buf:np.ndarray, step_Pos:bool  ):

    res_idx = 0 
    cur_x = x1
    cur_y = y1
    slope_error = 0

    dx = x2 - x1
    dy = y2 - y1
    slope = dx/dy

    threshold = 0.5 if step_Pos else -0.5


   
    for x in range(dy+1):
        res_buf[res_idx][0] = cur_x
        res_buf[res_idx][1] = cur_y
        res_idx +=1
        
        cur_y += 1        
        
        slope_error += slope

        if step_Pos:
            if slope_error >= threshold:
                cur_x +=1
                slope_error-=1
        else:
            if slope_error < threshold:
                cur_x -=1
                slope_error+=1




@njit
def Bresenham(x1:int,y1:int,x2:int,y2:int) -> np.ndarray:

        

    dy = y2 - y1
    dx = x2 - x1

    rev = False

    
  
    if dx == 0 :
        if dy != 0 :
            if y1 > y2:
                x1,x2 = x2,x1
                y1,y2 = y2,y1
                dx = x2 - x1 
                dy = y2 - y1

                rev = True
            res_buf = np.empty(shape=(dy + 1, 2),dtype=np.int32)

            SlopeCorrectionY(x1,y1,x2,y2,res_buf,True)
            return res_buf

        

        else:
            res_buf = np.empty(shape=(dy + 1, 2),dtype=np.int32)

            res_buf[0][0] = x1
            res_buf[0][1] = y1
            return res_buf





    slope = dy/dx


    #print("SLOasdPE: ", slope)
    if slope >= 0 :

        if slope <=1:
            #print("x1: ", x1, 'x2: ' ,x2, "dx: " , dx)
            if x1 > x2:
                x1,x2 = x2,x1
                y1,y2 = y2,y1
                dx = x2 - x1 
                dy = y2 - y1
                rev = True


            res_buf = np.empty(shape=(dx+1,2),dtype=np.int32)
            SlopeCorrectionX(x1,y1,x2,y2,res_buf,True)
            if rev:
                return revLst(res_buf) 
            return res_buf
        else:
            if y1 > y2:
                x1,x2 = x2,x1
                y1,y2 = y2,y1
                dx = x2 - x1 
                dy = y2 - y1
                rev = True

            res_buf = np.empty(shape=(dy+1,2),dtype=np.int32)
            SlopeCorrectionY(x1,y1,x2,y2,res_buf,True)
            if rev:
                return revLst(res_buf)  

            return res_buf
    elif slope < 0:
        if slope >= -1:
            if x1 > x2:
                x1,x2 = x2,x1
                y1,y2 = y2,y1
                dx = x2 - x1 
                dy = y2 - y1
                rev = True
            res_buf = np.empty(shape=(dx+1,2),dtype=np.int32)
            SlopeCorrectionX(x1,y1,x2,y2,res_buf,False)   
            if rev:
                return revLst(res_buf)        
            return res_buf
        else:
            if y1 > y2:
                x1,x2 = x2,x1
                y1,y2 = y2,y1
                dx = x2 - x1 
                dy = y2 - y1
                rev = True
            res_buf = np.empty(shape=(dy+1,2),dtype=np.int32)
            SlopeCorrectionY(x1,y1,x2,y2,res_buf,False) 

            if rev:
                return revLst(res_buf)         
            return res_buf


    return np.empty(shape=(0,2),dtype=np.int32)


print(Bresenham(3,2,15,5))
print(Bresenham(15,5,3,2))
# print(Bresenham(0,0,4,2))

@njit
def lerp(a:float,b:float,t:float):
    return (1-t)*a + t*b


@njit
def clear(pixelArray:np.ndarray, size:int, val=0):
    for i in range(size):
        pixelArray[i] = val



    
    pass




"""
    #NOTE The coords should be nomalized i.e between -1 and 1.
    Note that the point (0,0) is going to be in the middle of the 
    srceen
    x1: 
    y1:

    x2:
    y2:


    pixelArr: This is a flattend numpy array, and is 
              thought to be a pixel array buffer.
              Even though you put this as a flat array 
              keep in mind that you use it as a 2D array
              where each entry is a pixel defined by an
              3 unit8 values that define the RGB coords 
              respectively.  

    width: the width of the screen in pixels
    height: the height of the screen in pixels
"""

@njit
def drawLine(x1,y1,x2,y2,pixelArr,width, height,R=255,G=255,B=255,debug=False):

    sx1 = int (lerp(0,width, (x1 + 1) /2 ))  
    sy1 = int (lerp(height,0, (y1 + 1) /2 ))

    sx2 = int (lerp(0,width,  (x2 + 1) /2 ))  
    sy2 = int (lerp(height,0, (y2 + 1) /2 ))

    # print(sx1,sy1)
    # print(sx2,sy2)


    dy = sy2 - sy1
    dx = sx2 - sx1 


   


    lst = Bresenham(sx1,sy1,sx2,sy2)

    if debug:

        slope = dy/dx if dx !=0  else 999999

        print("SLOPE:" , slope)
        print(lst)


    
    for cord in lst:
        width_cord = cord[0]
        height_cord = cord[1]

        pixelArr[ height_cord*3*width +  3*width_cord + 0 ] = R
        pixelArr[ height_cord*3*width +  3*width_cord + 1 ] = G
        pixelArr[ height_cord*3*width +  3*width_cord + 2 ] = B




@njit
def drawLineZbuff(x1,y1,x2,y2,pixelArr,width, height,z1:float,z2:float,depthBuffer:np.ndarray,R=255,G=255,B=255,debug=False):

    sx1 = x1
    sy1 = y1

    sx2 = x2
    sy2 = y2

    # print(sx1,sy1)
    # print(sx2,sy2)


    dy = sy2 - sy1
    dx = sx2 - sx1 


   


    lst = Bresenham(sx1,sy1,sx2,sy2)

    # if debug:

    #     slope = dy/dx if dx !=0  else 999999

    #     print("SLOPE:" , slope)
    #     print(lst)



    t = 0 
    # num_pix = len(lst) - 1 if len(lst) > 1 else 1  
    num_pix = len(lst)  
    t_step = 1 / num_pix  
    for cord_idx in range(num_pix):

        cord= lst[cord_idx]
        
        cur_z = lerp(z1,z2,t)

        width_cord = cord[0]
        height_cord = cord[1]
        change  =  1
        lightD = 1


        if (depthBuffer[height_cord][width_cord] > 0 and debug):

            print("z1           :" ,  z1)
            print("z2           :" ,  z2)
            print("cz           :" ,  cur_z)
            print(f"DB[{height_cord}][{width_cord}] :", depthBuffer[height_cord][width_cord])
            print("t            :", t)
            print("_________________________________")



        #print("z1: " , z1, "\nz2: " , z2,"\ncur_z: ",cur_z , "\ndepthBuffer[height_cord][width_cord]: ",depthBuffer[height_cord][width_cord]  )

        # print("cur_z     " , cur_z)
        # print("depthBuff: " , depthBuffer[height_cord][width_cord] )
        # abs( cur_z - depthBuffer[height_cord][width_cord]) < 0.001*cur_z or
        if cur_z >= depthBuffer[height_cord][width_cord] - lerp(0.0,0.009,cur_z)   :

            a = depthBuffer[height_cord][width_cord]


            

                #print("z1: " , z1, "\nz2: " , z2,"\ncur_z: ",cur_z , "\ndepthBuffer[height_cord][width_cord]: ",depthBuffer[height_cord][width_cord]  )

            #print("z1: " , z1, "\nz2: " , z2,"\ncur_z: ",cur_z , "\n" )
            

            # if abs( cur_z - depthBuffer[height_cord][width_cord]) < 0.00001*cur_z :
            #     pixelArr[ height_cord*3*width +  3*width_cord + 0 ] = R
            #     pixelArr[ height_cord*3*width +  3*width_cord + 1 ] = G
            #     pixelArr[ height_cord*3*width +  3*width_cord + 2 ] = B
            # else:
            #     # if cur_z < 0.015:
            #     #     print(cur_z)
            #     #     print(depthBuffer[height_cord][width_cord] )
                
            #     pixelArr[ height_cord*3*width +  3*width_cord + 0 ] = 0
            #     pixelArr[ height_cord*3*width +  3*width_cord + 1 ] = 255
            #     pixelArr[ height_cord*3*width +  3*width_cord + 2 ] = 0
            #     depthBuffer[height_cord][width_cord] = cur_z

           
            # change = lerp(0,1,cur_z)

            # pixelArr[ height_cord*3*width +  3*width_cord  + 0 ] = int(R*1/(cur_z+ 1)*lightD)
            # pixelArr[ height_cord*3*width +  3*width_cord  + 1 ] = int(G*1/(cur_z+ 1)*lightD)
            # pixelArr[ height_cord*3*width +  3*width_cord  + 2 ] = int(B*1/(cur_z+ 1)*lightD) 
            pixelArr[ height_cord*3*width +  3*width_cord  + 0 ] = int(R)
            pixelArr[ height_cord*3*width +  3*width_cord  + 1 ] = int(G)
            pixelArr[ height_cord*3*width +  3*width_cord  + 2 ] = int(B) 
            depthBuffer[height_cord][width_cord] = cur_z
            

            # depthBuffer[height_cord][width_cord] = cur_z
            # if cur_z > depthBuffer[height_cord][width_cord]:
            #     depthBuffer[height_cord][width_cord] = cur_z
            # else:
            #     depthBuffer[height_cord][width_cord] = cur_z - 0.001



        t = cord_idx*t_step 


@njit
def drawLineZbuff2(x1,y1,x2,y2,pixelArr,width, height,z1:float,z2:float,depthBuffer:np.ndarray,R=255,G=255,B=255,debug=False):

    sx1 = x1
    sy1 = y1

    sx2 = x2
    sy2 = y2

    # print(sx1,sy1)
    # print(sx2,sy2)


    dy = sy2 - sy1
    dx = sx2 - sx1 


   


    lst = Bresenham(sx1,sy1,sx2,sy2)

  

    t = 0 

    num_pix = len(lst)  


    t_step = 1 / (dy + 1 ) 
    i = 0  
    for _ in range(dy + 1 ):
        
        cur_z = lerp(z1,z2,t)

   
        
        height_cord = lst[i][1]
        change  =  1
        lightD = 1

        same_y_ind = 0 

        while (i + same_y_ind) < num_pix:

            if  lst[i + same_y_ind][1] != height_cord:
                break

            width_cord = lst[i + same_y_ind][0]
            if cur_z <= depthBuffer[height_cord][width_cord]   :
            

                pixelArr[ height_cord*3*width +  3*width_cord  + 0 ] = int(R)
                pixelArr[ height_cord*3*width +  3*width_cord  + 1 ] = int(G)
                pixelArr[ height_cord*3*width +  3*width_cord  + 2 ] = int(B) 
                depthBuffer[height_cord][width_cord] = cur_z

            same_y_ind+= 1

        i += same_y_ind 

        
        t += t_step 




    



def TestX(pixelArr:np.ndarray,width,height):

    # OCT 1 
    drawLine(0,0,0.5,0.5,pixelArr,width,height,debug=True)
    drawLine(0,0,0.5,0.2,pixelArr,width,height,230,149,39)
    drawLine(-0.5,-0.3,0.8,0.1,pixelArr,width,height,255,159,139)

    #OCT 4
    drawLine(0.7,-0.2,-0.5,0.2,pixelArr,width,height,230,149,39)
    drawLine(-0.5,0.2,0.7,-0.2,pixelArr,width,height,100,0,0)


    #OCT 5
    drawLine(0,0,-0.5,-0.4,pixelArr,width,height,0,149,39)
    drawLine(-0.5,-0.4,0,0,pixelArr,width,height,0,0,255)
    drawLine(-0.5,-0.5,0,0,pixelArr,width,height,0,244,0)

    #OCT 8
    drawLine(0,0,0.5,-0.4,pixelArr,width,height,0,255,39)
    drawLine(0.5,-0.4,0,0,pixelArr,width,height,0,222,240)
    drawLine(0.5,-0.5,-1,1,pixelArr,width,height,0,180,240)

    #drawLine(-0.5,-0.4,0,0,pixelArr,width,height,0,0,255)
    #drawLine(-0.5,-0.5,0,0,pixelArr,width,height,0,244,0)
 
    pass



def TestEdgeCases(pixelArr:np.ndarray,width,height):


    #Vertical line test
    drawLine(0.1,0.7,0.1,0.2,pixelArr,width,height,0,0,255)

    #Horizontal line Test
    drawLine(-0.7,-0.132,0.2,-0.132,pixelArr,width,height,0,0,255)






de_bug = False
@njit
def DrawTris(Lst_tri:np.ndarray, pixelArr:np.ndarray,width:int,height:int , 
             num_tris:int,trianglZbuff:np.ndarray,depthBuffer:np.ndarray,
             uvTexCords:np.ndarray,textBuff:np.ndarray,q:float,near:float,
             outLine=True,FillCol=False,R=255,G=255,B=255):
    tri_idx = 0 

    
    use_tex       = len(uvTexCords) > 0 
    use_text_cols = len(textBuff  ) > 0

    shape = textBuff.shape
    text_height = shape[0]  
    text_width  = shape[1]

    while tri_idx <    num_tris:
        tri_point_idx = 6*tri_idx
        p1  = Lst_tri[tri_point_idx : tri_point_idx + 2 ]
        tri_point_idx +=2
        p2  = Lst_tri[tri_point_idx : tri_point_idx + 2 ]
        tri_point_idx +=2
        p3  = Lst_tri[tri_point_idx:  tri_point_idx + 2 ]


        if use_tex:
            uvTri = uvTexCords[tri_idx]
            uv1   = uvTri[0]
            uv2   = uvTri[1]
            uv3   = uvTri[2]


        






        # print("p1: ",p1)
        # print("p2: ",p2)
        # print("p3: ",p3)



        p1x = p1[0]
        p1y = p1[1]

        p2x = p2[0]
        p2y = p2[1]

        p3x = p3[0]
        p3y = p3[1]

        s1x = int(lerp(0,width - 1, (p1x+1)/2))
        s1y = int(lerp(height - 1,0, (p1y+1)/2))
        s1z = trianglZbuff[3*tri_idx  + 0 ]

        s2x = int(lerp(0,width - 1, (p2x+1)/2))
        s2y = int(lerp(height - 1,0, (p2y+1)/2))
        s2z = trianglZbuff[3*tri_idx  + 1 ]

        s3x = int( lerp(0,width - 1, (p3x+1)/2)  )
        s3y = int( lerp(height - 1,0, (p3y+1)/2 ))
        s3z = trianglZbuff[3*tri_idx  + 2 ]


        if s1y > s2y:
            s1x,s1y,s2x,s2y = s2x,s2y,s1x,s1y
            s1z,s2z =  s2z,s1z

            if use_tex:
                uv1,uv2 =  uv2,uv1    

        if s1y > s3y:
            s1x,s1y,s3x,s3y = s3x,s3y,s1x,s1y
            s3z,s1z =  s1z,s3z  

            if use_tex:
                uv1,uv3 =  uv3,uv1
        
        if s2y > s3y:
            s2x,s2y,s3x,s3y = s3x,s3y,s2x,s2y
            s2z,s3z =  s3z,s2z 

            if use_tex:
                uv2,uv3 =  uv3,uv2 

        

        eps = 0.00001
        # print("s1z: " , s1z )
        # print("s2z: " , s2z )
        # print("s3z: " , s3z )
        # print("-")
          

        if FillCol:
            
            
            # print("s1x: " , s1x )
            # print("s1y: " , s1y )
            # print("s2x: " , s2x )
            # print("s2y: " , s2y )
            # print("s3x: " , s3x ) 
            # print("s3y: " , s3y , "------------------------\n" )       

            dys2s1 =  s2y - s1y
            dxs2s1 =  s2x - s1x

            dys3s1 = s3y - s1y
            dxs3s1 = s3x - s1x
           
            dys3s2 = s3y - s2y
            dxs3s2 = s3x - s2x
           
           
            if use_tex:

                dus2s1 = uv2[0] - uv1[0]
                dvs2s1 = uv2[1] - uv1[1] 

                dus3s1 = uv3[0] - uv1[0]
                dvs3s1 = uv3[1] - uv1[1]
                
                dus3s2 = uv3[0] - uv2[0]
                dvs3s2 = uv3[1] - uv2[1]


                pass
                


            # TOP HALF: s1y -> s2y
            rev = False
            da = 0 
            db = 0 
            
            da_tex = np.array([0,0],dtype=np.float64) 
            db_tex = np.array([0,0],dtype=np.float64) 

            t_c_step_inrc =  1 / dys3s1 if  (dys3s1!=0 ) else 0 
            t_c = 0 

            # start_tex  = np.array([-1,-1],dtype=np.float64) 
            # end_tex    = np.array([-1,-1],dtype=np.float64) 
            if (dys2s1 != 0):
    
                if use_tex:
                    da_tex =      np.array([dus2s1/dys2s1, dvs2s1/dys2s1   ], dtype=np.float64 ) 
                    
                t_a_step_inrc = 1 / dys2s1
                t_a = 0 
                da = dxs2s1 /dys2s1

                if dys3s1 != 0 :
                    db = dxs3s1 / dys3s1
                    if use_tex:
                        db_tex = np.array([dus3s1/dys3s1, dvs3s1/dys3s1], dtype=np.float64 ) 

                for y in range(s1y,s2y+1,1):
                    start_x  =   (s1x + (y - s1y)*da)
                    end_x    =   (s1x + (y - s1y)*db)

                    if use_tex:
                        start_tex:np.ndarray    =   (uv1 + (y - s1y) * da_tex )
                        end_tex: np.ndarray     =   (uv1 + (y - s1y) * db_tex )

                        

                    
                    




                    start_z =  lerp(s1z,s2z,t_a)
                    end_z   =  lerp(s1z,s3z,t_c) 

                    if start_x > end_x:
                        start_x,end_x  = end_x , start_x
                        start_z,end_z  = end_z , start_z  
                        start_tex,end_tex = end_tex,start_tex 
                        rev = True

                    if y == s2y:
                        top_start_tex = start_tex
                        top_end_tex   = end_tex

                        top_start_z = start_z
                        top_end_z   = end_z




                    
                    start_x = int(round(start_x))
                    end_x   = int(round(end_x))
        
                    #drawLine(start_x,y,end_x,p3y,pixelArr,width,height,R,G,B)
                    dx_horz = int( round(end_x) - round(start_x))
                    t_a_step_horz_incr = 1 / (dx_horz ) if  (dx_horz !=0 ) else 0 
                    t_a_horz = 0 
                    for x in range(int(start_x),int(end_x+1)):
                        

                        cur_z = lerp(start_z , end_z, t_a_horz)
                        
                        cur_uv = ut.lerp(start_tex, end_tex , t_a_horz )

                        #print(1/cur_z)

                        # if abs(1 -t_a_horz ) < 0.000001 :
                        #     print("t_a_horz = " , t_a_horz)

                        if  cur_z > depthBuffer[y][x]  :

        
                            if use_tex and use_text_cols :
                                
                               
                                u = cur_uv[0] / cur_z   
                                v = cur_uv[1] / cur_z
                                #print(u,v) 

                                # if u < 0 or v < 0 :

                                #     print("\n")
                                #     print("start_tex: " , start_tex)
                                #     print("end_tex  : " , end_tex)
                                #     print("u: " , u)
                                #     print("v: " , v)
                                #     print("cu: ",cur_uv)
                                #     print("cz: ",cur_z)
                                #     print("t_ahorz: " , t_a_horz)
                                #     print("___")

                                test1 = u < 0 or v < 0  or u > 1 or v > 1
                                
                                
                                test2 = t_a_horz  - eps > 1
                                if False and test1:
                                    print("\n")
                                    print("start_tex    : " , start_tex)
                                    print("end_tex      : " , end_tex)
                                    print("u            : " , u)
                                    print("v            : " , v)
                                    print("cuv          : " , cur_uv)
                                    print("cz           : " , cur_z)
                                    print("t_ahorz      : " , t_a_horz)
                                    print("start_x      : " , start_x)
                                    print("end_x        : " , end_x)
                                    print("dx_horz      : " , dx_horz)
                                    print("t_ahorz_inc  : " , t_a_step_horz_incr)
                                    print("___")

                                # if v > 1 or u > 1:
                                #     print("u: " , u)
                                #     print("v: " , v)

                                x_t = int(round((u) * (text_width - 1)))
                                y_t = int(round((v - 1)*(1- text_height )))

                                if x_t >= text_width:
                                    x_t = text_width - 1
                                
                                if y_t >= text_height:
                                    y_t = text_height - 1
                               
                                    
                                pixelArr[width*3*y + 3*x + 0 : width*3*y + 3*x + 3   ] = textBuff[y_t][x_t]


                            else:
                                

                                pixelArr[width*3*y + 3*x + 0 ] = int(R)
                                pixelArr[width*3*y + 3*x + 1 ] = int(G)
                                pixelArr[width*3*y + 3*x + 2 ] = int(B)  
                
                            depthBuffer[y][x] = cur_z 

                            # if tri_idx == 1:
                            #     pixelArr[width*3*y + 3*x + 0 ] = int(0)
                            #     pixelArr[width*3*y + 3*x + 1 ] = int(0)
                            #     pixelArr[width*3*y + 3*x + 2 ] = int(B) 
                            # else:
                            #     pixelArr[width*3*y + 3*x + 0 ] = int(R)
                            #     pixelArr[width*3*y + 3*x + 1 ] = int(G)
                            #     pixelArr[width*3*y + 3*x + 2 ] = int(B) 



                            # if x == start_x or x == end_x:
                            #     pixelArr[width*3*y + 3*x + 0 ] = 0
                            #     pixelArr[width*3*y + 3*x + 1 ] = 0
                            #     pixelArr[width*3*y + 3*x + 2 ] = B


                        t_a_horz+=t_a_step_horz_incr

                    t_a += t_a_step_inrc
                   

                    if y != s2y:
                        t_c += t_c_step_inrc




            # if rev:
            #     top_start_tex = end_tex
            #     top_end_tex   = start_tex
            # else:
            #     top_start_tex = start_tex
            #     top_end_tex   = end_tex

            # rev = False
            # Bottom Half: s2y -> s3y

            da = 0 
            db = 0 

            
            if (dys3s2!=0):

                if use_tex:
                    da_tex =      np.array([dus3s2/dys3s2, dvs3s2/dys3s2   ], dtype=np.float64 ) 

                da = dxs3s2 / dys3s2

                if dys3s1!=0:
                    db = dxs3s1 / dys3s1
                    if use_tex:
                        db_tex = np.array([dus3s1/dys3s1, dvs3s1/dys3s1   ], dtype=np.float64 ) 

                

                t_b_step_inrc = 1 / dys3s2 if(dys3s2 != 0) else 0
                t_b = 0 


                for y in range(s2y,s3y+1,1):
                    start_x       =     (s2x + (y - s2y)*da)
                    end_x         =     (s1x + (y - s1y)*db)

                    start_z = lerp(s2z,s3z,t_b)
                    end_z =   lerp(s1z,s3z,t_c)


                    dy_2  = y - s2y
                    dy_1  = y - s1y 
                    if use_tex:
                        start_tex:np.ndarray    =   (uv2 + ((dy_2) * da_tex ))
                        end_tex: np.ndarray     =   (uv1 + ((dy_1) * db_tex ))

                    if start_x > end_x:
                        start_x,end_x = end_x , start_x
                        start_z,end_z  = end_z,start_z
                        start_tex,end_tex = end_tex, start_tex
                        rev = True
                    #drawLine(start_x,y,end_x,p3y,pixelArr,width,height,R,G,B)

                    if y == s2y:

                        if rev:
                            bottom_start_tex = end_tex
                            bottom_end_tex   = start_tex
                        else:
                            bottom_start_tex = start_tex
                            bottom_end_tex   = end_tex


                        if (dys2s1  > 0 ) and de_bug:    
                            if not( (ut.is_close(top_start_tex , bottom_start_tex))) and not((ut.is_close(top_end_tex , bottom_start_tex))):
                                print("top_start_tex     : " , top_start_tex)
                                print("top_end_tex       : " , top_end_tex)                            
                                print("bot_start_tex     : " , bottom_start_tex)
                                print("UV2               : " , uv2)
                                print("da_tex            : " , da_tex  )
                                print("dy_2              : " , dy_2  )
                                print("dy_2*da_tex       : " , dy_2*da_tex  )
                                print("uv2 + dy_2*da_tex : " , (uv2 + ((dy_2) * da_tex )))
                                print("tri_idx           : " , tri_idx )
                                print("_________________________________________")

                            

                    start_x = int(round(start_x))
                    end_x   = int(round(end_x))

                    dx_horz = int( round(end_x) - round(start_x))
                    t_b_step_horz_incr = 1 / (dx_horz) if  (dx_horz !=0 ) else 0 
                    t_b_horz  = 0 
                    for x in range(int(start_x),int(end_x+1)):

                        
                        cur_z = lerp(start_z , end_z, t_b_horz)

                        cur_uv = ut.lerp(start_tex, end_tex , t_b_horz )

                        # if abs(1 -t_b_horz ) < 0.000001 :
                        #     print("t_b_horz = " , t_b_horz)

                        #print(1/cur_z)
                        if  cur_z > depthBuffer[y][x]  :

                            


                            if use_tex and use_text_cols :
                                
                                # print("\n")
                                # print(cur_uv)
                                # print(cur_z)
                                u = cur_uv[0] / cur_z   
                                v = cur_uv[1] / cur_z
                                #print(u,v)

                        
                                test1 =  u < 0 or v < 0  or u > 1 or v > 1
                                test2 = t_b_horz - eps > 1

                                if False and test1:
                                    print("\n")
                                    print("start_tex    : " , start_tex)
                                    print("end_tex      : " , end_tex)
                                    print("u            : " , u)
                                    print("v            : " , v)
                                    print("cuv          : ",cur_uv)
                                    print("cz           : ",cur_z)
                                    print("t_bhorz      : " , t_b_horz)
                                    print("start_x      : " , start_x)
                                    print("end_x        : " , end_x)
                                    print("dx_horz      : " , dx_horz)
                                    print("t_bhorz_inc  : " , t_b_step_horz_incr)

                                    print("___")

                                # if v > 1 or u > 1:
                                #     print("u: " , u)
                                #     print("v: " , v)

                                x_t = int(round((u) * (text_width - 1)))
                                y_t = int(round((v - 1)*(1- text_height )))

                                if x_t >= text_width:
                                    x_t = text_width - 1
                                
                                if y_t >= text_height:
                                    y_t = text_height - 1
                               
                                    
                                pixelArr[width*3*y + 3*x + 0 : width*3*y + 3*x + 3   ] = textBuff[y_t][x_t]
                                col = textBuff[y_t][x_t]

                            else:
                                

                                pixelArr[width*3*y + 3*x + 0 ] = int(R)
                                pixelArr[width*3*y + 3*x + 1 ] = int(G)
                                pixelArr[width*3*y + 3*x + 2 ] = int(B)  

                            depthBuffer[y][x] = cur_z 

                            # if tri_idx == 1:
                            #     pixelArr[width*3*y + 3*x + 0 ] = int(R)
                            #     pixelArr[width*3*y + 3*x + 1 ] = int(0)
                            #     pixelArr[width*3*y + 3*x + 2 ] = int(0) 
                            # else:
                            #     pixelArr[width*3*y + 3*x + 0 ] = int(R)
                            #     pixelArr[width*3*y + 3*x + 1 ] = int(G)
                            #     pixelArr[width*3*y + 3*x + 2 ] = int(B) 

                            # if x == start_x or x == end_x:
                            #     pixelArr[width*3*y + 3*x + 0 ] = 0
                            #     pixelArr[width*3*y + 3*x + 1 ] = 0
                            #     pixelArr[width*3*y + 3*x + 2 ] = B

                        t_b_horz += t_b_step_horz_incr

                    t_b += t_b_step_inrc 
                    t_c += t_c_step_inrc




                pass
        

            
        
                
        not_eq = False
        idx = 0 

        if de_bug and dys2s1 > 0:

            for i in top_start_tex:

                if abs(bottom_start_tex[idx] - i) > eps:
                    not_eq = True


                idx += 1

            if not(not_eq):
                idx = 0 
                for i in top_end_tex:

                    if abs(bottom_end_tex[idx] - i) > eps:
                        not_eq = True
                    
                    idx += 1


            

        
        if not_eq and False:
            print("Top start    : ", top_start_tex)
            print("Bottom start : ", bottom_start_tex)
            print("UV2          : ", uv2 , "\n")


            print("Top end      : ", top_end_tex)
            print("Bottom end   : ", bottom_end_tex)
            print("UV2          : ", uv2)
            print("_________________________________")

        # line1 = "p1x: {:>7} p1y: {:>7}".format(round(p1x,3),round(p1y,3))
        # line2 = "p2x: {:>7} p2y: {:>7}".format(round(p2x,3),round(p2y,3))
        # line3 = "p3x: {:>7} p3y: {:>7}".format(round(p3x,3),round(p3y,3))


        # print(line1)
        # print(line2)
        # print(line3)
        # print("\n")
        # drawLine(p1x,p1y,p2x,p2y,pixelArr,width,height,R=0,G=0)
        # drawLine(p2x,p2y,p3x,p3y,pixelArr,width,height,R=0,G=0)
        # drawLine(p3x,p3y,p1x,p1y,pixelArr,width,height,R=0,G=0)


        if outLine:
            #debug = False if tri_idx == 0 else True

            debug = False 
            n1z = s1z
            n2z = s2z
            n3z = s3z

            # print("n1z: " , n1z  ,"s1y: " , s1y  )
            # print("n2z: " , n2z  ,"s2y: " , s2y  )
            # print("n3z: " , n3z  ,"s3y: " , s3y  )
            # print("---------------------")

            # print("n1 :",n1z, "s1z: ", s1z)
            # print("n2 :",n2z, "s2z: ", s2z)
            # print("n3 :",n3z, "s3z: ", s3z)

            drawLineZbuff(s1x,s1y,s2x,s2y,pixelArr,width,height,n1z,n2z,depthBuffer,R=0,G=0,debug=debug  )
            drawLineZbuff(s2x,s2y,s3x,s3y,pixelArr,width,height,n2z,n3z,depthBuffer,R=0,G=0,debug=debug)
            drawLineZbuff(s1x,s1y,s3x,s3y,pixelArr,width,height,n1z,n3z,depthBuffer,R=0,G=0,debug=debug)
        tri_idx +=1 


        


def TextY (pixelArr:np.ndarray,width,height):
    

    drawLine(-0.5,0.7,-0.1,0.2,pixelArr,width,height,0,0,255)
    drawLine(-0.1,0.233,-0.5,0.9,pixelArr,width,height,255,0,0)


    drawLine(0,0,0.5,0.9,pixelArr,width,height,255,0,0)
    drawLine(0.5,0.9,0,0,pixelArr,width,height,0,0,255)


    

def TestTriDraw(pixelArr:np.ndarray,width,height):

    tri = np.array([0.0,0.4,-0.5,-0.3,0.1,0,
                    0.5,0.4,-0.1,-.4,0.3,0.4])

    #DrawTris(tri,pixelArr,width,height,1,True,True,,R=0,G=0,B=255)



    pass




def main():
    pg.init()

    width = 600
    height = 600


    clock = pg.time.Clock()
    pixelArr= np.zeros(shape=(width*height*3),dtype=np.uint8)
    display_surface = pg.display.set_mode((width,height))

    #TestX(pixelArr,width,height)
    #TextY(pixelArr,width,height)
    #TestEdgeCases(pixelArr,width,height)

    TestTriDraw(pixelArr,width,height)
    
    
    #drawLine(-1,-1,0.5,0.5,pixelArr,width,height)
    #drawLine(0,-0.8,0,0,pixelArr,width,height)
    #drawLine(-1,-1,1,1,pixelArr,width,height)

    

    while True:
        
      

        surf = pg.image.frombuffer(pixelArr,(width,height),"RGB")


        display_surface.blit(surf,(0,0))


        

        #pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit(0)
        


        

    

        pg.display.update()
        clock.tick(60)


def test():

    a = np.array( [0.02491912 , 0.00662047])

    return 0 *  a 

if __name__ =="__main__":
    print(test())

 # [0.02491912 0.00662047]

