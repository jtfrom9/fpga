# -*- coding: utf-8 -*-
from myhdl import *

def Hello(clk):
    @always(clk.posedge)
    def logic():
        print("{0} Hello".format(now()))

    return logic

clk = Signal(bool(0))

@instance
def bench():
    for i in range(10):
        yield delay(1)
        clk.next = not clk

Simulation(Hello(clk),bench).run(30)
