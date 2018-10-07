import util.parameters as param

import numpy as np

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

artificialDB = np.genfromtxt( param.FILENAME2, delimiter = ',' )
data = np.concatenate( ( data, artificialDB ) )

# Objective function: errors type I and type II
def f( x, op ):
    global cols
    cols = getCols( x )
    
    nActClau = getNActivatedClauses( x )
    
    typeI = typeII = 0 # no damage
    if( op == 0 ):
        # Training     
        classLabels = [] # post-classification labels
        pos = 0
        for i in range( param.ID_TRAIN + param.NART ):
            if( i == param.ID_TRAIN ):
                pos = 809
            t = getT( x, i + pos )   
            
            if( t == nActClau and i + pos < param.ID_DAMAGE_START - 1 ):
                typeI += 1
            elif( t < nActClau and i + pos >= param.ID_DAMAGE_START - 1 ):
                typeII += 1                
    else: 
        # Testing  
        classLabels = np.zeros( param.NLIN );
        for i in range( param.NLIN ):
            t = getT( x, i )   
            
            if( t == nActClau and i < param.ID_DAMAGE_START - 1 ):
                typeI += 1
                classLabels[i] = 1
            elif( t < nActClau and i >= param.ID_DAMAGE_START - 1 ):
                typeII += 1
                classLabels[i] = 1
            else:
                classLabels[i] = 0
                    
    return [ typeI, typeII, classLabels ]

#
def getCols( x ):
    nActClau = getNActivatedClauses( x )
    if( nActClau == 0 ):
        nActClau = 1
        x[ ( param.DIM - param.NCLA ) +  np.random.randint( param.NCLA ) ] = \
                                                np.random.random() * param.PCLA
        
    cols = np.ones( ( param.NCLA, param.DBSIZE ) ) * -1
                
    pos = 2
    for i in range( param.DIM - param.NCLA, param.DIM, 1 ):
        if( x[i] <= param.PCLA ):
            aux = [ j - 2 for j in range( pos, pos+10, 3 ) \
                                                        if x[j] <= param.PCON ]
            if( len( aux ) == 0 ):
                x, aux = getActivatedCondition( x, pos )
                
            cols[ i - ( param.DIM - param.NCLA ), :len( aux ) ] = aux
                        
        pos += 12
    return cols

def getT( x, id ):  
    t = 0 # no damage
    for i in range( param.NCLA ):
        if( cols[ i, 0 ] != -1 ):
            aux = cols[ i, cols[i,:] > -1 ]
            for j in aux:                
                if( x[ int(j) + 1 ] <= param.PSIG ):
                    if( data[id][ int( j/3 - 4*i ) ] > x[int(j)] ):
                        t += 1 # damage
                        break
                else:
                    if( data[id][ int( j/3 - 4*i ) ] < x[int(j)] ):
                        t += 1 # damage
                        break
    return t
    
#
def getNActivatedClauses( x ):
    n = 0
    for i in range( param.DIM - param.NCLA, param.DIM, 1 ):
        if( x[i] <= param.PCLA ):
            n += 1    
    return n

#
def getActivatedCondition( x, pos ):
    cols = 3 * np.random.randint( param.NCOL ) + pos - 2
    x[ cols + 2 ] = np.random.random() * param.PCON 
    cols = list( [ cols ] ) 
    return x, cols

#
def polishRule( s ):
    for i in range( param.NPARTICLE ):
        for j in range( 0, param.DIM - ( param.NCLA - 1 ), 3 ):
            if( s.particles[i].x[j] < param.LIMITS[0] or s.particles[i].x[j] > \
                                                            param.LIMITS[1] ):
                s.particles[i].x[j] = np.random.random()

def diversity( s, L ):
    x = s.particles
    x = [ i.x for i in x ]
    avg = np.mean( x, 0 )
    return np.sum( np.sqrt( np.sum( ( x - avg ) ** 2, 1 ) ) ) / ( len( x ) * L )
                      
# def evaluate( s, i, op ):
#     n = param.NPARTICLE / param.NTHREAD
#     start = int( i * n )
#     end = int( i * n + n )
#     for j in range( start, end ):
#         s.particles[j].evaluate( op )
#     return [ start, end, s.particles[ start:end ] ]
