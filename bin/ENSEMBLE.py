#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 21:34:28 2020
@author: binyao
"""

from math import *
from itertools import *
import numpy as np
import time

def generate_instance(n, sigma, seed): 
    """
    generate an instance with n planes where consumption rates c are integers
    randomly sampled between 1 and 100, and volumes v are correlated with c given by sigma
    return a list of tuples (c,v)
    """
    np.random.seed(seed)
    p = list(np.random.randint(1,101,n))
    instance = []
    for i in p:
        instance.append((i,2**(np.random.normal(0,sigma))*i)) # consumption rate & volume
    return instance

def get_structured_instance(instance, epsilon):
    """
    round up the consumption rate to nearest power of 1+epsilon
    return a vector and a list
    vector N: number of planes in each class
    list class_list: The ith item is a list includes the index of all planes in class i with volume sorted in descend order.
    """
    L = floor(log(max(instance[i][0] for i in range(len(instance))),1+epsilon))+1 # number of classes
    class_list = [[] for _ in range(L+1)]
    for idx in range(len(instance)):
        class_list[floor(log(instance[idx][0],1+epsilon))+1].append(idx)
    print(class_list)
    for idx in range(1,L+1): # C_1,...,C_L
        plane_list = class_list[idx]
        if len(plane_list) > 0:
            volume_list = [(plane_list[i],instance[plane_list[i]][1]) for i in range(len(plane_list))] # list of tuples (index,volume)
            volume_list = sorted(volume_list,key=lambda x:x[1],reverse=True)
            class_list[idx] = [volume_list[i][0] for i in range(len(volume_list))]
    class_list.pop(0)
    N = [len(class_list[i]) for i in range(len(class_list))]
    return N, class_list  

def get_vecs(instance,epsilon): # generate all state vectors precedes the biggest vector N and bounded by D_hat
    '''requires 
    from itertools import *
    import numpy as np
    '''
    N = get_max_vec(instance,epsilon)
    # generate all vectors precedes N
    L = len(N)
    vec_list = []
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
    return vec_list 

def get_apx_vecs(instance,epsilon):
    cr_list = [plane[0] for plane in instance] # list of consumption rate
    r = ceil(log(max(cr_list),1+epsilon)) # number of classes
    N = get_max_vec(instance,epsilon)
    vec_list = get_vecs(instance,epsilon)
    apx_vec_list = [tuple([0 for i in range(r)])]
    vec_list.pop(0)
    for vec in vec_list:
        total_cr = sum((1+epsilon)**j*vec[j] for j in range(r))
        C_star = 2**(floor(log(total_cr,2)))
        base = epsilon*C_star/r
        apx_vec = tuple([min(floor(ceil((1+epsilon)**(j+1)*vec[j]/base)*base/(1+epsilon)**(j+1)),N[j]) for j in range(r)])
        if apx_vec not in apx_vec_list:
            apx_vec_list.append(apx_vec)
        else:
            print('Awesome!!!')
    return apx_vec_list

def dynamic_prog(instance,epsilon):
    instance_dict = sort_volume(instance,epsilon)
    apx_vec_list = get_apx_vecs(instance,epsilon)
    val_list = [0 for apx_vec in apx_vec_list] # stores the value for each vector
    pred_list = [0 for apx_vec in apx_vec_list] # stores the index of predecessor for each vector
    total_cr_list = [0 for apx_vec in apx_vec_list]
    for i in range(len(apx_vec_list)):
        for j in range(i):
            vec = apx_vec_list[i]
            pred_vec = apx_vec_list[j]
            flag = True
            for k in range(r):
                if pred_vec[k] > vec[k]:
                    flag = False
            if flag == False:
                continue
            else:
                add_value = 0
                u = total_cr_list[j]
                for k in range(r):
                    for l in range(pred_vec[k]+1,vec[k]+1):
                        u += (1+epsilon)**(k+1)
                        add_value += instance_dict[k][l][1]/u
                if val_list[j]+add_value > val_list[i]:
                    val_list[i] = val_list[j]+add_value
                    pred_list[i] = j
                    total_cr_list[i] = u
    return val_list,pred_list

epsilon = sqrt(2)-1
instance = generate_instance(25,1,2)
