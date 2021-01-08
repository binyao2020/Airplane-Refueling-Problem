#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 19:02:51 2020

@author: binyao

This function takes as values instance, D_hat, epsilon, and returns a set of vectors such that each vector N
in [n]^L and satisfies \sum_{p=1}^L N(p) * (1 + epsilon)^p <= (1 + epsilon) * D_hat
"""

def get_max_vec(instance,epsilon): # return the vector corresponds to the structured instance
    cr_list = [plane[0] for plane in instance] # list of consumption rate
    r = max(ceil(log(max(cr_list),1+epsilon)),1) # number of classes
    class_list = [] #records the type of each plane
    N = [] # number of planes for each class
    for j in range(len(instance)):
        class_list.append(floor(log(cr_list[j],1+epsilon))) #plane -> class
    for i in range(r):
        N.append(class_list.count(i))
    return N

def get_appx_state_vecs(instance,epsilon, D_hat): # generate all state vectors precedes the biggest vector N and bounded by D_hat
    '''requires 
    from itertools import *
    import numpy as np
    '''
    N = get_max_vec(instance,epsilon)
    # generate all vectors precedes N
    L = len(N)
    appx_state_vecs = []
    bound = (1 + epsilon) * D_hat
    cr_list = np.array([(1+epsilon)**i for i in range(1,L+1)]) # list of consumption rate for each class
    bound_list = np.array([min(N[i],floor(bound/cr_list[i])) for i in range(L)]) # the bound for number of planes for each class
    appx_state_vecs = list(range(bound_list[0]+1)) # initialization
    for i in range(1,L):
        l = list(range(bound_list[i]+1))
        appx_state_vecs = list(product(appx_state_vecs,l))
        for j in range(len(appx_state_vecs)):
            if i == 1:
                tp1 = (appx_state_vecs[j][0],)
            else:
                tp1 = appx_state_vecs[j][0] 
            tp2 = (appx_state_vecs[j][1],)
            appx_state_vecs[j] = tp1+tp2 
    count = 0
    # remove vectors that exceeds the bound
    for j in range(len(appx_state_vecs)):
        if np.dot(appx_state_vecs[count],cr_list) > bound:
            appx_state_vecs.pop(count)
        else:
            count += 1
    return appx_state_vecs
