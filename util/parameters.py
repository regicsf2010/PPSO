NITERATION = 1000
NPARTICLE = 20
NTHREAD = 4

# Dimension specs
DBSIZE = 4
DIM = 3 * DBSIZE

# Search space and constraints
RANGE = (0, 1)
VMAX = (RANGE[1] - RANGE[0]) / 2.0

# PSO coefficients
C1 = 2.05
C2 = 2.05
WRANGE = (.4, .9)
W = [WRANGE[1] - (WRANGE[1] - WRANGE[0]) * i / NITERATION for i in range(NITERATION)]

# Rule specs
TSIG = .5
TACT = .5

# Database specs
FILENAME = "database/database.csv"
NLIN = 3932
NCOL = 4
ID_DAMAGE_START = 3463