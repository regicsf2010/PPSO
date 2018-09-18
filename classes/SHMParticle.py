import numpy as np
import copy

import util.parameters as param

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
        self.evaluate()
        
        # start velocity with 0
        self.v = np.zeros(self.n)

        # deep copy the current position as best personal and fitness
        self.m = copy.deepcopy(self.x)
        self.fit_m = self.fit_x
        
    # Evaluate the particle as accuracy    
    def evaluate(self):
        self.typeI, self.typeII = self.f(self.x)
        self.fit_x = sum([ (1/100) * self.typeI, (99/100) * self.typeII])

    # Deep copy of this object
    def getCopy(self):
        return copy.deepcopy(self)
    
    # Verify if the particle has the rule enabled
    def isRule(self):
        n = [i for i in range(2, self.n, 3) if self.x[i] <= param.TACT] # list
        return True if len(n) != 0 else False
    
    # Convert the particle to the rule
    def getRule(self):
        r = "IF"
        nv = 1
        for i in range(0, self.n, 3):
            if self.x[i+2] <= param.TACT:
                r += " x" + str(nv) + (" < " if self.x[i+1] < param.TSIG else " > ") + str("{:.3f}".format(self.x[i])) + " AND"                
            nv += 1
        return r[:-4] # take-off the last substring (" AND")
    
    # This method is used to print this object
    def __str__(self):
        return "x: " + str([round(i, 3) for i in self.x]) + \
               "\nfit_x: " + str(self.fit_x) + \
               "\nerr: " + str([self.typeI, self.typeII]) + \
               "\nrule: " + self.getRule()