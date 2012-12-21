# -*- coding: utf-8 -*-
from myhdl import *

class Bus(object):
    def __init__(self):
        self.clk2 = Signal(bool())
        self.A   = Signal(intbv(0)[16:])
        self.B   = Signal(intbv(0)[16:])

def submodule(clk, A, B):
    @always(clk.posedge)
    def logic():
        A.next = B + 1
    return logic

def topmod(clk):
    
    bus = Bus()

    @always(clk.posedge)
    def clkcon():
        print(bus.clk2)
        bus.clk2.next = clk

    sub = submodule(bus.clk2, bus.A, bus.B)

    return clkcon, sub

toVerilog(topmod, 
          Signal(bool()))

          


