#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 15:25:37 2022

@author: zhiming
"""

import queue
import numpy as np
import logging
from ErrorControl_EventSim.errctl_sim import Errctl_Sim, event
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


class Fec_Sim(Errctl_Sim):

    def __init__(self, tracefile="starwars.frames.old"):

        super().__init__(tracefile)

        # set the number of redundant pkts for each batch of packet
        self.redun_pkt_no = 1

        self.lost_pkt_no = 0
        self.lost_pkt = queue.Queue()

        self.fail_flag = False

    def __snd_pkts(self):
        while self.S_next < self.S_base + self.snd_wnd - self.redun_pkt_no:
            if self.S_next >= self.max_pkt_no:
                break
            one_trip = np.random.uniform(self.one_trip_min, self.one_trip_max)

            # determine pkt importance:
            frm_id = np.where(self.accumu_packets >= self.S_next+1)[0][0]
            pkt_imp = self.frametype(frm_id+1)

            # determine whether the packet is lost or not
            lost = np.random.binomial(1, self.drp_rate)
            self.drp_rate = 0.25 * self.drp_rate + \
                np.random.uniform(0, 0.05) * 0.75

            if lost:
                self.lost_pkt_no += 1
                self.lost_pkt.put_nowait(
                    event(self.t, self.t, 2, self.S_next, pkt_imp, self.t + self.delay_req, frm_id))
            else:
                # determine the arrival time
                self.event_list.put_nowait(
                    event(self.t + one_trip, self.t, 2, self.S_next, pkt_imp, self.t + self.delay_req, frm_id))
            #
            self.S_next += 1

        # for every 4 pkts sent, we check whether the aditional redundant pkt lost or not
        # if not, we check if the succssfully delivered pkts can recover the lost pkts
        if self.S_next % (self.snd_wnd - self.redun_pkt_no) == 0 and self.S_next > 0:
            # Check whether the redundant pkt lost or not
            redun_pkt_lost_no = np.random.binomial(
                self.redun_pkt_no, self.drp_rate)

            # if the delivered redun pkts can recover the lost pkts
            if self.lost_pkt_no + redun_pkt_lost_no <= self.redun_pkt_no:
                for i in range(self.lost_pkt_no):
                    pkt_evnt = self.lost_pkt.get_nowait()
                    one_trip = np.random.uniform(
                        self.one_trip_min, self.one_trip_max)
                    pkt_evnt.set_time(self.t + one_trip)
                    self.event_list.put_nowait(pkt_evnt)
            else:
                # generate timeout events
                for i in range(self.lost_pkt_no):
                    pkt_evnt = self.lost_pkt.get_nowait()
                    pkt_evnt.set_type(1)
                    pkt_evnt.set_time(self.t+self.rto)
                    self.event_list.put_nowait(pkt_evnt)

            # reset lost packet number and queues
            self.lost_pkt_no = 0
            self.lost_pkt = queue.Queue()

    def __event_lost(self, evnt):
        self.t = evnt.time
        # if packet lost and timeout, move snd window
        pkt_no = evnt.pkt_no
        self.lost_pkts.append(pkt_no)
        if pkt_no >= self.S_base:
            self.S_base = pkt_no

        self.__snd_pkts()

    def __event_ack(self, evnt):
        # receive an ack
        self.t = evnt.time
        self.rtt = self.t - evnt.snd_time
        self.rttvar = (1-self.beta) * self.rttvar + \
            self.beta * abs(self.srtt-self.rtt)
        self.srtt = (1-self.alpha) * self.srtt + \
            self.alpha * self.rtt
        self.rto = self.srtt + max(1, 4*self.rttvar)
        pkt_no = evnt.pkt_no

        if pkt_no >= self.S_base:
            self.S_base = pkt_no

        # Send packets
        self.__snd_pkts()

    def __event_pktarrival(self, evnt):
        # if packts arrive
        self.t = evnt.time
        # Get the current maximum packet number
        self.max_pkt_no = self.accumu_packets[evnt.frm_id]
        # Schedule next arrival event
        self.ind += 1
        if self.ind < self.num_frms:
            try:
                self.event_list.put_nowait(
                    self.arrival_events[self.ind])
            except queue.Full:
                print("Queue is full")

        # Send packets
        self.__snd_pkts()

    def sim_run(self):
        while True:
            # logger.debug(str(event_list.queue))
            # Get imminent event
            try:
                evnt = self.event_list.get_nowait()
                self.t = evnt.time
            except queue.Empty:
                if not self.lost_pkt.empty():
                    for i in range(self.lost_pkt_no):
                        pkt_evnt = self.lost_pkt.get_nowait()
                        pkt_evnt.set_type(1)
                        self.event_list.put_nowait(pkt_evnt)
                    self.lost_pkt_no = 0
                    self.lost_pkt = queue.Queue()
                    self.fail_flag = True
                else:
                    break
            else:
                if evnt.type == 0:
                    self.__event_pktarrival(evnt)

                elif evnt.type == 1:
                    self.__event_lost(evnt)

                elif evnt.type == 2:
                    self._Errctl_Sim__event_delivered(evnt)
                else:
                    self.__event_ack(evnt)


if __name__ == "__main__":
    Fec_Simulator = Fec_Sim()
    Fec_Simulator.sim_run()

    R_packets = Fec_Simulator.R_packets
    R_packets2 = Fec_Simulator.R_packets2
    expired_pkts = Fec_Simulator.expired_pkts
