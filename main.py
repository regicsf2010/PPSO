#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 11:54:10 2018

@author: Reginaldo Santos
"""

# from concurrent.futures import ProcessPoolExecutor, as_completed

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
    for x in as_completed(futures):
        s.particles[x.result()[0] : x.result()[1]] = x.result()[2]


"""   Declarations and definitions of PSO functions   """
# Update the velocity of a particle
def updateVelocity(p, g):
    for i in range(param.NPARTICLE):
        r1 = np.random.random(param.DIM)
        r2 = np.random.random(param.DIM)
        p.particles[i].v = param.W[i] * p.particles[i].v + \
              param.C1 * r1 * (p.particles[i].m - p.particles[i].x) + \
              param.C2 * r2 * (g.x - p.particles[i].x)
        for j in range(param.DIM):
            if(np.abs(p.particles[i].v[j]) > param.VMAX):
                p.particles[i].v[j] = np.sign(p.particles[i].v[j]) * param.VMAX    

# Find the best particle from the swarm
def getGlobalBest(s):
    fits = [p.fit_x for p in s.particles]
    i = fits.index(min(fits))
    return s.particles[i].getCopy()

# Move a particle in the search space
def move(p):
    for i in range(param.NPARTICLE):
        p.particles[i].x = p.particles[i].x + p.particles[i].v
        for j in range(param.DIM):
            if(p.particles[i].x[j] < param.RANGE[0]):
                p.particles[i].x[j] = param.RANGE[0]
            if(p.particles[i].x[j] > param.RANGE[1]):
                p.particles[i].x[j] = param.RANGE[1]
            
# Evaluate a particle
def evaluate(p,aux):
    for i in range(param.NPARTICLE):
        p.particles[i].evaluate(aux)
    
# Update local and global best memories
def updatePBAndGB(p, g):
    for i in range(param.NPARTICLE):
        if(p.particles[i].fit_x <= p.particles[i].fit_m):
            p.particles[i].m = copy.deepcopy(p.particles[i].x)
            p.particles[i].fit_m = p.particles[i].fit_x
            if(p.particles[i].fit_x <= g.fit_x):
                g.x = copy.deepcopy(p.particles[i].x)
                g.fit_x = p.particles[i].fit_x
            
""" PSO """
def main():
    s = Swarm(util.f, param.NPARTICLE)
    # parallelEvaluation(s) # tem que chamar agora
    g = getGlobalBest(s)
    
    for i in range(param.NITERATION):
        updateVelocity(s, g)
        move(s)
        evaluate(s,0)
        # parallelEvaluation(s)
        updatePBAndGB(s, g)
        print(i+1, g.fit_x)
        #if(g.fit_x == 0):
        #    break
    
    evaluate(s,1)
    
    print(s)

if __name__ == '__main__':
    main()