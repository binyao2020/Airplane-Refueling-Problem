#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 23:24:47 2020

"""

"""

This function takes as input an instance of the airplane refueling problem,
and a value epsilon 

It returns a structured instance of the airplane refueling problem based on epsilon.

"""

def get_structured_instance(instance, epsilon):
    structured_instance = []
    for plane in instance:
        rounded_cr = (1+epsilon)**(ceil(log(plane[1],1+epsilon)))
        structured_instance.append((plane[0],rounded_cr))
    return structured_instance
