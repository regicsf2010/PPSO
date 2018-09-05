from classes.Particle import Particle
import util.parameters as param

import math

class Swarm:
       
    def __init__(self, f, n = None):
        if n is not None:
            self.n = n
        else:
            self.n = param.NPARTICLE
        
        self.f = f
        self.particles = []
        
    def initialize(self):
        for i in range(self.n):
            self.particles.insert(i, Particle(self.f))
    
    def avgFitness(self):
        return sum(p.fit_x for p in self.particles) / float(self.n)
    
    def stdFitness(self, avg = None):
        if avg is None:
            avg = self.avgFitness()
        return math.sqrt(sum((p.fit_x - avg)**2 for p in self.particles) / float(self.n - 1))
            
        
    def printFitness(self):
        print(["{:.4e}".format(p.fit_x) for p in self.particles])