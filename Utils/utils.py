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

