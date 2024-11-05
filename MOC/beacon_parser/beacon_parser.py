#  ---------------------------------------------------------------------------------------------------------------------- #
# Author: Jared Morrison                                                                                                  #
# Description: Parses beacons received from SpaceComms.                                                                   #
# Date: November 5th, 2024                                                                                                #
#                                                                                                                         #
# Beacon Structure:                                                                                                       #
# | BeaconHeader | BeaconMsgHeader | Beacon Data | BeaconMsgHeader | Beacon Data | ... 77 bytes                           #
#                                                                                                                         #
# Note:                                                                                                                   #
# Each beacon only has a single BeaconHeader. Each message within that beacon has its own BeaconMsgHeader and data.       #
# ----------------------------------------------------------------------------------------------------------------------- #


import os
from struct import unpack_from
from rich import print

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


class BeaconMsg:
    def __init__(self):
        self.header = BeaconMsgHeader()
        self.data = []

    def parse(self, data: bytes):
        for byte in data:
            self.data.append(byte)
    
    def __str__(self):
        str_repr = f"\tBeaconMsgHeader> DC ID: {hex(self.header.dc_id)} | MSG Length: {hex(self.header.msg_length)}\n"
        str_repr += f"\t\tBeaconMsgData> {self.data}"
        return str_repr

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
            # Create a new beacon header object
            beacon_header = BeaconHeader()

            # Get the header of the current beacon
            beacon_header.parse(file.read(BeaconHeader.HEADER_SIZE))
            print(beacon_header)
            # Update current file position
            current_file_pos = file.tell()
            
            # Get all messages from current beacon
            while current_file_pos < (BeaconFile.BEACON_SIZE * current_beacon_number):
                # Create new message object for each message in the current beacon
                beacon_msg = BeaconMsg()

                # Parse the header for the message
                beacon_msg.header.parse(file.read(BeaconMsgHeader.MSG_HEADER_SIZE))
                
                # Update current file position
                current_file_pos = file.tell()

                # If the message is split, just read until the end of the current beacon
                if (beacon_msg.header.msg_length + current_file_pos > (BeaconFile.BEACON_SIZE * current_beacon_number)):
                    beacon_msg.parse(file.read((BeaconFile.BEACON_SIZE * current_beacon_number) - current_file_pos))
                
                # Otherwise, read the full length of the beacon message
                else:
                    beacon_msg.parse(file.read(beacon_msg.header.msg_length))

                # Add the parsed message to the message list
                self.msg_list.append(beacon_msg)
                print(beacon_msg)
                # Update current file position
                current_file_pos = file.tell()

            # Update current beacon number
            current_beacon_number += 1


if __name__ == "__main__":
    root = os.path.dirname(__file__)
    filepath = os.path.join(root, "raw_beacons.bin")
    beacons = BeaconFile(filepath)
    beacons.parse_file()

