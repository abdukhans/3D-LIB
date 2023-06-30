import numpy as  np
#@jit(target_backend='cuda' )
def numpFast2(x,y):
    return np.array([x,y])

#@jit(target_backend='cuda' )
def numpFast3(x,y,z):
    return np.array([x,y,z])

#@jit(target_backend='cuda' )
def get_len(x):
    return len(x)

#@jit(target_backend='cuda' )
def dotProd (p1:np.ndarray , p2:np.ndarray):
    num_ = get_len(p1)
    sum_ = 0 

    for i in range(num_):
        sum_ += p1[i]*p2[i]

    return sum_

