import numpy as np
import copy

import util.parameters as param

# Normalize data by minmax
def norm(data):
    for j in range(param.NCOL):
        m = min(data[0:3931, j])
        diff = max(data[0:3931, j]) - m
        data[0:3931, j] = (data[0:3931, j] - m) / diff
    return data

# Load database: z24
data = np.genfromtxt(param.FILENAME, delimiter = ',')
data = norm(data)

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
        # self.evaluate()
        self.typeI = self.typeII = self.fit_x = 10000
        
        # start velocity with 0
        self.v = np.zeros(self.n)

        # deep copy the current position as best personal and fitness
        self.m = copy.deepcopy(self.x)
        self.fit_m = self.fit_x
        
    # Evaluate the particle as accuracy    
    def evaluate(self,op):
        self.typeI, self.typeII = self.f(self.x,op)
        self.fit_x = self.typeI + self.typeII 
        # self.fit_x = abs( self.typeI - round( param.ID_TRAIN * 0.15 ) ) + self.typeII
    
    def eval(s,op):
        for id in range(param.NPARTICLE):
            x = s.particles[id].x
            
            typeI = typeII = 0 # no damage
            
            flag = 0
            
            cols = [i - 2 for i in range(2, 12, 3) if x[i] <= param.TACT]
            if(len(cols) == 0):
                cols = 3 * np.random.randint(4)
                x[cols+2] = np.random.random() * param.TACT
                cols = list([cols])
            
            if(x[param.DIM-2] <= param.TRUL):
                flag += 1
                cols2 = [i - 2 for i in range(14, 24, 3) if x[i] <= param.TACT]
                if(len(cols2) == 0):
                    cols2 = 3 * np.random.randint(4) + 12
                    x[cols2+2] = np.random.random() * param.TACT
                    cols2 = list([cols2])
                    
            if(x[param.DIM-1] <= param.TRUL and flag == 1):  
                flag += 1
                cols3 = [i - 2 for i in range(26, param.DIM-2, 3) if x[i] <= param.TACT]
                if(len(cols3) == 0):
                    cols3 = 3 * np.random.randint(4) + 24
                    x[cols3+2] = np.random.random() * param.TACT
                    cols3 = list([cols3])
                    
            if(op == 0):
                aux = 0
                for i in range(param.ID_TRAIN+312*1):
                    t = 0 # no damage
                    if(i == param.ID_TRAIN):
                        aux = 809
                        
                    for j in cols:
                        if(x[j+1] <= param.TSIG):
                            if(data[i+aux][int(j/3)] > x[j]):
                                t = 1 # damage
                                break 
                        else:
                            if(data[i+aux][int(j/3)] < x[j]):
                                t = 1 # damage
                                break
                    
                    if(t == 1 and flag > 0):
                        for j in cols2:
                            if(x[j+1] <= param.TSIG):
                                if(data[i+aux][int(j/3-4)] > x[j]):
                                    t += 1 # damage
                                    break 
                            else:
                                if(data[i+aux][int(j/3-4)] < x[j]):
                                    t += 1 # damage
                                    break
                        
                        if(t == 2 and flag > 1):
                            for j in cols3:                              
                                if(x[j+1] <= param.TSIG):
                                    if(data[i+aux][int(j/3-8)] > x[j]):
                                        t += 1 # damage
                                        break 
                                else:
                                    if(data[i+aux][int(j/3-8)] < x[j]):
                                        t += 1 # damage
                                        break
                                    
                    if(t == 1+flag and i+aux < param.ID_DAMAGE_START):
                        typeI += 1
                    elif(t < 1+flag and i+aux >= param.ID_DAMAGE_START):
                        typeII += 1       
            
            else:
                for i in range(param.NLIN):
                    t = 0 # no damage                        
                    for j in cols:
                        if(x[j+1] <= param.TSIG):
                            if(data[i][int(j/3)] > x[j]):
                                t = 1 # damage
                                break 
                        else:
                            if(data[i][int(j/3)] < x[j]):
                                t = 1 # damage
                                break
                            
                    if(t == 1 and flag > 0):
                        for j in cols2:
                            if(x[j+1] <= param.TSIG):
                                if(data[i][int(j/3-4)] > x[j]):
                                    t += 1 # damage
                                    break 
                            else:
                                if(data[i][int(j/3-4)] < x[j]):
                                    t += 1 # damage
                                    break
                        
                        if(t == 2 and flag > 1):
                            for j in cols3:                                                         
                                if(x[j+1] <= param.TSIG):
                                    if(data[i][int(j/3-8)] > x[j]):
                                        t += 1 # damage
                                        break 
                                else:
                                    if(data[i][int(j/3-8)] < x[j]):
                                        t += 1 # damage
                                        break
                                        
                    if(t == 1+flag and i < param.ID_DAMAGE_START):
                        typeI += 1
                    elif(t < 1+flag and i >= param.ID_DAMAGE_START):
                        typeII += 1       
            
            s.particles[id].fit_x = typeI + typeII
            s.particles[id].typeI = typeI
            s.particles[id].typeII = typeII               
                
    # Deep copy of this object#
    def getCopy(self):
        return copy.deepcopy(self)
    
    # Verify if the particle has the rule enabled
    def isRule(self):
        n = [i for i in range(2, self.n, 3) if self.x[i] <= param.TACT] # list
        return True if len(n) != 0 else False
    
    # Convert the particle to the rule
    def getRule(self):
        r = "IF ("
        nv = 1
        flag = 0
        for i in range(0, self.n-2, 3):
            if self.x[i+2] <= param.TACT:
                r += " x" + str(nv) + (" < " if self.x[i+1] < param.TSIG else " > ") + str("{:.3f}".format(self.x[i])) + " AND"
            
            nv += 1
                    
            if(nv == 5): 
                if(flag == 2):
                    break 
                if(self.x[param.DIM-(2-flag)] > param.TRUL):
                    break
                flag += 1
                r = r[:-4] + " ) OR ("
                nv = 1
            
        return r[:-4] + " )" 
    
    # This method is used to print this object
    def __str__(self):
        return "x: " + str([round(i, 3) for i in self.x]) + \
               "\nfit_x: " + str(self.fit_x) + \
               "\nerr: " + str([self.typeI, self.typeII]) + \
               "\nrule: " + self.getRule()