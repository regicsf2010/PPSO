from classes.Swarm import Swarm
from classes.PSOSteps import PSOSteps
from classes.PSOPlots import PSOPlots
import util.parameters as param
import util.functions as util

# from concurrent.futures import ProcessPoolExecutor, as_completed
import matplotlib.pyplot as plt
import numpy as np

# def parallelEvaluation( s ):
#     pool = ProcessPoolExecutor( param.NTHREAD )
#     futures = []
#     for i in range( param.NTHREAD ):
#         futures.append( pool.submit( util.evaluate, s, i, 0 ) )
#     for x in as_completed( futures ):
#         s.particles[ x.result()[0] : x.result()[1] ] = x.result()[2]
            
""" Particle Swarm Optimization | Structural Health Monitoring """

def main():
    s = Swarm( util.f, param.NPARTICLE  )
    pso = PSOSteps( s )
    plot = PSOPlots( range( param.NITERATION ) )
    
    util.polishRule( s )
    
    # Evaluate training data set
    # parallelEvaluation( s )
    pso.evaluate( 0 )
        
    g = pso.getGlobalBest()
    
    avg = np.zeros( param.NITERATION )
    std = np.zeros( param.NITERATION )
    bfit = np.zeros( param.NITERATION )
    div = np.zeros( param.NITERATION )
    L = np.linalg.norm( np.ones( param.DIM ) * ( param.RANGE[1] - \
                                                            param.RANGE[0] ) )
    
    for i in range( param.NITERATION ):
        pso.updateVelocity( i, g )
        
        pso.move()
        
        util.polishRule( s )
        
        # parallelEvaluation( s )
        pso.evaluate( 0 )
        
        pso.updatePBAndGB( g )
        
        avg[i] = s.avgFitness()
        std[i] = s.stdFitness( avg[i] )
        bfit[i] = g.fit_x
        div[i] = util.diversity( s, L )     
        
        # iteration | typeI+typeII=fitness | # of clauses | decision rule        
        nActClau = util.getNActivatedClauses( g.x )
        print( str(i) + ",", ( str( g.typeI ) + "+" + str( g.typeII ) + "=" + \
                    str( g.fit_x ) ) + ",", str( nActClau ) + ",", g.getRule() )  
    
    # Evaluate test data set    
    # type I error | type I error | post-classification labels      
    g.typeI, g.typeII, classLabels = util.f( g.x, 1 ) 
               
    print( g ) 
 
    plt.figure()
    plot.bestFitness( 221, bfit ) 
    plot.avgFitness( 222, avg, std )
    plot.divSwarm( 223, div )    
    plot.DBMisclass( 224, g, classLabels )
    plt.show()

if __name__ == '__main__':
    main()
    