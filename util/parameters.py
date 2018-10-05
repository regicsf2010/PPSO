NITERATION = 100
NPARTICLE = 20
NTHREAD = 4

# Dimension coefficients
DBSIZE = 4
NCLA = 1
DIM = 3 * DBSIZE * NCLA + NCLA 

# Search space and constraints
RANGE = ( 0, 1 )
VMAX = ( RANGE[1] - RANGE[0] ) / 2.0

# PSO coefficients
C1 = 2.05
C2 = 2.05
WRANGE = ( .4, .9 )
W = [ WRANGE[1] - ( WRANGE[1] - WRANGE[0] ) * i / \
                                    NITERATION for i in range( NITERATION ) ]

# Rule specifications
PSIG = .5
PCON = .0
PCLA = .0
LIMITS = ( .01, .99 ) # lower and upper limits for polishing the rule

# Database specifications
FILENAME1 = "database/database.csv"
FILENAME2 = "database/artificialdata.csv"
NLIN = 3932
NCOL = 4
NART = 312
ID_TRAIN = 3123
ID_DAMAGE_START = 3471
