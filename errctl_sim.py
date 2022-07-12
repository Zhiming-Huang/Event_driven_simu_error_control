#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 19:08:34 2022

@author: Zhiming
"""
import numpy as np
import queue
import logging


class event:
    def __init__(self,  evt_time, snd_time, evt_type, pkt_no=None, pkt_imp=None, pkt_delay_req=None, frm_id=None):
        # evt_type 0 for pkt arrival, 1 for timeout, 2 for delivered, 3 for ACK
        self.time = evt_time
        self.snd_time = snd_time
        self.type = evt_type
        self.pkt_no = pkt_no
        self.pkt_imp = pkt_imp
        self.delay_req = pkt_delay_req
        self.frm_id = frm_id
        self.ifretran = False

    def __lt__(self, other):
        return self.time < other.time

    def set_type(self, evt_type):
        self.type = evt_type

    def set_time(self, evt_time):
        self.time = evt_time

    def set_sndtime(self, snd_time):
        self.snd_time = snd_time

    def set_retran(self):
        self.ifretran = True


class Errctl_Sim:
    def __init__(self, tracefile="starwars.frames.old"):
        # read the tracefile
        with open(tracefile, 'r+') as infile:
            self.traces = infile.read().splitlines()[0:1000]
            self.traces = np.array(list(map(int, self.traces)))

        self.pkt_size = 1000*8  # 1000 bytes per packet
        self.pkts_per_frm = np.array(
            [int(np.ceil(item/(self.pkt_size)))+1 for item in self.traces])
        self.accumu_packets = np.cumsum(self.pkts_per_frm)
        # Determine the generation time for each frame
        self.num_frms = len(self.traces)
        self.frame_spawn = np.zeros(self.num_frms) + 42
        self.frame_spawn[0] = 0
        self.frame_spawn_time = np.cumsum(self.frame_spawn)

        self.arrival_events = []
        for i in range(self.num_frms):
            self.arrival_events.append(
                event(self.frame_spawn_time[i], 0, 0, frm_id=i))

        self.__set_network()

    def __set_network(self):
        # sending window control
        self.snd_wnd = 10
        self.S_base = 0
        self.S_next = 0

        self.R_packets = np.zeros(self.num_frms)
        self.R_packets2 = np.zeros(self.accumu_packets[-1])
        self.R_packets3 = np.zeros(self.accumu_packets[-1])
        self.pkt_drprate = np.zeros(self.accumu_packets[-1])

        self.ACKed_pkts = queue.PriorityQueue()
        self.pktdelay = np.zeros(self.accumu_packets[-1])
        self.expired_pkts = []
        self.lost_pkts = []
        self.finalRcv_t = 0
        self.max_pkt_no = 0

        self.drp_rate = 0.01
        self.max_drp_rate = 0.05
        self.max_pkt_no = 0
        self.delay_req = 180
        self.one_trip_min = 20
        self.one_trip_max = 40

        # retran RCF6298 https://www.saminiir.com/lets-code-tcp-ip-stack-5-tcp-retransmission/
        self.srtt = 2*self.one_trip_max  # smoothed round-trip time
        self.rttvar = self.one_trip_max  # round-trip time variation
        self.rto = self.one_trip_max  # retransmission timeout
        self.alpha = 0.125
        self.beta = 0.25

        self.t = 0
        self.ind = 0
        self.event_list = queue.PriorityQueue()
        self.event_list.put_nowait(self.arrival_events[self.ind])

    @staticmethod
    def frametype(frm_num):
        # 1 for I, 2 for B, and P for 3
        ret = frm_num % 12
        if ret == 1:
            return 1
        elif 1 < ret < 4 and 4 < ret < 7 and 7 < ret < 10 and 10 < ret <= 12:
            return 2
        else:
            return 3

    def __snd_pkts(self):
        while self.S_next < self.S_base + self.snd_wnd:
            if self.S_next >= self.max_pkt_no:
                break
            one_trip = np.random.uniform(
                self.one_trip_min, self.one_trip_max)

            # determine pkt importance:
            frm_id = np.where(
                self.accumu_packets >= self.S_next+1)[0][0]
            pkt_spawn_time = self.frame_spawn_time[frm_id]
            pkt_imp = self.frametype(frm_id+1)

            self.pkt_drprate[self.S_next] = self.drp_rate

            # determine whether the packet is lost or not
            lost = np.random.binomial(1, self.drp_rate)

            self.drp_rate = 0.25 * self.drp_rate + \
                np.random.uniform(0, 0.05) * 0.75

            if lost:
                # if packet is lost, an timeout event is generated
                self.event_list.put_nowait(
                    event(self.t + self.rto, self.t, 1, self.S_next, pkt_imp, pkt_spawn_time + self.delay_req, frm_id))

            else:
                # determine the arrival time
                self.event_list.put_nowait(
                    event(self.t + one_trip, self.t, 2, self.S_next, pkt_imp, pkt_spawn_time + self.delay_req, frm_id))
            self.S_next += 1

    def __event_pktarrival(self, evnt):
        # if packts arrive at the sender side
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

    def __event_lost(self, evnt):
        # if packet lost and timeout, retransmit packet
        self.t = evnt.time
        lost = np.random.binomial(1, self.drp_rate)
        one_trip = np.random.uniform(
            self.one_trip_min, self.one_trip_max)
        self.drp_rate = 0.25 * self.drp_rate + \
            np.random.uniform(0, 0.05) * 0.75
        if lost:
            # if packet is lost, an timeout event is generated
            evnt.set_time(self.t + self.rto)
            # evnt.set_sndtime(self.t)
            # set the event type to timeout event
            evnt.set_type(1)
            # add event to the event list
            self.event_list.put_nowait(evnt)

        else:
            # determine the arrival time
            evnt.set_time(self.t + one_trip)
            evnt.set_retran()
            # set the event type to the arrival event
            evnt.set_type(2)
            # add event to the event list
            self.event_list.put_nowait(evnt)

    def __event_delivered(self, evnt):
        # if packet is successfully received by the receiver
        self.t = evnt.time
        self.finalRcv_t = evnt.time
        pkt_no = evnt.pkt_no
        self.pktdelay[pkt_no] = self.t - evnt.snd_time
        one_trip = np.random.uniform(
            self.one_trip_min, self.one_trip_max)
        # send ACK, set the event to ack event
        evnt.set_type(3)
        evnt.set_time(self.t + one_trip)
        self.event_list.put_nowait(evnt)

        # receive packets that are not expired
        frm_id = evnt.frm_id
        if self.t <= evnt.delay_req:
            self.R_packets[frm_id] += 1
            self.R_packets2[evnt.pkt_no] += 1
        else:
            self.expired_pkts.append(evnt.pkt_no)

    def __event_ack(self, evnt):
        # receive an ack
        if not evnt.ifretran:
            self.t = evnt.time
            self.rtt = self.t - evnt.snd_time
            self.rttvar = (1-self.beta) * self.rttvar + \
                self.beta * abs(self.srtt-self.rtt)
            self.srtt = (1-self.alpha) * self.srtt + \
                self.alpha * self.rtt
            self.rto = self.srtt + max(1, 4*self.rttvar)
        pkt_no = evnt.pkt_no
        self.ACKed_pkts.put_nowait(pkt_no)

        # update snd window
        while True:
            try:
                pkt_no = self.ACKed_pkts.get_nowait()
            except queue.Empty:
                break

            # uodate S_base if pkt_no == S_base
            if pkt_no == self.S_base:
                self.S_base += 1
            # else put back the pkt_no if pkt_no > S_base
            elif pkt_no > self.S_base:
                self.ACKed_pkts.put_nowait(pkt_no)
                break

        # Send packets
        self.__snd_pkts()

    def sim_run(self):
        while True:
            # logger.debug(str(event_list.queue))
            # Get imminent event
            try:
                evnt = self.event_list.get_nowait()
            except queue.Empty:
                logging.debug("No events any more")
                break
            else:
                if evnt.type == 0:
                    self. __event_pktarrival(evnt)

                elif evnt.type == 1:
                    self.__event_lost(evnt)

                elif evnt.type == 2:
                    self.__event_delivered(evnt)
                else:
                    self.__event_ack(evnt)


if __name__ == "__main__":
    Arq_Simulator = Errctl_Sim()
    Arq_Simulator.sim_run()

    R_packets = Arq_Simulator.R_packets
    R_packets2 = Arq_Simulator.R_packets2
    expired_pkts = Arq_Simulator.expired_pkts
    pktdelay = Arq_Simulator.pktdelay
