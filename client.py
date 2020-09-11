import socket
import sys
from segment import Segment
import time


class ClientTCP:
    HOST = None
    PORT = None
    PATH = None
    RTT = 5
    SOCKET = None
    BFFR_SIZE = 1280

    SEQ_NUMBER = 1
    ACK_NUMBER = 0

    def __init__(self):
        super().__init__()
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.SOCKET.settimeout(self.RTT)
        pass

    def start(self, path, host, port):
        if len(path) == 0: self.PATH = '/img/500B.jpg'
        else: self.PATH = path
        if len(host) == 0: self.HOST = 'localhost'
        else: self.HOST = host
        if len(port) == 0: self.PORT = int('IP'.encode('utf-8').hex(), 16)
        else: self.PORT = int(self.PORT.encode('utf-8').hex(), 16)

        print(self.PORT)
        self.connect()
        pass

    def connect(self):
        # This function does the 3-way handshake and establish the connection
        while True:
            try:
                # Build and send the first packet (SYN)
                sgm = Segment().build_syn(destination_port=self.PORT, seq_number=self.SEQ_NUMBER)
                self.s.sendto(sgm.encode('utf-8'), (self.HOST, self.PORT))

                # Wait the ACK
                data, address = self.s.recvfrom(self.BFFR_SIZE)

                break
            except socket.timeout:
                print('Timeout')
                pass
        pass
    pass
