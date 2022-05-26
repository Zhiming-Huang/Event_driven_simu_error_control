#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 18:59:23 2022

@author: zhiming
"""

import Discrete_Event_Sim_Arq
import Discrete_Event_Sim_FEC
import Discrete_Event_Sim_MAB

import pandas

import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
    Arq_Simulator = Discrete_Event_Sim_Arq.Arq_Sim()
    FEC_Simulator = Discrete_Event_Sim_FEC.Fec_Sim()
    MAB_Simulator = Discrete_Event_Sim_MAB.MAB_Sim()

    Arq_Simulator.sim_run()
    FEC_Simulator.sim_run()
    MAB_Simulator.sim_run()

    Arq_R_packets = np.array(Arq_Simulator.R_packets)
    Arq_R_packets2 = np.array(Arq_Simulator.R_packets2)
    Arq_pkts_per_frm = np.array(Arq_Simulator.pkts_per_frm)
    Arq_expired_pkts = np.array(Arq_Simulator.expired_pkts)

    FEC_R_packets = np.array(FEC_Simulator.R_packets)
    FEC_R_packets2 = np.array(FEC_Simulator.R_packets2)
    FEC_pkts_per_frm = np.array(FEC_Simulator.pkts_per_frm)
    FEC_expired_pkts = np.array(FEC_Simulator.expired_pkts)

    MAB_R_packets = np.array(MAB_Simulator.R_packets)
    MAB_R_packets2 = np.array(MAB_Simulator.R_packets2)
    MAB_pkts_per_frm = np.array(MAB_Simulator.pkts_per_frm)
    MAB_expired_pkts = np.array(MAB_Simulator.expired_pkts)

    Arq_completeness = Arq_R_packets / Arq_pkts_per_frm
    FEC_completeness = FEC_R_packets / FEC_pkts_per_frm
    MAB_completeness = MAB_R_packets / MAB_pkts_per_frm
    expired_pkts_no = [len(Arq_expired_pkts), len(
        FEC_expired_pkts), len(MAB_expired_pkts)]

    plt.hist(Arq_completeness)
    plt.xlabel("Frame Completeness")
    plt.ylabel("Frame Number")
    plt.ylim([0, 8000])

    plt.hist(FEC_completeness)
    plt.xlabel("Frame Completeness")
    plt.ylabel("Frame Number")
    plt.ylim([0, 8000])

    plt.hist(MAB_completeness)
    plt.xlabel("Frame Completeness")
    plt.ylabel("Frame Number")
    plt.ylim([0, 8000])

    plt.bar(['ARQ', 'FEC', 'MAB'], expired_pkts_no)
