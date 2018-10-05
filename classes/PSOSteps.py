import util.parameters as param

class PSOSteps:

    # constructor
    def __init__( self, s ):
        # Store objective function
        self.s = s
    
    # Evaluate a particle
    def evaluate( self, op ): 
        for i in range( param.NPARTICLE ):
            self.s.particles[i].evaluate( op )