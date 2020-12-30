#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 23:12:17 2020

@author: Yinghan

This function takes as input a value n = number of airplanes, and 
sigma = variance to be used in the normal distribution while generating an instance.

The function returns an instance of the airplane refueling problem as a list of 2-tuples.

"""
import numpy as np


def generate_instance(n, sigma, seed):
    np.random.seed(seed)
    p = list(np.random.randint(1,100,n))
    instance = []
    for i in p:
        instance.append((i,2**(np.random.normal(0,sigma))*i)) # consumption rate & volume
    return instance

#S1

n_S1 = list(range(14))
S1 = []
for i in range(14):
    n_S1[i] = (n_S1[i]+1)*10
    S1.append([])
sigma_S1 = 0.1
for i in range(len(n_S1)):
    for j in range(50):
        instance = generate_instance(n_S1[i],sigma_S1,j*n_S1[i])
        S1[i].append(instance)
print("endS1")
        

#sigma of S2 and S3       
sig = 0.1
Sigma = []
while sig <=1:
    Sigma.append(sig)
    sig += 0.001


#S2

size = {100,500,1000,2000,3000}
S2_100, S2_500, S2_1000, S2_2000, S2_3000 = [], [], [], [], []

for i in range(len(Sigma)):
    for j in range(1,6):
        instance = generate_instance(100,Sigma[i],int(j*1000*Sigma[i]))
        S2_100.append(instance)
print("end1")

for i in range(len(Sigma)):
    for j in range(1,6):
        instance = generate_instance(500,Sigma[i],int(j*5000*Sigma[i]))
        S2_500.append(instance)
print("end2")

for i in range(len(Sigma)):
    for j in range(1,6):
        instance = generate_instance(1000,Sigma[i],int(j*10000*Sigma[i]))
        S2_1000.append(instance)
print("end3")
        
for i in range(len(Sigma)):
    for j in range(1,6):
        instance = generate_instance(2000,Sigma[i],int(j*20000*Sigma[i]))
        S2_2000.append(instance)
print("end4")

for i in range(len(Sigma)):
    for j in range(1,6):
        instance = generate_instance(3000,Sigma[i],int(j*30000*Sigma[i]))
        S2_3000.append(instance)
print("end5")
        

#S3

size_S3 = 500
S3 = [] 

for i in range(len(Sigma)):
    for j in range(1,6):
        instance = generate_instance(500,Sigma[i],int(j*50000*Sigma[i]))
        S3.append(instance)
print("endS3")








