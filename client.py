import socket
import sys

class Client:
    buffer_size = 1024
    host = None
    port = None
    s = None
    def __init__(self):
        super().__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pass

    def connect(self, host, port):
        self.host = host
        self.port = port
        while(True):
            msg = input('Enter a text: ')
            self.s.sendto(str.encode(msg), (self.host, self.port))

            if msg.lower() == 'exit': sys.exit()
            data, addr = self.s.recvfrom(self.buffer_size)
            print('[SERVER]: %s'%str(data.decode('utf-8')))
            pass
        pass
    pass

client = Client()
client.connect('127.0.0.8', 4444)