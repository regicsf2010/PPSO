import util.parameters as param
import util.functions as util

import matplotlib.pyplot as plt

class PSOPlots:

    # constructor
    def __init__( self, t ):
        self.t = t
    
    # Plot best particle through iterations
    def bestFitness( self, position, bfit ):     
        plt.subplot( position )
        plt.plot( self.t, bfit )
        # plt.yscale( 'log' )
        plt.grid( True )
        plt.xlabel( "Iteration" )
        plt.ylabel( "Best particle fitness" )
    
    # Plot average fitness, and standard deviation, through iterations    
    def avgFitness( self, position, avg, std ): 
        plt.subplot( position )
        plt.plot( self.t, avg )
        plt.fill_between( self.t, avg + std, avg - std, facecolor = 'red', \
                                                                alpha = 0.5 )
        plt.grid( True )
        plt.xlabel( "Iteration" )
        plt.ylabel( "Average fitness" )
        
    # Plot diversity through iterations
    def divSwarm( self, position, div ):
        plt.subplot( position )
        plt.plot( self.t, div )
        plt.grid( True )
        plt.xlabel( "Iteration" )
        plt.ylabel( "Diversity" ) 
        
    # Plot natural frequencies and misclassification
    def DBMisclass( self, position, g, classLabels ):
        t = range( 1, param.NLIN + 1 )
        classLabels = [ i for i in range( param.NLIN ) if classLabels[i] == 1 ]
        misclass = [ i + 1 for i in classLabels ]; # misclassification
        
        plt.subplot( position )
        for i in range( param.NCOL ):
            plt.plot( t, util.originalDB[ :param.NLIN, i ], 'xb' )
            plt.plot( misclass, util.originalDB[ misclass, i ], 'xr' )

        plt.axvline( x = param.ID_TRAIN, color = 'k', linestyle = '-' )
        plt.axvline( x = param.ID_DAMAGE_START, color = 'k', linestyle = '-' )
        plt.grid( True )    
        plt.xlabel( "Observation" )
        plt.ylabel( "Natural frequency" )   
        plt.title( g.getRule() )
        