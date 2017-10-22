from network import WLAN
import socket
import ssl
from time import sleep

class ThingSpeak(object):
    # Edit these to suit your particular situation
    api_key = None
    ssid = None
    auth = None 

    host = 'api.thingspeak.com'

    wlan = WLAN(mode=WLAN.STA)

    sock = None
    ssock = None
    addr = None

    def connect_wlan(self):
        if not self.wlan.isconnected():
            self.wlan.connect(ssid=self.ssid, auth=self.auth)
            # Give it a chance to get connected
            while not self.wlan.isconnected():
                pass
            print("Connected: \n", self.wlan.ifconfig())

    def open_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssock = ssl.wrap_socket(self.sock)
        self.ssock.connect(self.addr)

    def close_socket(self):
        for s in [ self.sock, self.ssock ]:
            if s:
                s.close()

    def __init__(self, config):
        self.api_key = config['API_KEY']
        self.ssid = config['WLAN_SSID']
        self.auth = (WLAN.WPA2, config['WLAN_KEY'])
        self.connect_wlan()
        self.addr = socket.getaddrinfo(self.host, 443)[0][-1]
        
    def update(self, field_name, field_value):
        self.connect_wlan()
        self.open_socket()

        path = '/update?api_key=' + self.api_key + '&' + field_name + '=' + str(field_value)

        try: 
            msg = 'GET /' + path + ' HTTP/1.0\r\n\r\n'

            self.ssock.send(bytes(msg, 'utf8'))
            print("Sent message")
            self.close_socket()  
        except Exception as e:
            print("Hit an error")
            print(e)
            self.close_socket()
            raise

