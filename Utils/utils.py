import numpy as  np
from numba import njit


@njit
def numpFast2(x,y):
    return np.array([x,y])

@njit
def numpFast3(x,y,z):
    return np.array([x,y,z])

@njit
def get_len(x):
    return len(x)

@njit
def dotProd (p1:np.ndarray , p2:np.ndarray):
    num_ = get_len(p1)
    sum_ = 0 

    for i in range(num_):
        sum_ += p1[i]*p2[i]

    return sum_

@njit 
def dotProdN(v1,v2,n):
    sum_ =  0
    for i in range(n):
        sum_ += v1[i]*v2[i]
    return sum_  




@njit
def dotProd3(v1,v2):
    sum_ =  0
    for i in range(3):
        sum_ += v1[i]*v2[i]
    return sum_  




@njit
def lerp(start, end , t):

    return (1-t)* start + t*end
    pass

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


# @njit
# def reduce(lst:np.ndarray, func:function ):

#     for i in 


"""
    This function just returns weather or not
    each entry in both numpy arrays are roughly equal 
    to some epsilon and returns false when two entries 
    are not 'close' . 
"""
@njit
def is_close(x:np.ndarray, y: np.ndarray,eps= 0.0001):
    
    for i in range(len(x)):

        if  abs(x[i] - y[i] ) > eps:
            return False


    return True 
    