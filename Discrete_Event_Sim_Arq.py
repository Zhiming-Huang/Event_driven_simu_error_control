#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 15:25:37 2022

@author: zhiming
"""

import queue
import numpy as np
import logging
from errctl_sim import Errctl_Sim

#from SplayTree import *

# set logger
# logger = logging.getLogger("arq-simulator")
# logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
# create console handler and set level to debug
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)

# create formatter
# formatter = logging.Formatter(
#     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
# ch.setFormatter(formatter)

# add ch to logger
# logger.addHandler(ch)


class Arq_Sim(Errctl_Sim):
    def __init__(self, tracefile="starwars.frames.old"):
        super().__init__(tracefile)


if __name__ == "__main__":
    Arq_Simulator = Arq_Sim()
    Arq_Simulator.sim_run()

    R_packets = Arq_Simulator.R_packets
    R_packets2 = Arq_Simulator.R_packets2
