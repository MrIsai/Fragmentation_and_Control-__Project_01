import socket
import sys
import segment


class Client:
    host = None
    port = None
    s = None

    def __init__(self):
        super().__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pass

    def start(self, host = "localhost", port = 3333):
        self.host, self.port = host, port
        self.connection()
        pass

    def threew_handshake(self):
        seg = segment.Segment()
        segmento = seg.build_syn(src_port, dst_port)
        print(segmento)
        pass

    def connection(self):
        print("# Enter the ports")
        src_port = input("Source port: ")
        dst_port = input("Destination port: ")
        if len(src_port) == 2 and len(dst_port) == 2:
            self.threew_handshake()
            #s.sendto(segmento, (self.host, self.port))
        else: print('!!! Invalid ports')
        pass
    pass
