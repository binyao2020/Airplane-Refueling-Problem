#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 15:40:01 2021

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
    list class_list: The ith item is a list includes the index of all planes in class i with volume sorted in descending order.
    """
    L = floor(log(max(instance[i][0] for i in range(len(instance))),1+epsilon))+1 # number of classes
    class_list = [[] for _ in range(L+1)]
    for idx in range(len(instance)):
        class_list[floor(log(instance[idx][0],1+epsilon))+1].append(idx)
    for idx in range(1,L+1): # C_1,...,C_L
        plane_list = class_list[idx]
        if len(plane_list) > 0:
            volume_list = [(plane_list[i],instance[plane_list[i]][1]) for i in range(len(plane_list))] # list of tuples (index,volume)
            volume_list = sorted(volume_list,key=lambda x:x[1],reverse=True)
            class_list[idx] = [volume_list[i][0] for i in range(len(volume_list))]
    class_list.pop(0)
    N = [len(class_list[i]) for i in range(len(class_list))]
    return N, class_list  

def generate_vectors(instance,epsilon,LB=0,UB=inf): 
    """
    generate all state vectors precedes the biggest vector N, and bounded by LB and UB (set to 0 and infinite by default)
    return vec_list
    """
    # generate all vectors precedes N
    L = len(N)
    vec_list = []
    cr_list = np.array([(1+epsilon)**i for i in range(1,L+1)]) # list of consumption rate for each class\
    vec_list = list(range(N[0]+1)) # initialization
    for i in range(1,L):
        l = list(range(N[i]+1))
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
    if UB < inf:
        for j in range(len(vec_list)):
            total = np.dot(vec_list[count],cr_list)
            if total > UB or total < LB:
                vec_list.pop(count)
            else:
                count += 1
    return vec_list
n = 25
sigma = 1
seed = 0
epsilon = sqrt(2)-1
bound = 1000
instance = generate_instance(n,sigma,seed)
N,class_list = get_structured_instance(instance, epsilon)
vec_list = generate_vectors(instance,epsilon)
