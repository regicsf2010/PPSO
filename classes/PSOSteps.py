import util.parameters as param

import numpy as np
import copy

"""   Declarations and definitions of PSO functions   """

class PSOSteps:

    # constructor
    def __init__( self, s ):
        # Store objective function
        self.s = s
    
    # Evaluate a particle
    def evaluate( self, op ): 
        for i in range( param.NPARTICLE ):
            self.s.particles[i].evaluate( op )
            
    # Update the velocity of a particle
    def updateVelocity( self, it, g ):
        for i in range( param.NPARTICLE ):
            r1 = np.random.random( param.DIM )
            r2 = np.random.random( param.DIM )
            self.s.particles[i].v = param.W[it] * self.s.particles[i].v + \
                param.C1 * r1 * ( self.s.particles[i].m - \
                self.s.particles[i].x ) + param.C2 * r2 * \
                ( g.x - self.s.particles[i].x )
                  
            for j in range( param.DIM ):
                if( np.abs( self.s.particles[i].v[j] ) > param.VMAX ):
                    self.s.particles[i].v[j] = \
                                np.sign( self.s.particles[i].v[j] ) * param.VMAX   

    # Move a particle in the search space
    def move( self ):
        for i in range( param.NPARTICLE ):
            self.s.particles[i].x = self.s.particles[i].x + \
                                                       self.s.particles[i].v
            for j in range( param.DIM ):
                if( self.s.particles[i].x[j] < param.RANGE[0] ):
                    self.s.particles[i].x[j] = param.RANGE[0]
                if( self.s.particles[i].x[j] > param.RANGE[1] ):
                    self.s.particles[i].x[j] = param.RANGE[1]

    # Update local and global best memories
    def updatePBAndGB( self, g ):
        for i in range( param.NPARTICLE ):
            if( self.s.particles[i].fit_x <= self.s.particles[i].fit_m ):
                self.s.particles[i].m = copy.deepcopy( self.s.particles[i].x )
                self.s.particles[i].fit_m = self.s.particles[i].fit_x
                if( self.s.particles[i].fit_x <= g.fit_x ):
                    g.x = copy.deepcopy( self.s.particles[i].x )
                    g.fit_x = self.s.particles[i].fit_x
                    g.typeI = self.s.particles[i].typeI
                    g.typeII = self.s.particles[i].typeII
                    
    # Find the best particle from the swarm
    def getGlobalBest( self ):
        fits = [ p.fit_x for p in self.s.particles ]
        i = fits.index( min( fits ) )
        return self.s.particles[i].getCopy()  
                                                                       