# -*- coding: utf-8 -*-
from myhdl import *

def monitor(a):
    @always(a)
    def logic1():
        print("a={0:0>4}".format(bin(a)))

    return logic1

def top():
    a = Signal(intbv(0)[4:])

    @instance
    def bench():
        for i in range(16):
            a.next = (a + 1) % 16
            yield delay(1)

    return bench, monitor(a)

Simulation(top()).run(20)

x = intbv(24)
print(x, x.min, x.max, len(x))
print(bin(x))
x = intbv(24,min=1,max=30)
print(x, x.min, x.max, len(x))
print(bin(x))
x = intbv(24)[5:]
print(x, x.min, x.max, len(x))
print(bin(x))
x = intbv(24)[5:0]
print(x, x.min, x.max, len(x))
print(bin(x))
x = intbv(24)[5:1]
print(x, x.min, x.max, len(x))
print(bin(x))
x[:] = 0
print(x, x.min, x.max, len(x))
print(bin(x))


X = intbv(15)[4:]
print(X, X.min, X.max, len(x), bin(X))
X[0] = 0
print(X, X.min, X.max, len(x), bin(X))
X[3] = 0
print(X, X.min, X.max, len(x), bin(X))
X[4:] = intbv(int("f",16))
print(X, X.min, X.max, len(x), bin(X))

S = Signal(0)
v1 = S.val
S.next = S + 1
v2 = S.val
print(v1,v2)
print(v1 is v2)
print(type(S))
print(type(S.val))
