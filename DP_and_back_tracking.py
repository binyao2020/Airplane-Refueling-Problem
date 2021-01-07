# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 21:03:29 2020

@author: chang
"""
import numpy as np


def Dynamic_Program(F, i, T, num_class, epsilon, sorted_instance):
    T_new = {}
    for vec_i in F[i]:
        feasible = []
        for vec_i_1 in F[i-1]:
            for j in range(num_class):
                if vec_i[j] < vec_i_1[j]:
                    break
            feasible.append(vec_i_1)
        T1 = {}
        for vec in feasible:
            v1 = 0
            for p in range(num_class):
                for k in range(vec[p]+1,vec_i[p]+1):
                    v1 += sorted_instance[p][k]          
            T1[vec] = T[vec] + 1/((1+epsilon)**i*v1)
        T1_ordered = sorted(T1.items(),key=lambda x:x[1],reverse=True)
        T_new[vec_i] = T1_ordered[0][1]

    #T_new_ordered = sorted(T_new.items(),key=lambda x:x[1],reverse=True)
    #DP_value = T_new_ordered[0][1]

    return T_new
            
            
            
def DP(num_buckets, num_class, F, epsilon, sorted_instance):    
    
    vec_0 = np.zeros(num_class)
    T_0 = {vec_0:0}
    T_record = []
    T_record.append(T_0)
         
    for i in range(1,num_buckets+1):
        if i ==1:
            T_N = Dynamic_Program(F, i, T_0, num_class, epsilon, sorted_instance)
            T_pre = T_N
            T_record.append(T_N)
        else:
            T_N = Dynamic_Program(F, i, T_pre, num_class, epsilon, sorted_instance)
            T_pre = T_N
            T_record.append(T_N)
    return T_N[0][1], T_record


N_L = get_max_vec(instace,epsilon)#imported function from get_appx_state_vecs


def back_tracking(num_buckets, num_class, F, T_record, N_L):
    N = []
    N.append(N_L)
    for i in range(num_buckets,0,-1):
        if i == num_buckets:
            N_i = N_L
            feasible = []
            for vec_i_1 in F[i-2]:
                for j in range(num_class):
                    if N_i[j] < vec_i_1[j]:
                        break
                feasible.append(vec_i_1)
            T_i_1 = T_record[i-2]
            N_i_1 = 0
            T_i_1_max = 0
            for vec in feasible:
                if T_i_1_max < T_i_1[vec]:
                    T_i_1_max = T_i_1[vec]
                    N_i_1 = vec
            N.append(N_i_1)
        else:
            N_i = N_i_1
            feasible = []
            for vec_i_1 in F[i-2]:
                for j in range(num_class):
                    if N_i[j] < vec_i_1[j]:
                        break
                feasible.append(vec_i_1)
            T_i_1 = T_record[i-2]
            N_i_1 = 0
            T_i_1_max = 0
            for vec in feasible:
                if T_i_1_max < T_i_1[vec]:
                    T_i_1_max = T_i_1[vec]
                    N_i_1 = vec
            N.append(N_i_1)
    return N




            
            
            
            
            
            
        