#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 21:34:28 2020

@author: binyao
"""

import math
from gurobipy import *
from itertools import *
import numpy as np
import time

def generate_instance(n, sigma, seed):
    np.random.seed(seed)
    p = list(np.random.randint(1,101,n))
    instance = []
    for i in p:
        instance.append((i,2**(np.random.normal(0,sigma))*i)) # consumption rate & volume
    return instance

def get_structured_instance(instance, epsilon):
    structured_instance = []
    for plane in instance:
        rounded_cr = (1+epsilon)**(math.floor(math.log(plane[0],1+epsilon))+1)
        structured_instance.append((rounded_cr,plane[1]))
    return structured_instance

def sort_volume(instance,epsilon):
    volume_list = [plane[1] for plane in instance]
    cr_list = [plane[0] for plane in instance] # list of consumption rate
    r = math.ceil(math.log(max(cr_list),1+epsilon))
    class_list = [] #records the type of each plane
    for j in range(len(instance)):
        class_list.append(math.floor(math.log(cr_list[j],1+epsilon))-1) #plane -> class
    sorted_volume = {}
    #assign each plane to a class in a dict
    for i in range(len(class_list)):
        if class_list[i] not in sorted_volume:
            sorted_volume[class_list[i]] = [(i,volume_list[i])]
        else:
            pre = sorted_volume[class_list[i]]
            pre.append((i,volume_list[i]))
            sorted_volume[class_list[i]] = pre
    #sort by volume
    def takeSecond(elem):
        return elem[1]
    for i in sorted_volume:
        v = sorted_volume[i]
        v.sort(key=takeSecond,reverse=True)
        sorted_volume[i] = v
    #sort the class from 0 to r
    class_volume_sorted = {}
    for i in sorted(sorted_volume):
        class_volume_sorted[i] = sorted_volume[i]
    return class_volume_sorted

def get_max_vec(instace,epsilon): # return the vector corresponds to the structured instance
    cr_list = [plane[0] for plane in instance] # list of consumption rate
    r = ceil(log(max(cr_list),1+epsilon)) # number of classes
    class_list = [] #records the type of each plane
    N = [] # number of planes for each class
    for j in range(len(instance)):
        class_list.append(floor(log(cr_list[j],1+epsilon))) #plane -> class
    for i in range(r):
        N.append(class_list.count(i))
    return N

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

epsilon = math.sqrt(2)-1
instance = generate_instance(25,1,2)
s_instance = get_structured_instance(instance, epsilon)
print(get_apx_vecs(s_instance,epsilon))
