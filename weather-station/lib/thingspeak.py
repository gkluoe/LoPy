import socket
import ssl
from time import sleep
from wifi import WiFi

class ThingSpeak(object):
    # Edit these to suit your particular situation
    api_key = None
    host = 'api.thingspeak.com'

    sock = None
    ssock = None
    addr = None

    config = None 

    wifi = None

    def open_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssock = ssl.wrap_socket(self.sock)
        self.ssock.connect(self.addr)

    def close_socket(self):
        for s in [ self.sock, self.ssock ]:
            if s:
                s.close()

    def __init__(self, config):
        self.config = config
        self.wifi = WiFi(self.config)
        self.wifi.connect_wifi()
        self.api_key = config['API_KEY']
        self.addr = socket.getaddrinfo(self.host, 443)[0][-1]
        
        
    def update(self, data):
        self.wifi.connect_wifi()
        self.open_socket()

        values = ''

        for k in data.keys():
           values = values+"&{}={}".format(k, data[k])
           
        path = '/update?api_key=' + self.api_key + values

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

