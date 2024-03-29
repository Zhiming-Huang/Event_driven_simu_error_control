#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 18:59:23 2022

@author: zhiming
"""

import Discrete_Event_Sim_Arq
import Discrete_Event_Sim_FEC2

import Discrete_Event_Sim_MAB

import pandas

import matplotlib.pyplot as plt
import numpy as np


def one_instance(num = 1000):
    Arq_Simulator = Discrete_Event_Sim_Arq.Arq_Sim(num_frms = num)
    FEC_Simulator = Discrete_Event_Sim_FEC2.Fec_Sim(num_frms = num)
    MAB_Simulator = Discrete_Event_Sim_MAB.MAB_Sim(num_frms = num)

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

    # Arq_completeness = [(Arq_R_packets[i] / Arq_pkts_per_frm[i])
    #                     for i in range(1000)]
    # FEC_completeness = [(FEC_R_packets[i] / FEC_pkts_per_frm[i])
    #                     for i in range(1000)]
    # MAB_completeness = [(MAB_R_packets[i] / MAB_pkts_per_frm[i])
    #                     for i in range(1000)]

    Arq_completeness = [
        1
        if (Arq_R_packets[i] / Arq_pkts_per_frm[i])
        >= ((Arq_pkts_per_frm[i] - 1) / Arq_pkts_per_frm[i])
        else 0
        for i in range(num)
    ]
    FEC_completeness = [
        1
        if (FEC_R_packets[i] / FEC_pkts_per_frm[i])
        >= ((FEC_pkts_per_frm[i] - 1) / FEC_pkts_per_frm[i])
        else 0
        for i in range(num)
    ]
    MAB_completeness = [
        1
        if (MAB_R_packets[i] / MAB_pkts_per_frm[i])
        >= ((MAB_pkts_per_frm[i] - 1) / MAB_pkts_per_frm[i])
        else 0
        for i in range(num)
    ]
    expired_pkts_no = [
        len(Arq_expired_pkts),
        len(FEC_expired_pkts),
        len(MAB_expired_pkts),
    ]

    def pkt_type(pkt_num):
        frm_id = np.where(Arq_Simulator.accumu_packets >= pkt_num + 1)[0][0]
        return Arq_Simulator.frametype(frm_id + 1)

    expired_keypackets = [
        len(np.where(np.array(list(map(pkt_type, Arq_expired_pkts))) == 1)[0]),
        len(np.where(np.array(list(map(pkt_type, FEC_expired_pkts))) == 1)[0]),
        len(np.where(np.array(list(map(pkt_type, MAB_expired_pkts))) == 1)[0]),
    ]
    # plt.bar(['ARQ', 'FEC', 'MAB'], expired_keypackets)

    # plt.hist(Arq_completeness)
    # plt.xlabel("ARQ Frame Completeness")
    # plt.ylabel("Frame Number")
    # plt.ylim([0, 1300])

    Arq_key_completeness = [Arq_completeness[i] for i in range(0, num, 12)]
    # plt.hist(Arq_key_completeness)
    # plt.xlabel("Frame Completeness")
    # plt.ylabel("Frame Number")
    # plt.ylim([0, 1300])

    FEC_key_completeness = [FEC_completeness[i] for i in range(0, num, 12)]
    # plt.hist(FEC_key_completeness)
    # plt.xlabel("Frame Completeness")
    # plt.ylabel("Frame Number")

    MAB_key_completeness = [MAB_completeness[i] for i in range(0, num, 12)]
    # plt.bar(['ARQ', 'FEC', 'MAB'], [sum(Arq_key_completeness),
    #          sum(FEC_key_completeness), sum(MAB_key_completeness)])
    # plt.ylabel('Number of Complete Key Frames')
    Frame_completeness = [
        sum(Arq_completeness),
        sum(FEC_completeness),
        sum(MAB_completeness),
    ]
    Key_frame_completeness = [
        sum(Arq_key_completeness),
        sum(FEC_key_completeness),
        sum(MAB_key_completeness),
    ]
    pkt_ave_delay = [
        np.mean(Arq_pktdelay),
        np.mean(FEC_pktdelay),
        np.mean(MAB_pktdelay),
    ]
    return [
        Frame_completeness,
        Key_frame_completeness,
        expired_pkts_no,
        expired_keypackets,
        pkt_ave_delay,
    ]
    # plt.hist(FEC_completeness)
    # plt.xlabel("FEC Frame Completeness")
    # plt.ylabel("Frame Number")
    # plt.ylim([0, 8000])

    # plt.hist(MAB_completeness)
    # plt.xlabel("MAB Frame Completeness")
    # plt.ylabel("Frame Number")
    # plt.ylim([0, 8000])
    # plt.bar(['ARQ', 'FEC', 'MAB'], [sum(Arq_completeness), sum(FEC_completeness), sum(MAB_completeness)])
    # plt.bar(['ARQ', 'FEC', 'MAB'], expired_pkts_no)

    # plt.bar(['ARQ', 'FEC', 'MAB'], expired_keypackets)

    # plt.bar(['ARQ', 'FEC', 'MAB'], [
    #         0, len(FEC_lost_pkts), len(MAB_lost_pkts)])

    # plt.bar(['ARQ', 'FEC', 'MAB'], [Arq_Simulator.t, FEC_Simulator.t, MAB_Simulator.t])
    # plt.ylim([208000, 212000])


if __name__ == "__main__":
    F_complenetess_num = np.zeros([1000,3])
    F_key_completeness_num = np.zeros([1000,3])
    E_pkt_no_num = np.zeros([1000,3])
    E_key_pkt_no_num = np.zeros([1000,3])
    P_Ave_Delay_num = np.zeros([1000,3])    
    for num in range(0,1000):
        F_complenetess = np.zeros([3])
        F_key_completeness = np.zeros([3])
        E_pkt_no = np.zeros([3])
        E_key_pkt_no = np.zeros([3])
        P_Ave_Delay = np.zeros([3])
        for i in range(1, 2):
            [
                Frame_completeness,
                Key_frame_completeness,
                expired_pkts_no,
                expired_keypackets,
                pkt_ave_delay,
            ] = one_instance(num+1)
            F_complenetess += np.array(Frame_completeness)
            F_key_completeness += np.array(Key_frame_completeness)
            E_pkt_no += np.array(expired_pkts_no)
            E_key_pkt_no += np.array(expired_keypackets)
            P_Ave_Delay += np.array(pkt_ave_delay)
    
            F_complenetess_num[num,:] = F_complenetess / (num+1)
            F_key_completeness_num[num,:] = F_key_completeness / (num+1)
            E_pkt_no_num[num,:] = E_pkt_no / 1
            E_key_pkt_no_num[num,:] = E_key_pkt_no / 1
            P_Ave_Delay_num[num,:] = P_Ave_Delay / 1
        

    # def plot_completeness(F_complenetess, F_key_completeness):
    #     fig, ax1
    # plt.bar(['ARQ', 'FEC', 'MAB'], F_complenetess/1000)
    # plt.ylim([0.95,1])
    # plt.bar(['ARQ', 'FEC', 'MAB'], F_key_completeness/84)
    # plt.ylim([0.95,1])
    # plt.bar(['ARQ', 'FEC', 'MAB'], E_key_pkt_no)
    # plt.bar(['ARQ', 'FEC', 'MAB'], P_Ave_Delay)
    # plt.ylim([25, 35])
    def draw_bars(bars, file_name, args=None):
        fig, ax = plt.subplots()
        barhandler = ax.bar(["ARQ", "FEC", "MAB"], bars)
        ax.bar_label(barhandler)
        if args == 1:
            ax.set_ylabel("Packet_averaged_delay (ms)")
        if args == 2:
            ax.set_ylim([0.95, 1])
        plt.savefig(file_name, format="eps")

    # draw_bars(F_complenetess / 1000, "Sce2_Frame_completeness.eps", 2)
    # draw_bars(F_key_completeness / 84, "Sce2_Key_Frame_completeness.eps", 2)
    # draw_bars(E_key_pkt_no, "Sce2_Key_packet_expired.eps")
    # draw_bars(P_Ave_Delay, "Sce2_packet_delay.eps", 1)


# plt.bar(['ARQ', 'FEC', 'MAB'], [np.mean(Arq_pktdelay),
#         np.mean(FEC_pktdelay), np.mean(MAB_pktdelay)])

    def draw_sensitivity(lines, file_name, args=None):
        fig, ax = plt.subplots()
        barhandler1 = ax.plot(lines[:,0], label= 'ARQ')
        barhandler2 = ax.plot(lines[:,1], label= 'FEC')
        barhandler3 = ax.plot(lines[:,2], label= 'MAB')
        ax.set_ylabel("Frame Completeness")
        ax.set_xlabel("The number of rounds")
        plt.legend()
        plt.savefig(file_name, format="eps")