#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 18:59:23 2022

@author: zhiming
"""


import ErrorControl_EventSim

import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
    Arq_Simulator = ErrorControl_EventSim.Discrete_Event_Sim_Arq.Arq_Sim()
    FEC_Simulator = ErrorControl_EventSim.Discrete_Event_Sim_FEC.Fec_Sim()
    MAB_Simulator = ErrorControl_EventSim.Discrete_Event_Sim_MAB.MAB_Sim()

    Arq_Simulator.sim_run()
    FEC_Simulator.sim_run()
    MAB_Simulator.sim_run()

    Arq_R_packets = np.array(Arq_Simulator.R_packets)
    Arq_R_packets2 = np.array(Arq_Simulator.R_packets2)
    Arq_pkts_per_frm = np.array(Arq_Simulator.pkts_per_frm)
    Arq_finalt = Arq_Simulator.finalRcv_t

    FEC_R_packets = np.array(FEC_Simulator.R_packets)
    FEC_R_packets2 = np.array(FEC_Simulator.R_packets2)
    FEC_pkts_per_frm = np.array(FEC_Simulator.lost_pkts)
    FEC_finalt = FEC_Simulator.finalRcv_t

    MAB_R_packets = np.array(MAB_Simulator.R_packets)
    MAB_R_packets2 = np.array(MAB_Simulator.R_packets2)
    MAB_pkts_per_frm = np.array(MAB_Simulator.pkts_per_frm)
    MAB_pkts_per_frm = np.array(MAB_Simulator.lost_pkts)
    MAB_finalt = MAB_Simulator.finalRcv_t

    # Arq_completeness = Arq_R_packets / Arq_pkts_per_frm
    # plt.hist(Arq_completeness)
    # plt.xlabel("Frame Completeness")
    # plt.ylabel("Frame Number")
