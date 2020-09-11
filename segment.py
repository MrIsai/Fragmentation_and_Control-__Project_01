from header import Header

class Segment:
    def __init__(self):
        super().__init__()
        pass

    def build_syn(self, source_port = 0x0, destination_port = 0x0, seq_number=0x1):
        header = Header()

        header.source_port = source_port
        header.destination_port = destination_port
        header.sequence_number = seq_number
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

    def is_ack_syn(self):
        pass
    pass