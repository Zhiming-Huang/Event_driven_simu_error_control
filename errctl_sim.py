#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 19:08:34 2022

@author: Zhiming
"""
import numpy as np

class Errctl_Sim:
    def __init__(self, tracefile="starwars.frames.old"):
        # read the tracefile
        tracefile = open(tracefile, "r+")
        traces = tracefile.read().splitlines()[0:10000]
        traces = np.array(list(map(int, traces)))
        tracefile.close()