import pygame as pg 
import numpy as np
from numba import njit
from Utils import utils as ut 



#@njit 
def dotProdN(v1,v2,n):
    sum_ =  0
    for i in range(n):
        sum_ += v1[i]*v2[i]
    return sum_  



#@njit
def vectMatMul(vect:np.ndarray, matrix:np.ndarray,size:int) -> np.ndarray:

    res = np.empty( size,dtype=np.float64)

    mat_trans = matrix.T 
    entry_idx = 0 
    for row in mat_trans:
        res[entry_idx] = dotProdN(vect, row,size)
        entry_idx += 1
            


    return res


@njit
def makeNump(lst) -> np.ndarray:
    return np.frombuffer(lst,dtype=np.uint8)


def makeNumpTexture(path:str) -> np.ndarray:

    img = pg.image.load(path)

    width = img.get_width()
    height = img.get_height() 


    return makeNump(pg.image.tobytes(img,"RGB")).reshape(height,width,-1)



"""
    u:   This is the component along the u axis
    v:   This is the component along the v axis

    text_buff: This is a  H x W x 3 

    NOTE: Both u and yv are in a nomralized sapce meaning in between zero  and one.
          Also note that (0,0) maps to the bottom left of the screen
"""
@njit
def Sample(u:float,v:float,text_buff:np.ndarray):

    shape = text_buff.shape
    
    height = shape[0]
    width  = shape[1]



    # print("shape: " , shape)
    # print("height: ", height)
    # print("Width : ", width)

    # uv_vect = np.array([u,v],dtype=np.float64)


    # screenTrans = np.array([
    #                         [0         , width  - 1 ],
    #                         [1 - height, 0          ]
    #                        ],dtype=np.float64)

    
    # intrim_cords =np.array([ int(round(i)) for i in ut.vectMatMul( uv_vect , screenTrans,2)], dtype= np.float64) 
    # array_cords = intrim_cords +  np.array([ height - 1 , 0 ] ,dtype= np.float64)

    # # print("Intrim Cords: " , intrim_cords)
    # # print("Array Cords : " , array_cords)

    # x = int(array_cords[1])
    # y = int(array_cords[0])

    # x = int((v - 1)*(1- height ))
    x = int((u) * (width - 1))
    y = int((v - 1)*(1- height ))

    # x = int(u * (width  - 1))
    # y = int(v * (height  - 1))

    if x >= width:
        x = width - 1
    
    if y >= height:
        y = height - 1
    return text_buff[y][x]
    




    






def main():

    cottage_text = "C:/Users/abdul/OneDrive/Documents/CODING HOBBIES/3D Lib Py/34-cottage_textures/cottage_textures/cottage_diffuse.png"
    test         = "Test.png"


    text_buff = makeNumpTexture(test)

    height = text_buff.shape[0]
    width  = text_buff.shape[1]
    print(text_buff[0][0])
    print(Sample(0,1, text_buff ))




    pass



if __name__ == "__main__":

    main()
