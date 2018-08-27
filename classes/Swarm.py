from classes.Particle import Particle
import math

class Swarm:
    # size of the swarm
    n = -1
    # particles
    particles = []
    # objective function
    f = None
        
    def __init__(self, n, f):
        self.n = n
        self.f = f        
    
    def initialize(self):
        for i in range(self.n):
            self.particles.append(Particle(self.f))            
    
    def avgFitness(self):
        return sum(p.fit_x for p in self.particles) / float(self.n)
    
    def stdFitness(self, avg = None):
        if avg is None:
            avg = self.avgFitness()
        return math.sqrt(sum((p.fit_x - avg)**2 for p in self.particles) / float(self.n - 1))
            
        
    def printFitness(self):
        print(["{:.4e}".format(p.fit_x) for p in self.particles])