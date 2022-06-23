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


def pkt_type(pkt_num):
    frm_id = np.where(Arq_Simulator.accumu_packets >= pkt_num+1)[0][0]
    return Arq_Simulator.frametype(frm_id+1)


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
    Arq_finalt = Arq_Simulator.finalRcv_t
    Arq_pktdelay = np.array(Arq_Simulator.pktdelay)

    FEC_R_packets = np.array(FEC_Simulator.R_packets)
    FEC_R_packets2 = np.array(FEC_Simulator.R_packets2)
    FEC_pkts_per_frm = np.array(FEC_Simulator.pkts_per_frm)
    FEC_expired_pkts = np.array(FEC_Simulator.expired_pkts)
    FEC_lost_pkts = np.array(FEC_Simulator.lost_pkts)
    FEC_finalt = FEC_Simulator.finalRcv_t
    FEC_pktdelay = np.array(FEC_Simulator.pktdelay)

    MAB_R_packets = np.array(MAB_Simulator.R_packets)
    MAB_R_packets2 = np.array(MAB_Simulator.R_packets2)
    MAB_pkts_per_frm = np.array(MAB_Simulator.pkts_per_frm)
    MAB_expired_pkts = np.array(MAB_Simulator.expired_pkts)
    MAB_lost_pkts = np.array(MAB_Simulator.lost_pkts)
    MAB_finalt = MAB_Simulator.finalRcv_t
    MAB_pktdelay = np.array(MAB_Simulator.pktdelay)

    Arq_completeness = [1 if (Arq_R_packets[i] / Arq_pkts_per_frm[i]) >=
                        ((Arq_pkts_per_frm[i]-1)/Arq_pkts_per_frm[i]) else 0 for i in range(1000)]
    FEC_completeness = [1 if (FEC_R_packets[i] / FEC_pkts_per_frm[i]) >=
                        ((FEC_pkts_per_frm[i]-1)/FEC_pkts_per_frm[i]) else 0 for i in range(1000)]
    MAB_completeness = [1 if (MAB_R_packets[i] / MAB_pkts_per_frm[i]) >=
                        ((MAB_pkts_per_frm[i]-1)/MAB_pkts_per_frm[i]) else 0 for i in range(1000)]
    expired_pkts_no = [len(Arq_expired_pkts), len(
        FEC_expired_pkts), len(MAB_expired_pkts)]

    expired_keypackets = [len(np.where(np.array(list(map(pkt_type, Arq_expired_pkts))) == 1)[0]),
                          len(np.where(
                              np.array(list(map(pkt_type, FEC_expired_pkts))) == 1)[0]),
                          len(np.where(
                              np.array(list(map(pkt_type, MAB_expired_pkts))) == 1)[0])
                          ]
    # plt.bar(['ARQ', 'FEC', 'MAB'], expired_keypackets)

    # plt.hist(Arq_completeness)
    # plt.xlabel("Frame Completeness")
    # plt.ylabel("Frame Number")
    # plt.ylim([0, 1300])

    Arq_key_completeness = [Arq_completeness[i] for i in range(0, 1000, 12)]
    # plt.hist(Arq_key_completeness)
    # plt.xlabel("Frame Completeness")
    # plt.ylabel("Frame Number")
    # plt.ylim([0, 1300])

    FEC_key_completeness = [FEC_completeness[i] for i in range(0, 1000, 12)]
    # plt.hist(FEC_key_completeness)
    # plt.xlabel("Frame Completeness")
    # plt.ylabel("Frame Number")

    MAB_key_completeness = [MAB_completeness[i] for i in range(0, 1000, 12)]
    # plt.bar(['ARQ', 'FEC', 'MAB'], [sum(Arq_key_completeness),
    #         sum(FEC_key_completeness), sum(MAB_key_completeness)])
    # plt.ylabel('Number of Complete Key Frames')

    # plt.hist(FEC_completeness)
    # plt.xlabel("Frame Completeness")
    # plt.ylabel("Frame Number")
    # plt.ylim([0, 8000])

    # plt.hist(MAB_completeness)
    # plt.xlabel("Frame Completeness")
    # plt.ylabel("Frame Number")
    # plt.ylim([0, 8000])

    # plt.bar(['ARQ', 'FEC', 'MAB'], expired_pkts_no)

    # # plt.bar(['ARQ', 'FEC', 'MAB'], expired_keypackets)

    # plt.bar(['ARQ', 'FEC', 'MAB'], [
    #         0, len(FEC_lost_pkts), len(MAB_lost_pkts)])

    # plt.bar(['ARQ', 'FEC', 'MAB'], [Arq_Simulator.t, FEC_Simulator.t, MAB_Simulator.t])
    # plt.ylim([208000, 212000])

    plt.bar(['ARQ', 'FEC', 'MAB'], [np.mean(Arq_pktdelay),
            np.mean(FEC_pktdelay), np.mean(MAB_pktdelay)])
