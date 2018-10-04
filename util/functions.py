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

# Objective function: errors type I and type II
def f( x, op ):
    typeI = typeII = 0 # no damage
    actClau = getNActivatedClauses( x )
    cols = getCols( x )
    
    if(op == 0):    
        errors = []
        aux = 0
        for i in range( param.ID_TRAIN + param.NART ):
            if(i == param.ID_TRAIN):
                aux = 809
            t = getT( i+aux, x, cols )   
            
            if(t == actClau and i+aux < param.ID_DAMAGE_START-1):
                typeI += 1
            elif(t < actClau and i+aux >= param.ID_DAMAGE_START-1):
                typeII += 1
    else:
        errors = np.zeros( param.NLIN );
        for i in range( param.NLIN ):
            t = getT( i, x, cols )   
            
            if( t == actClau and i < param.ID_DAMAGE_START - 1 ):
                typeI += 1
                errors[ i ] = 1
            elif( t < actClau and i >= param.ID_DAMAGE_START - 1 ):
                typeII += 1
                errors[ i ] = 1
            else:
                errors[ i ] = 0
                    
    return [ typeI, typeII, errors ]

def getT( id, x, cols ):
    actClau = getNActivatedClauses( x )
    
    t = 0 # no damage
    for i in range(actClau):
        aux = cols[ i, cols[i,:] > -1 ]
        for j in aux:                
            if(x[int(j)+1] <= param.PSIG):
                if(data[id][int(j/3-4*i)] > x[int(j)]):
                    t += 1 # damage
                    break
            else:
                if(data[id][int(j/3-4*i)] < x[int(j)]):
                    t += 1 # damage
                    break

    return t
#
def getCols( x ):
    actClau = getNActivatedClauses( x )
    cols = np.ones( ( actClau, param.DBSIZE ) ) * -1
                
    id = 2
    for i in range(actClau):
        aux = [ j - 2 for j in range( id, id+10, 3 ) if x[j] <= param.PCON ]
        if(len(aux) == 0):
            x, aux = getActivatedCondition( x, id )
        
        cols[ i, :len( aux ) ] = aux
                        
        id += 12
    return cols
    
#
def getNActivatedClauses( x ):
    n = 1
    for i in range( param.NCLA - 1, 0, -1 ):
        if( x[ param.DIM - i ] <= param.PCLA ):
            n += 1 
        else:
            break            
    return n

#
def getActivatedCondition( x, acc ):
    aux = 3 * np.random.randint( param.NCOL ) + acc-2
    x[ aux + 2 ] = np.random.random() * param.PCON 
    aux = list( [ aux ] ) 
    return x, aux
      
def evaluate(s, i, op):
    n = param.NPARTICLE / param.NTHREAD
    start = int(i * n)
    end = int(i * n + n)
    for j in range(start, end):
        s.particles[j].evaluate(op)
    return [start, end, s.particles[start:end]]