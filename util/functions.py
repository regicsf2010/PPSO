# Objective functions to be optimized
from math import cos, pi

def sphere(x):
    return sum(i * i for i in x)

def rastrigin(x):
    return 10 * len(x) + sum(i * i - 10 * cos(2 * pi * i) for i in x)

def himmelblau(x):
    return (x[0]**2 + x[1] - 11)**2 + (x[0] + x[1]**2 - 7)**2