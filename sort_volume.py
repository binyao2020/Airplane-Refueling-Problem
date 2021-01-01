# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 18:58:42 2020

@author: chang
"""
import math

def sort_volume(instance,epsilon):
    volume_list = [plane[1] for plane in instance]
    cr_list = [plane[0] for plane in instance] # list of consumption rate
    r = math.ceil(math.log(max(cr_list),1+epsilon))
    #print('r='+str(r))
    class_list = [] #records the type of each plane
    for j in range(len(instance)):
        class_list.append(math.floor(math.log(cr_list[j],1+epsilon))) #plane -> class
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

