from anemometer import Anemometer
from thingspeak import ThingSpeak
import _thread
import time
import micropython
import gc
import json
micropython.alloc_emergency_exception_buf(100)

# Testing, 1234
SAMPLE_TIME = 2
FIELD = 'field1'

def read_config(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())

def bg_update():
    config = read_config('/flash/lib/config.json')
    an = Anemometer()
    ts = ThingSpeak(config=config)
    while True:
        ts.update(FIELD, an.sample(SAMPLE_TIME))
        gc.collect()
        print(gc.mem_free())
        # Thingspeak only allows us an update
        # every 15 seconds
        time.sleep(15)
        

def run():
    bg = _thread.start_new_thread(bg_update, ())
    #bg_update()
