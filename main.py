#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 09:44:04 2018

@author: Reginaldo Santos
@description: Rotational variant PSO algorithm with fast information exchange
"""

import numpy as np
import matplotlib.pyplot as plt
import copy

import util.functions as f
import util.parameters as param
from classes.Swarm import Swarm


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
            
# Find the best particle from the swarm
def getGlobalBest(swarm):
    fits = [p.fit_x for p in swarm.particles]
    i = fits.index(min(fits))
    return swarm.particles[i].getCopy()



"""   Main iteration of the algorithm   """
f = f.himmelblau
swarm = Swarm(f, param.NPARTICLE)
swarm.initialize()
g = getGlobalBest(swarm)
avg = np.zeros(param.NITERATION)
std = np.zeros(param.NITERATION)
bfit = np.zeros(param.NITERATION)


# plot the level curves
r = np.arange(param.RANGE[0]-.2, param.RANGE[1]+.2, 0.05)
x, y = np.meshgrid(r, r)
z = copy.deepcopy(x) # temporarily
for i in range(x.shape[0]):
    z[i, :] = [f([x[i, j], y[i, j]]) for j in range(x.shape[1])]
    
fig, ax = plt.subplots()
ax.contour(x, y, z, 60)
plt.xlabel("Variable X")
plt.ylabel("Variable Y")

# plot the swarm and the global best particle
pos = np.matrix([[swarm.particles[j].x[0], swarm.particles[j].x[1]] for j in range(param.NPARTICLE)])
h = ax.plot(pos[:, 0], pos[:, 1], 'ob') # swarm
hg = ax.plot(g.x[0], g.x[1], 'xr', markersize = 8) # global best

for i in range(param.NITERATION):
    plt.title("Iteration: " + str(i+1))
    for j in range(param.NPARTICLE):
        updateVelocity(i, swarm.particles[j], g)
        move(swarm.particles[j])
        evaluate(swarm.particles[j])
        updatePBAndGB(swarm.particles[j], g)
    avg[i] = swarm.avgFitness()
    std[i] = swarm.stdFitness(avg[i])
    bfit[i] = g.fit_x
    # remove swarm and global best
    h[0].remove()
    hg[0].remove()
    # plot again swarm and global best
    pos = np.matrix([[swarm.particles[j].x[0], swarm.particles[j].x[1]] for j in range(param.NPARTICLE)])
    h = ax.plot(pos[:, 0], pos[:, 1], 'ob')
    hg = ax.plot(g.x[0], g.x[1], 'xr', markersize = 8)
    plt.pause(.005)



"""   Results and plots   """
t = range(param.NITERATION)
plt.figure(2)

# Plot best particle through iterations
plt.subplot(211)
plt.plot(t, bfit)
plt.yscale('log')
plt.grid(True)
plt.xlabel("Iterations")
plt.ylabel("Best particle fitness")

# Plot average fitness through iterations
plt.subplot(212)
plt.plot(t, avg)
plt.fill_between(t, avg+std, avg-std, facecolor='red', alpha=0.5)
plt.grid(True)
plt.xlabel("Iterations")
plt.ylabel("Average fitness")

plt.show()

print("Best result found")        
print(g)