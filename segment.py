from header import Header

class Segment:
    def __init__(self, src_port=0x0, dst_port=0x0, data=''):
        super().__init__()
        self.src_port = src_port
        self.dst_port = dst_port
        self.header = Header()
        self.data = data
        pass

    def build_segment(self, seq=0x0, ack=0x0):
        self.header.source_port = self.src_port
        self.header.destination_port = self.dst_port
        self.header.sequence_number = seq
        self.header.ack_number = ack
        segmento = ''
        if len(self.data) != 0:
            self.header.window_size = len(self.data)
            segmento = self.header.build_header()
            if len(self.data) == 700: segmento += self.data
            else: segmento += self.data + (700-len(self.data))*"0"

        else: 
            self.header.window_size = 0x0
            segmento = self.header.build_header()
        return bytearray.fromhex(segmento)
    pass