import math
import random

"""
MAB control model

public methods:
    input_context(delayReq, packet_imp, seg_buffer, snd_wnd): to determine context, return context_id
    exp3_udate(context_id, action_id, reward): to update the model for an action in a context
    exp3_action(): get action for current packet
"""


class MAB_Control():
    def __init__(self):
        #self.packetno = 1
        # self.contype = 1 #context type
        self.rtt = 120
        # action 0 for retransmission, 1 for FEC, and 2 for drop
        # Initialize selection probability and counters for 9 contexts
        self.c1_count = [1/2, 1/2, 0, 0]
        self.c2_count = [1/2, 1/2, 0, 0]
        self.c3_count = [1/2, 1/2, 0, 0]
        self.c4_count = [1/2, 1/2, 0, 0]
        self.c5_count = [1/3, 1/3, 1/3, 0, 0, 0]
        self.c6_count = [1/3, 1/3, 1/3, 0, 0, 0]
        self.c7_count = [1/3, 1/3, 1/3, 0, 0, 0]
        self.c8_count = [1/3, 1/3, 1/3, 0, 0, 0]
        # c9 for where snd_wnd =1, so no fec, 0 for retransmission, 1 for drop
        self.c9_count = [1/2, 1/2, 0, 0]
        self.action = 0
        self.count = {1: self.c1_count, 2: self.c2_count, 3: self.c3_count,
                      4: self.c4_count, 5: self.c5_count, 6: self.c6_count,
                      7: self.c7_count, 8: self.c8_count, 9: self.c9_count}
        self.type = 1
        self.packetno = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}

    def update_rtt(self, rtt):
        self.rtt = rtt

    def update_mxwnd(self, max_wnd):
        self.max_wnd = max_wnd

    def input_context(self, delayReq, packet_imp, seg_buffer, snd_wnd):
        self.delayReq = delayReq
        self.packet_imp = packet_imp
        self.seg_buffer = seg_buffer
        self.snd_wnd = snd_wnd
        return self.type

    def _detcontype(self):
        # type 1: delay<1.5 rtt, seg_buffer = 0, packet_importance = 0
        # type 2: delay<1.5 rtt, seg_buffer = 0, packet_importance = 1
        # type 3: delay<1.5 rtt, seg_buffer > win, packet_importance = 0
        # type 4: delay<1.5 rtt, seg_buffer > win, packet_importance = 1
        # type 5: delay > 1.5 rtt, seg_buffer = 0, packet_importance = 0
        # type 6: delay > 1.5 rtt, seg_buffer = 0, packet_importance = 1
        # type 7: delay > 1.5 rtt, seg_buffer > 0, packet_importance = 0
        # type 8: delay > 1.5 rtt, seg_buffer > 0, packet_importance = 1
        if self.delayReq <= 1.5*self.rtt:
            if self.packet_imp != 1 and self.seg_buffer <= self.snd_wnd:
                self.type = 1
            if self.packet_imp == 1 and self.seg_buffer <= self.snd_wnd:
                self.type = 2
            if self.packet_imp != 1 and self.seg_buffer > self.snd_wnd:
                self.type = 5
            if self.packet_imp == 1 and self.seg_buffer > self.snd_wnd:
                self.type = 6
        if self.delayReq > 1.5*self.rtt:
            if self.packet_imp != 1 and self.seg_buffer <= self.snd_wnd:
                self.type = 3
            if self.packet_imp == 1 and self.seg_buffer <= self.snd_wnd:
                self.type = 4
            if self.packet_imp != 1 and self.seg_buffer > self.snd_wnd:
                self.type = 7
            if self.snd_wnd <= 1:
                self.type = 9
            if self.packet_imp == 1 and self.seg_buffer > self.snd_wnd:
                self.type = 8

    def exp3_action(self):
        self._detcontype()
        num_action = len(self.count[self.type])/2
        rndnum = random.uniform(0, 1)
        cumsum = 0
        for i in range(int(num_action)):
            cumsum = cumsum + self.count[self.type][i]
            if rndnum <= cumsum:
                self.action = i
                break
        if self.type == 9 and self.action == 1:
            return 2
        return self.action
        # 0 for retransmission, 1 for FEC, and 2 for drop

    def exp3_udate(self, context_id, action_id, reward):
        num_action = len(self.count[context_id])/2
        loss_sum = 0
        eta = math.sqrt(math.log(num_action) /
                        (num_action*self.packetno[context_id]))
        for i in range(int(num_action)):
            if i == action_id:
                self.count[context_id][int(num_action) + i] += (1-reward) / \
                    (self.count[context_id][self.action]+eta/2)
            else:
                self.count[context_id][int(num_action) + i] += 0
            self.count[context_id][i] = math.exp(-eta *
                                                 self.count[context_id][int(num_action)+i])
            loss_sum += self.count[context_id][i]
        for i in range(int(num_action)):
            self.count[context_id][i] = self.count[context_id][i]/loss_sum
        self.packetno[context_id] += 1
