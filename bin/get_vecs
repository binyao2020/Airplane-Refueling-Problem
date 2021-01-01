def get_vecs(instance,epsilon): # generate all state vectors precedes the biggest vector N and bounded by D_hat
    '''requires 
    from itertools import *
    import numpy as np
    '''
    N = get_max_vec(instance,epsilon)
    # generate all vectors precedes N
    L = len(N)
    vec_list = []
    bound = (1 + epsilon) * D_hat
    cr_list = np.array([(1+epsilon)**i for i in range(1,L+1)]) # list of consumption rate for each class
    bound_list = np.array([N[i] for i in range(L)]) # the bound for number of planes for each class
    vec_list = list(range(bound_list[0]+1)) # initialization
    for i in range(1,L):
        l = list(range(bound_list[i]+1))
        vec_list = list(product(vec_list,l))
        for j in range(len(vec_list)):
            if i == 1:
                tp1 = (vec_list[j][0],)
            else:
                tp1 = vec_list[j][0] 
            tp2 = (vec_list[j][1],)
            vec_list[j] = tp1+tp2 
    count = 0
    # remove vectors that exceeds the bound
    for j in range(len(vec_list)):
        if np.dot(vec_list[count],cr_list) > bound:
            vec_list.pop(count)
        else:
            count += 1
    return vec_list 
