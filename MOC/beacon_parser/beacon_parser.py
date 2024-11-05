import os
from struct import unpack_from

class BeaconMsgHeader:
    MSG_HEADER_SIZE = 4
    
    def __init__(self):
        self.dc_id = 0
        self.flag_d = 0
        self.flag_e = 0
        self.msg_length = 0
    
    def parse(self, data: bytes):
        if len(data) >= BeaconMsgHeader.MSG_HEADER_SIZE:
            (
                self.dc_id,
                self.flag_d,
                self.flag_e,
                self.msg_length
            ) = unpack_from("<BBBB", data)
            return BeaconMsgHeader.MSG_HEADER_SIZE
        else:
            return 0
        
    def __str__(self):
        return f"   BeaconMsgHeader> DC ID: {hex(self.dc_id)} | MSG Length: {hex(self.msg_length)}"


class BeaconMsg:
    def __init__(self):
        self.header = BeaconMsgHeader()
        self.data = []

    def parse(self, data: bytes):
        for byte in data:
            self.data.append(byte)

class BeaconHeader:
    HEADER_SIZE = 7
   
    def __init__(self):
        self.beacon_consecutive_number = 0
        self.uhf_address = 0
        self.flag_a = 0
        self.obc_address = 0
        self.data_id = 0
        self.flag_b = 0
        self.flag_c = 0
    
    def parse(self, data: bytes):
        if len(data) >= BeaconHeader.HEADER_SIZE:
            (
                self.beacon_consecutive_number,
                self.uhf_address,
                self.flag_a,
                self.obc_address,
                self.data_id,
                self.flag_b,
                self.flag_c
            ) = unpack_from("<BBBBBBB", data)
            return BeaconHeader.HEADER_SIZE
        else:
            return 0
    
    def __str__(self):
        return f"\n\nBeaconHeader> Beacon Consecutive Number: {hex(self.beacon_consecutive_number)} | UHF Address: {hex(self.uhf_address)} | OBC Address: {hex(self.obc_address)} | Data ID: {hex(self.data_id)}"

class BeaconFile:
    BEACON_SIZE = 77
    def __init__(self, filepath):
        self.filepath = filepath
        self.msg_list = []

    def parse_file(self):
        current_file_pos = 0
        current_beacon_number = 1
        file_length = os.path.getsize(self.filepath)

        file = open(self.filepath, "rb")

        # While we aren't at the end of the file...
        while current_file_pos < file_length - BeaconFile.BEACON_SIZE:
            beacon_header = BeaconHeader()

            # Get the header of the current beacon
            beacon_header.parse(file.read(BeaconHeader.HEADER_SIZE))
            print(beacon_header)

            # Update current file position
            current_file_pos = file.tell()
            
            # Get all messages from current beacon
            while current_file_pos < (BeaconFile.BEACON_SIZE * current_beacon_number):
                beacon_msg = BeaconMsg()

                # Parse the header for the message
                beacon_msg.header.parse(file.read(BeaconMsgHeader.MSG_HEADER_SIZE))
                print(beacon_msg.header)
                
                current_file_pos = file.tell()
                if (beacon_msg.header.msg_length + current_file_pos > (BeaconFile.BEACON_SIZE * current_beacon_number)):
                    beacon_msg.parse(file.read((BeaconFile.BEACON_SIZE * current_beacon_number) - current_file_pos))
                else:
                    beacon_msg.parse(file.read(beacon_msg.header.msg_length))

                print(f"    {beacon_msg.data}")
                # Add the parsed message to the message list
                self.msg_list.append(beacon_msg)

                # Update current file position
                current_file_pos = file.tell()
            current_beacon_number += 1







    

if __name__ == "__main__":
    root = os.path.dirname(__file__)
    filepath = os.path.join(root, "raw_beacons.bin")
    beacons = BeaconFile(filepath)
    beacons.parse_file()

