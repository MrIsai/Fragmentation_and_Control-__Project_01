# TCP Implementation
import socket
import header
import sys

class Server:
    host = None
    port = None
    s = None
    def __init__(self):
        super().__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pass

    def listen(self, host, port):
        self.host = host
        self.port = port
        self.s.bind((self.host, self.port))
        print('[SERVER]: Listening in port %s'%str(self.port))

        while(True):
            #I'm listening and wait a segment with header and data
            segment, addr = self.s.recvfrom(1024)
            #self.s.sendto(str.encode(msg), addr)
            pass
        pass

    def close(self):
        self.s.close()
        pass
    pass