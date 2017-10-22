from machine import Pin
from time import sleep
from utime import time

class Anemometer(object):
    """ Maplin anemometer class'
        A wind speed of 1.492 MPH (2.4
        km/h) causes the switch to close 
        once per second."""

    # Constants
    PIN_INPUT = 'GP9'
   
    clicks = 0

    def process_click(self, pin):
        if pin.value() == 1: 
            self.clicks += 1

    def sample(self, seconds):
        start = time()
        finish = start + seconds
        start_clicks = self.clicks
       
        while time() != finish:
            pass

        end_clicks = self.clicks
        total_clicks = end_clicks - start_clicks

        mph_speed = ( (total_clicks / seconds) * 1.492 )
        print( "The wind is {} miles per hour".format( mph_speed ) )
        return mph_speed 


    def print_clicks(self):
        print(self.clicks)

    def __init__(self):
        print("Hello from the anemometer!")
        print("Our time is currently:", time())
     
        in_pin = Pin('G9', Pin.IN, Pin.PULL_UP)
        print("Pin value is currently:", in_pin.value())

        in_pin.callback(Pin.IRQ_RISING, handler=self.process_click)




