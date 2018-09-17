#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 11:54:10 2018

@author: Reginaldo Santos
"""

from concurrent.futures import ProcessPoolExecutor

from classes.Swarm import Swarm
import util.parameters as param
import util.functions as util

import matplotlib.pyplot as plt
import numpy as np
import copy


def parallelEvaluation(s):
    pool = ProcessPoolExecutor(param.NTHREAD)
    futures = []
    for i in range(param.NTHREAD):
        futures.append(pool.submit(util.evaluate, s, i))


"""   Declarations and definitions of PSO functions   """
# Update the velocity of a particle
def updateVelocity(i, p, g):
    r1 = np.random.random(param.DIM)
    r2 = np.random.random(param.DIM)
    p.v = param.W[i] * p.v + \
          param.C1 * r1 * (p.m - p.x) + \
          param.C2 * r2 * (g.x - p.x)
    for i in range(param.DIM):
        if(np.abs(p.v[i]) > param.VMAX):
            p.v[i] = np.sign(p.v[i]) * param.VMAX    

# Find the best particle from the swarm
def getGlobalBest(s):
    fits = [p.fit_x for p in s.particles]
    i = fits.index(min(fits))
    return s.particles[i].getCopy()

# Move a particle in the search space
def move(p):
    p.x = p.x + p.v
    for i in range(param.DIM):
        if(p.x[i] < param.RANGE[0]):
            p.x[i] = param.RANGE[0]
        if(p.x[i] > param.RANGE[1]):
            p.x[i] = param.RANGE[1]
            
# Evaluate a particle
def evaluate(p):
    p.evaluate()
    
# Update local and global best memories
def updatePBAndGB(p, g):
    if(p.fit_x <= p.fit_m):
        p.m = copy.deepcopy(p.x)
        p.fit_m = p.fit_x
        if(p.fit_x <= g.fit_x):
            g.x = copy.deepcopy(p.x)
            g.fit_x = p.fit_x
            
""" PSO """
s = Swarm(util.f, param.NPARTICLE)

g = getGlobalBest(s)


for i in range(param.NITERATION):
    for j in range(param.NPARTICLE):
        updateVelocity(i, s.particles[j], g)
        move(s.particles[j])
        evaluate(s.particles[j])
        updatePBAndGB(s.particles[j], g)

    
print(s)