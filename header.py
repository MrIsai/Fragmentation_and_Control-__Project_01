class Header:
    source_port = 0x0  # 16 bits
    destination_port = 0x0  # 16 bits
    sequence_number = 0x0  # 32 bits
    ack_number = 0x0  # 32 bits
    data_offset = 0x0          # 4 bits
    reserved = 0x0             # 3 bits
    # Flags                      # 1 bit/flag
    ack, psh, syn, fin = 0x0, 0x0, 0x0, 0x0
    window_size = 0x0  # 16 bits
    checksum = 0x0  # 16 bits
    urgent_pointer = 0x0  # 16 bits

    def __init__(self):
        super().__init__()
        pass

    def build_header(self, data=None):
        header = ''
        # Build first word
        self.source_port = self.source_port << 16
        word = (0 << 32) + self.source_port + self.destination_port
        header += format(word, '010x')[2:]
        #header += self.source_port + self.destination_port

        # Build second word
        header += format(self.sequence_number, '#010x')[2:]

        # Build third word
        header += format(self.ack_number, '#010x')[2:]

        # Build fourth word
        # Set the fields and then build the complete word
        word = 0 << 32
        self.data_offset = self.data_offset << 27
        self.reserved = self.reserved << 24
        self.ack = self.ack << 20
        self.psh = self.psh << 18
        self.syn = self.syn << 16
        self.fin = self.fin << 15
        word += self.data_offset+self.reserved+self.ack + \
            self.psh+self.syn+self.syn+self.fin+self.window_size
        header += format(word, '#010x')[2:]

        #Build the five word
        self.checksum = self.checksum << 16
        word = (0 << 32) + self.checksum + self.urgent_pointer
        header += format(word, '#010x')[2:]
        return header
    pass
