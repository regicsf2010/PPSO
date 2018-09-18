#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 17:52:52 2018

@author: Reginaldo Santos
"""
from numpy import genfromtxt

import util.parameters as param


# Normalize data by minmax
def norm(data):
    for j in range(param.NCOL):
        m = min(data[:, j])
        diff = max(data[:, j]) - m
        data[:, j] = (data[:, j] - m) / diff
    return data

# Load database: z24
data = genfromtxt(param.FILENAME, delimiter = ',')
data = norm(data)

# Objective function: errors type I and type II
def f(x):
    typeI = typeII = 0
    cols = [i - 2 for i in range(2, param.DIM, 3) if x[i] <= param.TACT]
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
    return [typeI, typeII]

def evaluate(s, i):
    n = param.NPARTICLE / param.NTHREAD
    start = int(i * n)
    end = int(i * n + n)
    for j in range(start, end):
        s.particles[j].evaluate()
    return [start, end, s.particles[start:end]]        