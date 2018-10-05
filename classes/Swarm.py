from classes.SHMParticle import SHMParticle
import util.parameters as param

import math

class Swarm:
    
    # constructor
    def __init__( self, f, n = None ):
        if n is not None:
            self.n = n
        else:
            self.n = param.NPARTICLE
        
        self.f = f
        self.particles = []
        self.initialize()
        
    # Build each particle 
    def initialize( self ):
        for i in range( self.n ):
            self.particles.insert( i, SHMParticle( self.f ) )
    
    # Average the swarm fitness
    def avgFitness( self ):
        return sum( p.fit_x for p in self.particles ) / float( self.n )
    
    # Average swarm deviation
    def stdFitness( self, avg = None ):
        if avg is None:
            avg = self.avgFitness()
        return math.sqrt( sum( ( p.fit_x - avg ) ** \
                            2 for p in self.particles ) / float( self.n - 1 ) )
        
    # Output fitness of each particle
    def printFitness( self ):
        print( [ p.fit_x for p in self.particles ] )
    
    # Get a copy of the best swarm particle   
    def getBestParticle( self ):
        fits = [ p.fit_x for p in self.particles ]
        return self.particles[ fits.index( min( fits ) ) ].getCopy()
    
    # Output swarm information
    def __str__( self ):
        avg = self.avgFitness()
        std = self.stdFitness( avg )
        print( "=== best particle of the swarm ===" )
        print( self.getBestParticle() )
        print( "=====================" )
        return "swarm avg fitness: " + str( round( avg, 3 ) ) + \
                                "\nswarm std fitness: " + str( round( std, 3 ) )
               