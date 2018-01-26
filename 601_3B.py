from lib601.lti import *


def averaging_filter(n):
    gain = Gain(1./n)
    adder = FeedforwardAdd(Gain(1), R(0))
    for g in range(2,n):
        adder = FeedforwardAdd(adder, delay_n(g))
    return Cascade(gain, adder)

def delay_n(n):
    if n==0:
        return Gain(1)
    if n==1:
        return R(0)
    return Cascade(R(0),delay_n(n-1))
