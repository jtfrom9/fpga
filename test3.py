# -*- coding: utf-8 -*-
from myhdl import *

def clkgen(clk, period=10):
    @always(delay(period))
    def logic():
        clk.next = not clk
    return logic

def memory(clk, addr, din, dout, en, write):
    data = {}

    @always_comb
    def data_in():
        if en and write:
            # print("{0}: addr={1}, data={2}".format(now(), addr, din))
            data[int(addr)] = int(din)
                
    @always_comb
    def data_out():
        if en and not write:
            dout.next = data[int(addr)]

    return instances()


class mem_bus_if(object):
    def __init__(self, addr_width=4, data_width=8):
        self.addr = Signal(intbv(0)[addr_width:])
        self.din  = Signal(intbv(0)[data_width:])
        self.dout = Signal(intbv(0)[data_width:])
        self.en   = Signal(intbv(0)[1:])
        self.write = Signal(intbv(0)[1:])
    

def top():
    clk = Signal(bool(0))

    cgen = clkgen(clk)

    mbus = mem_bus_if()

    mem  = memory(clk, 
                  addr = mbus.addr, 
                  din  = mbus.dout,
                  dout  = mbus.din,
                  en = mbus.en,
                  write = mbus.write)

    def write(addr):
        yield clk.posedge
        mbus.addr.next  = addr
        mbus.dout.next  = addr
        mbus.en.next    = 1 
        mbus.write.next = 1
        yield clk.posedge
        mbus.en.next    = 0

    def read(addr):
        yield clk.posedge
        mbus.addr.next = addr
        mbus.en.next   = 1
        mbus.write.next  = 0
        yield clk.posedge
        mbus.en.next   = 0
        
    @instance
    def bench():
        print("start..")
        for i in range(10):
            yield delay(10)
            yield write(i)
        for i in range(10):
            yield delay(10)
            yield read(i)
            print("Read: addr={0}, data={1}".format(mbus.addr, mbus.din))

    return cgen, mem, bench

Simulation(top()).run(1000)

def hoge(a,b,c):
    @always_comb
    def logic():
        c.next = a + b
    return logic

def hoge(clk, rst, addr, data, en):
    state = enum('INIT','WRITE',encoding='one_hot')

    s = Signal(state.INIT)

    @always(clk.posedge, rst.negedge)
    def logic():
        if rst:
            en.next = 0
            s.next  = state.INIT
        else:
            if s==state.INIT:
                en.next   = 1
                addr.next = addr + 1
                data.next = addr.val
                s.next    = state.WRITE
            elif s==state.WRITE:
                en.next   = 0
                s.next    = state.INIT

    return instances()

toVerilog(hoge, 
          Signal(bool(0)),
          Signal(bool(0)),
          Signal(intbv(0)[16:]),
          Signal(intbv(0)[16:]),
          Signal(bool(0)))



