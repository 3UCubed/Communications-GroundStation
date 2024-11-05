import os
from struct import unpack_from


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
        return f"BeaconHeader> Beacon Consecutive Number: {self.beacon_consecutive_number} | UHF Address: {self.uhf_address} | OBC Address: {self.obc_address} | Data ID: {self.data_id}"

class BeaconFile:
    def __init__(self, filepath):
        self.filepath = filepath

    def parse_file(self):
        beacon_header = BeaconHeader()
        file = open(self.filepath, "rb")
        beacon_header.parse(file.read(BeaconHeader.HEADER_SIZE))
        print(beacon_header)
        

if __name__ == "__main__":
    root = os.path.dirname(__file__)
    filepath = os.path.join(root, "raw_beacons.bin")
    beacons = BeaconFile(filepath)
    beacons.parse_file()
