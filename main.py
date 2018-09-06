#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 11:54:10 2018

@author: Reginaldo Santos
"""

from concurrent.futures import ProcessPoolExecutor

from classes.Swarm import Swarm
import util.parameters as param
import util.functions as util


def parallelEvaluation(s):
    pool = ProcessPoolExecutor(param.NTHREAD)
    futures = []
    for i in range(param.NTHREAD):
        futures.append(pool.submit(util.evaluate, s, i))


""" PSO """
s = Swarm(util.f, param.NPARTICLE)
print(s)