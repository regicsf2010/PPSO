#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 17:52:52 2018

@author: Reginaldo Santos
"""

import numpy as np

import util.parameters as param

# Normalize data by minmax
def norm(data):
    for j in range(param.NCOL):
        m = min(data[:, j])
        diff = max(data[:, j]) - m
        data[:, j] = (data[:, j] - m) / diff
    return data

# Load database: z24
data = np.genfromtxt(param.FILENAME, delimiter = ',')
data = norm(data)

# Objective function: errors type I and type II
def f(x,op):
    typeI = typeII = 0 # no damage
    cols = [i - 2 for i in range(2, param.DIM, 3) if x[i] <= param.TACT]
    if(len(cols) == 0):
        # cols = [int(x) for x in str(np.argmin(x[ np.arange(2,12,3) ])*3)]
        cols = 3 * np.random.randint(4)
        x[cols+2] = np.random.random() * param.TACT
        cols = [int(x) for x in str(cols)]
        
    if(op == 0):
        for i in range(param.ID_TRAIN):
            for j in cols:
                if(x[j+1] <= param.TSIG):
                    if(data[i][int(j/3)] > x[j]):
                        typeI += 1 # damage
                        # count += 1/x[j] 
                        break
                else:
                    if(data[i][int(j/3)] < x[j]):
                        typeI += 1 # damage
                        # count += x[j] 
                        break
                    
        count = 0            
        for i in cols:
            if(x[i+1] <= param.TSIG):
                if(x[i] == 0):
                    count += 100000000;
                else:
                    count += 1/x[i] 
            else:
                if(x[i] == 0):
                    count += 100000000;
                else:
                    count += x[i] 
            
        return [typeI, -1, count/len(cols) ]
    else:
        for i in range(param.NLIN):
            t = 0 # no damage
            for j in cols:
                if(x[j+1] <= param.TSIG):
                    if(data[i][int(j/3)] > x[j]):
                        t = 1 # damage
                        break
                else:
                    if(data[i][int(j/3)] < x[j]):
                        t = 1 # damage
                        break
            if(t == 1 and i < param.ID_DAMAGE_START):
                typeI += 1
            elif(t == 0 and i >= param.ID_DAMAGE_START):
                typeII += 1
        return [typeI, typeII, len(cols) ]

def evaluate(s, i, op):
    n = param.NPARTICLE / param.NTHREAD
    start = int(i * n)
    end = int(i * n + n)
    for j in range(start, end):
        s.particles[j].evaluate(op)
    return [start, end, s.particles[start:end]]        