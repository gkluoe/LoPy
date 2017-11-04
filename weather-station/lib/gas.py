from machine import ADC
import time


class GasSensor(object):

    PIN = None

    def __init__(self, pin):
        a = ADC(0)
        self.PIN = a.channel(pin='G3', attn=ADC.ATTN_11DB)
        self.PIN.init()

    def value(self):
        return self.PIN.value()