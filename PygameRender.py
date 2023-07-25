import pygame as pg 
from sys import exit
import numpy as np
from numba import njit

import random as r



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

    
  
    if dx == 0 :
        if dy != 0 :
            if y1 > y2:
                x1,x2 = x2,x1
                y1,y2 = y2,y1
                dx = x2 - x1 
                dy = y2 - y1
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

            res_buf = np.empty(shape=(dx+1,2),dtype=np.int32)
            SlopeCorrectionX(x1,y1,x2,y2,res_buf,True)
            return res_buf
        else:
            if y1 > y2:
                x1,x2 = x2,x1
                y1,y2 = y2,y1
                dx = x2 - x1 
                dy = y2 - y1

            res_buf = np.empty(shape=(dy+1,2),dtype=np.int32)
            SlopeCorrectionY(x1,y1,x2,y2,res_buf,True)

            return res_buf
    elif slope < 0:
        if slope >= -1:
            if x1 > x2:
                x1,x2 = x2,x1
                y1,y2 = y2,y1
                dx = x2 - x1 
                dy = y2 - y1
            res_buf = np.empty(shape=(dx+1,2),dtype=np.int32)
            SlopeCorrectionX(x1,y1,x2,y2,res_buf,False)            
            return res_buf
        else:
            if y1 > y2:
                x1,x2 = x2,x1
                y1,y2 = y2,y1
                dx = x2 - x1 
                dy = y2 - y1
            res_buf = np.empty(shape=(dy+1,2),dtype=np.int32)
            SlopeCorrectionY(x1,y1,x2,y2,res_buf,False)            
            return res_buf


    return np.empty(shape=(0,2),dtype=np.int32)


print(Bresenham(3,2,15,5))
# print(Bresenham(0,0,4,2))

@njit
def lerp(a:float,b:float,t:float):
    return (1-t)*a + t*b


@njit
def clear(pixelArray:np.ndarray, size:int):
    for i in range(size):
        pixelArray[i] = 100



    
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







@njit
def DrawTris(Lst_tri:np.ndarray, pixelArr:np.ndarray,width:int,height:int , num_tris:int,outLine=True,FillCol=False,R=255,G=255,B=255):
    tri_idx = 0 

    
    while tri_idx <    num_tris:
        tri_point_idx = 6*tri_idx
        p1  = Lst_tri[tri_point_idx : tri_point_idx + 2 ]
        tri_point_idx +=2
        p2  = Lst_tri[tri_point_idx : tri_point_idx + 2 ]
        tri_point_idx +=2
        p3  = Lst_tri[tri_point_idx: tri_point_idx + 2 ]




        # print("p1: ",p1)
        # print("p2: ",p2)
        # print("p3: ",p3)



        p1x = p1[0]
        p1y = p1[1]

        p2x = p2[0]
        p2y = p2[1]

        p3x = p3[0]
        p3y = p3[1]




        s1x = int(lerp(0,width, (p1x+1)/2))
        s1y = int(lerp(height,0, (p1y+1)/2))

        s2x = int(lerp(0,width, (p2x+1)/2))
        s2y = int(lerp(height,0, (p2y+1)/2))

        s3x = int( lerp(0,width, (p3x+1)/2)  )
        s3y = int( lerp(height,0, (p3y+1)/2 ) )

        
        if FillCol:
            if s1y > s2y:
                s1x,s1y,s2x,s2y = s2x,s2y,s1x,s1y

            if s1y > s3y:
                s1x,s1y,s3x,s3y = s3x,s3y,s1x,s1y

            if s2y > s3y:
                s2x,s2y,s3x,s3y = s3x,s3y,s2x,s2y


            dys2s1 =  s2y - s1y
            dxs2s1 =  s2x - s1x

            dys3s1 = s3y - s1y
            dxs3s1 = s3x - s1x

            dys3s2 = s3y - s2y
            dxs3s2 = s3x - s2x
            
            # TOP HALF: s1y -> s2y
            da = 0 
            db = 0 

            if (dys2s1 != 0):
            
                da = dxs2s1 /dys2s1

                if dys3s1 != 0 :
                    db = dxs3s1 / dys3s1

                for y in range(s1y,s2y+1,1):
                    start_x:int  =   (s1x + (y - s1y)*da)
                    end_x:int  =   (s1x + (y - s1y)*db)
                    if start_x > end_x:
                        start_x,end_x = end_x , start_x
                    #drawLine(start_x,y,end_x,p3y,pixelArr,width,height,R,G,B)
                    for x in range(int(start_x),int(end_x+1)):
                        pixelArr[width*3*y + 3*x + 0 ] = R
                        pixelArr[width*3*y + 3*x + 1 ] = G
                        pixelArr[width*3*y + 3*x + 2 ] = B
        
            # Bottom Half: s2y -> s3y

            da = 0 
            db = 0 
            if (dys3s2!=0):
                da = dxs3s2 / dys3s2

                if dys3s1!=0:
                    db = dxs3s1 / dys3s1

                for y in range(s2y,s3y+1,1):
                    start_x:int =   (s2x + (y - s2y)*da)
                    end_x:int     =   (s1x + (y - s1y)*db)
                    if start_x > end_x:
                        start_x,end_x = end_x , start_x
                    #drawLine(start_x,y,end_x,p3y,pixelArr,width,height,R,G,B)
                    for x in range(int(start_x),int(end_x+1)):

                        
                        pixelArr[width*3*y + 3*x + 0 ] = R
                        pixelArr[width*3*y + 3*x + 1 ] = G
                        pixelArr[width*3*y + 3*x + 2 ] = B





                pass
                

        # line1 = "p1x: {:>7} p1y: {:>7}".format(round(p1x,3),round(p1y,3))
        # line2 = "p2x: {:>7} p2y: {:>7}".format(round(p2x,3),round(p2y,3))
        # line3 = "p3x: {:>7} p3y: {:>7}".format(round(p3x,3),round(p3y,3))


        # print(line1)
        # print(line2)
        # print(line3)
        # print("\n")
        drawLine(p1x,p1y,p2x,p2y,pixelArr,width,height,R=0,G=0)
        drawLine(p2x,p2y,p3x,p3y,pixelArr,width,height,R=0,G=0)
        drawLine(p3x,p3y,p1x,p1y,pixelArr,width,height,R=0,G=0)
        tri_idx +=1 



def TextY (pixelArr:np.ndarray,width,height):
    

    drawLine(-0.5,0.7,-0.1,0.2,pixelArr,width,height,0,0,255)
    drawLine(-0.1,0.233,-0.5,0.9,pixelArr,width,height,255,0,0)


    drawLine(0,0,0.5,0.9,pixelArr,width,height,255,0,0)
    drawLine(0.5,0.9,0,0,pixelArr,width,height,0,0,255)


    

def TestTriDraw(pixelArr:np.ndarray,width,height):

    tri = np.array([0.0,0.4,-0.5,-0.3,0.1,0,
                    0.5,0.4,-0.1,-.4,0.3,0.4])

    DrawTris(tri,pixelArr,width,height,1,True,True,R=0,G=0,B=255)



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

if __name__ =="__main__":
    main()