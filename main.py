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
from classes.SHMParticle import SHMParticle as shm

import matplotlib.pyplot as plt
import numpy as np
import copy

def parallelEvaluation(s):
    pool = ProcessPoolExecutor(param.NTHREAD)
    futures = []
    for i in range(param.NTHREAD):
        futures.append(pool.submit(util.evaluate, s, i, 0))
    for x in as_completed(futures):
        s.particles[x.result()[0] : x.result()[1]] = x.result()[2]


"""   Declarations and definitions of PSO functions   """
# Update the velocity of a particle
def updateVelocity(aux, s, g):
    for i in range(param.NPARTICLE):
        r1 = np.random.random(param.DIM)
        r2 = np.random.random(param.DIM)
        s.particles[i].v = param.W[aux] * s.particles[i].v + \
              param.C1 * r1 * (s.particles[i].m - s.particles[i].x) + \
              param.C2 * r2 * (g.x - s.particles[i].x)
              
        for j in range(param.DIM):
            if(np.abs(s.particles[i].v[j]) > param.VMAX):
                s.particles[i].v[j] = np.sign(s.particles[i].v[j]) * param.VMAX    

# Find the best particle from the swarm
def getGlobalBest(s):
    fits = [p.fit_x for p in s.particles]
    i = fits.index(min(fits))
    return s.particles[i].getCopy()

# Move a particle in the search space
def move(s):
    for i in range(param.NPARTICLE):
        s.particles[i].x = s.particles[i].x + s.particles[i].v
        for j in range(param.DIM):
            if(s.particles[i].x[j] < param.RANGE[0]):
                s.particles[i].x[j] = param.RANGE[0]
            if(s.particles[i].x[j] > param.RANGE[1]):
                s.particles[i].x[j] = param.RANGE[1]
    
# Update local and global best memories
def updatePBAndGB(s, g):
    for i in range(param.NPARTICLE):
        if(s.particles[i].fit_x <= s.particles[i].fit_m):
            s.particles[i].m = copy.deepcopy(s.particles[i].x)
            s.particles[i].fit_m = s.particles[i].fit_x
            if(s.particles[i].fit_x <= g.fit_x):
                g.x = copy.deepcopy(s.particles[i].x)
                g.fit_x = s.particles[i].fit_x
                g.typeI = s.particles[i].typeI
                g.typeII = s.particles[i].typeII

def diversity(x, L):
    x = [i.x for i in x]
    avg = np.mean(x, 0)
    return np.sum(np.sqrt(np.sum((x - avg)**2, 1))) / (len(x) * L)

# Evaluate a particle
def evaluate( s, op ): 
    for i in range( param.NPARTICLE ):
        s.particles[i].evaluate( op )
#
def func( s ):
    for i in range( param.NPARTICLE ):
        for j in range( 0, param.DIM - ( param.NCLA - 1 ), 3 ):
            if( s.particles[i].x[j] < 0.01 or s.particles[i].x[j] > 0.99 ):
                s.particles[i].x[j] = np.random.random()
            
""" PSO """
def main():
    s = Swarm( util.f, param.NPARTICLE  )
    func( s )
    # shm.eval(s)
    evaluate(s,0)

    # parallelEvaluation(s) # tem que chamar agora
    g = getGlobalBest(s)
    avg = np.zeros(param.NITERATION)
    std = np.zeros(param.NITERATION)
    bfit = np.zeros(param.NITERATION)
    div = np.zeros(param.NITERATION)
    L = np.linalg.norm(np.ones(param.DIM) * (param.RANGE[1] - param.RANGE[0]))
    
    for i in range(param.NITERATION):
        updateVelocity(i, s, g)
        move(s)
        func( s )
        evaluate(s,0)
        # parallelEvaluation(s)
        updatePBAndGB(s, g)
        
        flag = shm.getNActivatedClauses(0,g.x)-1
                
        print(i+1, str(g.typeI)+"+"+str(g.typeII)+"="+str(g.fit_x), flag+1, sum(g.x[range(2, (flag+1)*12, 3)] <= param.PCON ))

        avg[i] = s.avgFitness()
        std[i] = s.stdFitness(avg[i])
        bfit[i] = g.fit_x
        div[i] = diversity(s.particles, L)       
              
    g.typeI, g.typeII, errors = util.f( g.x, 1 ) # evaluate test data set
            
    print(g) 
    
    t = range(param.NITERATION)
    plt.figure(3)    
    # Plot best particle through iterations
    plt.subplot(221)
    plt.plot(t, bfit)
    # plt.yscale('log')
    plt.grid(True)
    plt.xlabel("Iterations")
    plt.ylabel("Best particle fitness")
    
    # Plot average fitness through iterations
    plt.subplot(222)
    plt.plot(t, avg)
    plt.fill_between(t, avg+std, avg-std, facecolor='red', alpha=0.5)
    plt.grid(True)
    plt.xlabel("Iterations")
    plt.ylabel("Average fitness")
    
    # Plot average fitness through iterations
    plt.subplot(223)
    plt.plot(t, div)
    plt.grid(True)
    plt.xlabel("Iterations")
    plt.ylabel("Diversity") 
    
    # Plot natural frequency and classification
    tt = range( 1, param.NLIN + 1 )
    ids = [ i for i in range( param.NLIN ) if errors[i] == 1 ]
    plt.subplot(224)
    plt.plot( tt, util.originalDB[:param.NLIN, 0], 'xb')
    plt.plot( tt, util.originalDB[:param.NLIN, 1], 'xb')
    plt.plot( tt, util.originalDB[:param.NLIN, 2], 'xb')
    plt.plot( tt, util.originalDB[:param.NLIN, 3], 'xb')
    ttt = [ i+1 for i in ids ];
    plt.plot( ttt, util.originalDB[ids, 0], 'xr')
    plt.plot( ttt, util.originalDB[ids, 1], 'xr')
    plt.plot( ttt, util.originalDB[ids, 2], 'xr')
    plt.plot( ttt, util.originalDB[ids, 3], 'xr')
    plt.axvline(x = param.ID_TRAIN, color='k', linestyle='-')
    plt.axvline(x = param.ID_DAMAGE_START, color='k', linestyle='-')
    plt.grid(True)    
    plt.xlabel("Observations")
    plt.ylabel("Natural frequencies")   
    plt.title(g.getRule())
    plt.show()
    
if __name__ == '__main__':
    main()