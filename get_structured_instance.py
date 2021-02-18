#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 23:24:47 2020

@author: binyao

This function takes as input an instance of the airplane refueling problem,
and a value epsilon 

It returns a structured instance of the airplane refueling problem based on epsilon.

"""

from math import *

def get_structured_instance(instance, epsilon):
    structured_instance = []
    for plane in instance:
        rounded_cr = (1+epsilon)**(floor(log(plane[0],1+epsilon))+1)
        structured_instance.append((rounded_cr,plane[1]))
    return structured_instance
