import socket
import sys
from segment import Segment
import logging

class ClientTCP:
    HOST = None
    PORT = None
    PATH = None
    SOCKET = None

    SEQ_NUMBER = 0x1
    ACK_NUMBER = 0x0
    n_data_transmmited = 0

    last_flag = ''
    conn_stablished = False
    timeouts = 0

    def __init__(self):
        super().__init__()
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pass

    def start(self, path='500B.jpg', host='localhost', port='19509'):
        self.PATH = path
        self.HOST = host
        self.PORT = int(port)

        # Split the data
        with open('./img/'+self.PATH, 'rb') as file:
            content = file.read()
            file_data = content.hex()
            file_data = self.split_data(file_data)
            pass

        try:
            self.SOCKET.connect((self.HOST, self.PORT))
            logging.info('Connection started between tcp sockets')
            print('Connection started between tcp sockets')
            print('%s %s'%(self.HOST,self.PORT))
        except:
            logging.error('Connection refused')
            print('Refused')
        src_port = int('IP'.encode('utf-8').hex(), base=16)
        dst_port = 0x0

        try:
            while True:
                if self.n_data_transmmited == len(file_data):
                    self.SEQ_NUMBER = 0x14
                    pass

                if self.SEQ_NUMBER == 1 and self.ACK_NUMBER == 0:
                    # start 3 way handshake
                    sgm = Segment(src_port=0x0, dst_port=self.PORT)
                    header_syn = sgm.build_segment(seq=0x1)
                    logging.basicConfig(format="%(asctime)s [CLIENT] - %(levelname)s - %(message)s",filename="client.log" ,filemode='w+')
                    logging.info('[Client] Send SYN')
                    print('[Client] Send SYN')
                    self.SOCKET.sendall(header_syn)
                    pass
                elif self.SEQ_NUMBER == 1 and self.ACK_NUMBER == 2:
                    sgm = Segment(src_port=src_port, dst_port=dst_port)
                    header_ack = sgm.build_segment(seq=0x2, ack=0x2)
                    self.SOCKET.sendall(header_ack)

                    # Send file name
                    filename = str.encode(self.PATH).hex()
                    logging.basicConfig(format="%(asctime)s [CLIENT] - %(levelname)s - %(message)s",filename="client.log" ,filemode='w+')
                    logging.info('[Client Recv] SYN-ACK | [Client Send] ACK | [Client Send] PSH-ACK')
                    print('[Client Recv] SYN-ACK | [Client Send] ACK | [Client Send] PSH-ACK')
                    sgm = Segment(src_port, dst_port, data=filename)
                    segmento = sgm.build_segment(seq=0x32)
                    self.SOCKET.sendall(segmento)
                    pass
                elif self.SEQ_NUMBER == 0x14 and self.ACK_NUMBER >= 0x32:
                    logging.basicConfig(format="%(asctime)s [CLIENT] - %(levelname)s - %(message)s",filename="client.log" ,filemode='w+')
                    logging.info('[Client Recv] ACK | [Client Send] FIN')
                    print('[Client Recv] ACK | [Client Send] FIN')
                    sgm = Segment(src_port, dst_port)
                    segmento = sgm.build_segment(seq=self.SEQ_NUMBER)
                    self.SOCKET.sendall(segmento)
                    pass
                elif self.ACK_NUMBER == 0x15 and self.SEQ_NUMBER == 0x14:
                    logging.basicConfig(format="%(asctime)s [CLIENT] - %(levelname)s - %(message)s",filename="client.log" ,filemode='w+')
                    logging.info('[Client Recv] FIN-ACK | [Client Send] ACK | CONNECTION FINISHED')
                    print('[Client Recv] FIN-ACK | [Client Send] ACK | CONNECTION FINISHED')
                    sgm = Segment(src_port, dst_port)
                    segmento = sgm.build_segment(seq=self.ACK_NUMBER)
                    self.SOCKET.sendall(segmento)
                    break
                    pass
                elif self.ACK_NUMBER >= 0x33:
                    logging.info('[Client Recv] ACK | [Client Send] PSH-ACK')
                    sgm = Segment(src_port, dst_port,
                                  data=file_data[self.n_data_transmmited])
                    segmento = sgm.build_segment(
                        seq=self.ACK_NUMBER+len(file_data[self.n_data_transmmited]))
                    self.SOCKET.sendall(segmento)
                    self.n_data_transmmited += 1
                    pass

                data = self.SOCKET.recv(1280)
                words = self.get_words(data)
                if len(words) == 0:
                    break

                src_port = int(words[0][4:8], base=16)
                dst_port = int(words[0][0:4], base=16)
                self.SEQ_NUMBER = int(words[1], base=16)
                self.ACK_NUMBER = int(words[2], base=16)

            pass
        except:
            logging.error('Exception error')
        self.SOCKET.close()
        return

    def get_words(self, data):
        data_decoded = data.hex().upper()
        if len(data_decoded) < 40 or len(data_decoded) > 740:
            return []
        words = []
        for i in range(5):
            words.append(data_decoded[i*8:(i+1)*8])
        return words

    def file_data_to_words(self, data):
        for i in range(len(data)):
            pass
        pass

    def split_data(self, hex_string):
        data = []
        for i in range(int(len(hex_string)/700)+1):
            data.append(hex_string[(i)*700: (i+1)*700])
        return data
    pass
