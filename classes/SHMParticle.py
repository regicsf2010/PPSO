import numpy as np
import copy

import util.parameters as param
import util.functions as util

class SHMParticle:

    # contructor
    def __init__(self, f, n = None, x = None):
        # store objective function
        self.f = f
        
        if n is not None:
            self.n = n
        else:
            self.n = param.DIM

        # start position at random
        if x is not None:
            self.x = x * np.ones(self.n) # change to array-like
        else:
            self.x = param.RANGE[0] + (param.RANGE[1] - param.RANGE[0]) * np.random.random(self.n)

        # evaluate position
        self.typeI = self.typeII = self.fit_x = 10000

        # start velocity with 0
        self.v = np.zeros( self.n )

        # deep copy the current position as best personal and fitness
        self.m = copy.deepcopy( self.x )
        self.fit_m = self.fit_x
    
    # Evaluate the particle as accuracy    
    def evaluate( self, op ):
        self.typeI, self.typeII, [] = self.f( self.x, op )
        self.fit_x = self.typeI + self.typeII
        
    #
    def getNActivatedClauses( self, x ):
        n = 1
        for i in range( param.NCLA-1, 0, -1 ):
            if( x[ param.DIM - i ] <= param.PCLA ):
                n += 1 
            else:
                break            
        return n
    
    # Deep copy of this object#
    def getCopy(self):
        return copy.deepcopy(self)

    # Verify if the particle has the rule enabled
    def isRule(self):
        n = [i for i in range(2, self.n, 3) if self.x[i] <= param.TACT] # list
        return True if len(n) != 0 else False

    # Convert the particle to the rule
    def getRule(self):
        r = "IF ("
        nv = 1
        flag = 0
        for i in range( 0, self.n - ( param.NCLA - 1 ), 3 ):
            if self.x[ i + 2 ] <= param.PCON:
                r += " x" + str( nv ) + ( " < " if self.x[ i + 1 ] < param.PSIG else " > ") + str( "{:.3f}".format( self.x[i] ) ) + " AND"

            nv += 1

            if( nv == param.DBSIZE+1 ):
                if( flag == ( param.NCLA - 1 ) ):
                    break
                if( self.x[ param.DIM - ( ( param.NCLA - 1 ) - flag ) ] > param.PCLA ):
                    break
                flag += 1
                r = r[:-4] + " ) OR ("
                nv = 1

        return r[:-4] + " )"

    # This method is used to print this object
    def __str__(self):
        return "x: " + str([round(i, 3) for i in self.x]) + \
               "\nfit_x: " + str(self.fit_x) + \
               "\nerr: " + str([self.typeI, self.typeII]) + \
               "\nrule: " + self.getRule()
