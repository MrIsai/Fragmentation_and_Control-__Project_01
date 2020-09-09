import header as h

class Segment:
    def __init__(self):
        super().__init__()
        pass

    def build_syn(self, source_port, destination_port):
        header = h.Header()
        header.source_port = source_port.encode('utf-8').hex()
        header.destination_port = destination_port.encode('utf-8').hex()
        header.sequence_number = 0x1
        header.ack_number = 0x0
        header.data_offset = 0x0
        header.reserved = 0x0
        header.syn = 0x1
        header.checksum = 0x0
        header.urgent_pointer = 0x0
        return header.build_header()

    def build_ack_syn(self):
        pass

    def build_ack(self):
        pass
    pass