#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 17:52:52 2018

@author: Reginaldo Santos
"""

import numpy as np

import util.parameters as param

# Normalize data by min-max
def norm( data ):
    for j in range( param.NCOL ):
        m = min( data[ :, j ] )
        diff = max( data[ :, j ] ) - m
        data[ :, j ] = ( data[ :, j ] - m ) / diff

# Load database: z24
originalDB = np.genfromtxt( param.FILENAME1, delimiter = ',' )

data = originalDB.copy()
norm( data )

aux = np.genfromtxt( param.FILENAME2, delimiter = ',' )
data = np.concatenate( ( data, aux ) )

def classify( g, i ):
    out = 0
    
    x = g.x  
      
    flag = 0
            
    cols = [j - 2 for j in range(2, 12, 3) if x[j] <= param.PCON]
    
    if(x[param.DIM-2] <= param.PCLA):
        flag += 1
        cols2 = [j - 2 for j in range(14, 24, 3) if x[j] <= param.PCON]
            
    if(x[param.DIM-1] <= param.PCLA and flag == 1):  
        flag += 1
        cols3 = [j - 2 for j in range(26, param.DIM-2, 3) if x[j] <= param.PCON]
        
    t = 0 # no damage                        
    for j in cols:
        if(x[j+1] <= param.PSIG):
            if(data[i][int(j/3)] > x[j]):
                t = 1 # damage
                break 
        else:
            if(data[i][int(j/3)] < x[j]):
                t = 1 # damage
                break
            
    if(t == 1 and flag > 0):
        for j in cols2:
            if(x[j+1] <= param.PSIG):
                if(data[i][int(j/3-4)] > x[j]):
                    t += 1 # damage
                    break 
            else:
                if(data[i][int(j/3-4)] < x[j]):
                    t += 1 # damage
                    break
        
        if(t == 2 and flag > 1):
            for j in cols3:                                                         
                if(x[j+1] <= param.PSIG):
                    if(data[i][int(j/3-8)] > x[j]):
                        t += 1 # damage
                        break 
                else:
                    if(data[i][int(j/3-8)] < x[j]):
                        t += 1 # damage
                        break
                        
    if( (t == 1+flag and i < param.ID_DAMAGE_START-1) or (t < 1+flag and i >= param.ID_DAMAGE_START-1)):
        out = 1;
    
    return out   

def getTypeIandTypeII( g ):
    ids = [ i for i in range( param.NLIN ) if classify( g, i ) == 1 ]
    typeI = len( [ i for i in ids if i < param.ID_DAMAGE_START - 1 ] )
    typeII = len( ids ) - typeI
    return [ typeI, typeII, typeI + typeII ]
         
def evaluate(s, i, op):
    n = param.NPARTICLE / param.NTHREAD
    start = int(i * n)
    end = int(i * n + n)
    for j in range(start, end):
        s.particles[j].evaluate(op)
    return [start, end, s.particles[start:end]]