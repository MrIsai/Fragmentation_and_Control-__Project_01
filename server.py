import socket
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

        while(True):
            data, addr = self.s.recvfrom(1024)
            msg = str(data.decode('utf-8'))
            print("[CLIENT]: %s"%msg)

            msg = msg.upper()
            if msg == 'EXIT': sys.exit()

            print("[SERVER]: %s"%msg)
            self.s.sendto(str.encode(msg), addr)
            pass
        pass
    pass

server = Server()
server.listen('127.0.0.8', 4444)

