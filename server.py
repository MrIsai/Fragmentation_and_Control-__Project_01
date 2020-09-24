# TCP Implementation
import socket
from segment import Segment
import sys
import logging


class ServerTCP:
    host = None
    port = int('IP'.encode('utf-8').hex(), 16)
    SOCKET = None
    conn_established = False

    SEQ_NUMBER = 0x0
    ACK_NUMBER = 0x0
    FILE_LEN = 0x0
    FILE_NAME = ''
    FILE = ''

    timeouts = 0

    def __init__(self):
        super().__init__()
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.basicConfig(format="%(asctime)s [SERVER] - %(levelname)s - %(message)s",filename="server.log" ,filemode='w')
        logging.info('Server initialized, waiting parameters.')
        logging.info
        pass

    def listen(self, host="localhost", port="IP"):
        self.host = host
        self.port = self.port if len(port) == 0 else int(
            port.encode('utf-8').hex(), 16)
        self.SOCKET.bind((self.host, self.port))
        self.SOCKET.listen(1)
        print('[SERVER]: Listening in port %s' % str(self.port))
        logging.info('[SERVER]: Listening in port %s' % str(self.port))
        connection, address = self.SOCKET.accept()
        logging.info('[SERVER] Connection initialized between tcp sockets.')

        while True:
            data = connection.recv(1480)
            words, body = self.get_words(data)
            if len(words) == 0:
                break

            # el destino es el server
            src_port = int("IP".encode('utf-8').hex(), 16)
            dst_port = int(words[0][0:4], base=16)  # el origen es el cliente
            self.SEQ_NUMBER = int(words[1], base=16)
            self.ACK_NUMBER = int(words[2], base=16)
            self.FILE_LEN = int(words[3][4:8], base=16)

            if self.SEQ_NUMBER == 1:
                sgm = Segment(src_port, dst_port)
                header_syn_ack = sgm.build_segment(
                    seq=self.SEQ_NUMBER, ack=0x2)
                logging.info('[Server Recv] SYN | [Server Send] SYN-ACK')
                print('[Server Recv] SYN | [Server Send] SYN-ACK', self.SEQ_NUMBER, self.ACK_NUMBER)
                connection.sendall(header_syn_ack)
                pass
            elif self.SEQ_NUMBER == 2 and self.ACK_NUMBER == 2:
                logging.info('[Server Recv] ACK | CONNECTION STABLISHED')
                print('[Server Recv] ACK | CONNECTION STABLISHED', self.SEQ_NUMBER, self.ACK_NUMBER)
                pass

            elif self.SEQ_NUMBER == 0x32 and len(self.FILE_NAME) == 0:
                logging.info('[Server Recv] PSH-ACK | [Server Send] ACK')
                print('[Server Recv] PSH-ACK | [Server Send] ACK', self.SEQ_NUMBER, self.ACK_NUMBER)

                if self.FILE_LEN != 0:
                    self.FILE_NAME = body[0:self.FILE_LEN]
                    pass
                sgm = Segment(src_port, dst_port)
                segmento_ack = sgm.build_segment(ack=0x33)
                connection.sendall(segmento_ack)
                pass 
            elif self.SEQ_NUMBER >= 0x32:

                if self.FILE_LEN != 0 and len(body) != 0:
                    if self.FILE_LEN == 700:
                        self.FILE += body
                        pass
                    elif self.FILE_LEN < 700:
                        self.FILE += body[0: self.FILE_LEN]
                        pass
                    pass
                logging.info('[Server Recv] PSH-ACK | [Server Send] ACK')
                print('[Server Recv] PSH-ACK | [Server Send] ACK', self.SEQ_NUMBER, self.ACK_NUMBER)
                sgm = Segment(src_port, dst_port)
                segmento_ack = sgm.build_segment(ack=self.SEQ_NUMBER+1)
                connection.sendall(segmento_ack)
                pass
            elif self.SEQ_NUMBER == 0x14:
                logging.info('[Server Recv] FIN | [Server Send] FIN-ACK')
                print('[Server Recv] FIN | [Server Send] FIN-ACK', self.SEQ_NUMBER, self.ACK_NUMBER)
                sgm = Segment(src_port, dst_port)
                segmento = sgm.build_segment(seq=0x14, ack=0x15)
                connection.sendall(segmento)
                pass

        if len(self.FILE_NAME) == 0:
            self.SOCKET.close()
            return
            pass

        print(self.FILE)

        self.FILE_NAME = bytes.fromhex(self.FILE_NAME).decode('utf-8')
        logging.info('[SERVER] File recv: %s'%self.FILE_NAME)
        path = './rcp/'+self.FILE_NAME
        new_file = open(path, mode='wb+')
        new_file.write(bytes.fromhex(self.FILE))
        new_file.close()
        logging.info('[SERVER] The file was created, check it.')
        self.SOCKET.close()

    def get_words(self, data):
        data_decoded = data.hex().upper()
        data_body = ''
        words = []
        if len(data_decoded) < 40 or len(data_decoded) > 740:
            print('CONNECTION FINISHED')
            return [], ''
        else:
            for i in range(5):
                words.append(data_decoded[i*8:(i+1)*8])
            if len(data_decoded) > 40:
                data_body = data_decoded[40:740]
        return words, data_body
    pass
