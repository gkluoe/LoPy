from network import WLAN
from time import sleep


class WiFi(object):
    wlan = None
    config = None

    def can_see_ssid(self, ssid):
        networks = [ w[0] for w in self.wlan.scan() ]
        return ssid in networks

    def __init__(self, config):
        self.config = config
        self.wlan = WLAN(mode=WLAN.STA)

    def isconnected():
        return self.wlan.isconnected()
    
    def connect_wifi(self):
        config = self.config
        if not self.wlan.isconnected():
            for wlan in config['WLANS']:
                if self.can_see_ssid(wlan['WLAN_SSID']):
                    print("Trying: {} ...".format(wlan['WLAN_SSID']))
                    self.wlan.connect(ssid=wlan['WLAN_SSID'], 
                                       auth=(WLAN.WPA2, wlan['WLAN_KEY']))

                    # Give it a chance to get connected
                    count = 0
                    while not self.wlan.isconnected() and count < 10:
                        print("Waiting for connection... ({})".format(count))
                        count += 1
                        sleep(1)
                    if not self.wlan.isconnected():
                        print("Giving up")
            if self.wlan.isconnected():
                print("Connected: \n", self.wlan.ifconfig())
