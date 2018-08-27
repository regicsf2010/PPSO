import numpy as np
import copy

import util.parameters as param


class Particle:
    # position
    x = []
    fit_x = np.Inf

    # personal best memory
    m = []
    fit_m = np.Inf

    # velocity
    v = []

    # objective function
    f = None
    
    # contructor
    def __init__(self, f, x = None):
        # store objective function
        self.f = f
        
        # start position at random
        if x is not None:
            self.x = x * np.ones(param.DIM) # change to array-like
        else:               
            self.x = param.RANGE[0] + (param.RANGE[1] - param.RANGE[0]) * np.random.random(param.DIM)
            
        # evaluate position
        self.evaluate()

        # start velocity with 0
        self.v = np.zeros(param.DIM)

        # deep copy the current position as best personaland fitness
        self.m = copy.deepcopy(self.x)
        self.fit_m = self.fit_x
        
    def __str__(self):
        return "X: " + str([round(i, 4) for i in self.x]) + \
               "\nFITX: " + str("{:.4e}".format(self.fit_x))
#               "\nM: " + str([round(i, 4) for i in self.m]) + \
#               "\nFITM: " + str("{:.4e}".format(self.fit_m)) + \
#               "\nV: " + str([round(i, 4) for i in self.v])
               
    def getCopy(self):
        return copy.deepcopy(self)
    
    def evaluate(self):
        self.fit_x = self.f(self.x)