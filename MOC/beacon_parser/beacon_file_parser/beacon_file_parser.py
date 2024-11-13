#  ---------------------------------------------------------------------------------------------------------------------- 
# Author: Jared Morrison                                                                                                  
# Description: Parses beacons from a .bin file.                                                                           
# Date: November 5th, 2024                                                                                                
#                                                                                                                         
# Beacon Structure:                                                                                                       
# | BeaconHeader | BeaconMsgHeader | Beacon Data | BeaconMsgHeader | Beacon Data | ... 77 bytes                           
#                                                                                                                         
# Note:                                                                                                                   
# Each beacon only has a single BeaconHeader. Each message within that beacon has its own BeaconMsgHeader and data. Each  
# flag attribute (flag_a, flag_b, etc.) are currently unknown bytes in both the Beacon Header and Beacon Message Header.  
# ----------------------------------------------------------------------------------------------------------------------- 


import os
from struct import unpack_from


# ----------------------------------------------------------------------------------------------------------------------- #
# Parses message headers. Instances are created by class BeaconMsg.
class BeaconMsgHeader:
    MSG_HEADER_SIZE = 4

    # Used for translating the dc_id hex value to the actual DC attribute name
    dc_entries_dict = {
        0x00000010: "OBC_0",
        0x00000011: "ADCS_0",
        0x00000012: "ADCS_1",
        0x00000013: "ADCS_2",
        0x00000014: "EPS_0",
        0x00000015: "SSP_0",
        0x00000016: "SSP_1",
        0x00000017: "SSP_2",
        0x00000019: "AOCS_CNTRL_TLM",
        0x0000001A: "EPS_1",
        0x0000001B: "EPS_2",
        0x0000001C: "EPS_3",
        0x0000001D: "EPS_4",
        0x0000001E: "EPS_5",
        0x0000001F: "EPS_6",
        0x00000020: "TaskStats",
        0x00000021: "SSP_3",
        0x00000022: "SENSOR_MAG_PRIMARY",
        0x00000023: "SENSOR_MAG_SECONDARY",
        0x00000024: "SENSOR_GYRO",
        0x00000025: "SENSOR_COARSE_SUN",
        0x00000026: "ES_ADCS_SENSOR_MAG_PRIMARY",
        0x00000027: "ES_ADCS_SENSOR_MAG_SECONDARY",
        0x00000028: "ES_ADCS_SENSOR_GYRO",
        0x00000029: "ES_ADCS_SENSOR_CSS",
        0x00000030: "ES_ADCS_ESTIMATES_BDOT",
        0x00000031: "ES_ADCS_CONTROL_VALUES_MTQ",
        0x00000032: "ConOpsFlags",
        0x00000033: "AOCS_CNTRL_SYS_STATE",
        0x00000034: "ADCS_3",
        0x00000035: "ADCS_4",
        0x000000FF: "Unknown"
    }
    
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
            self.dc_id = BeaconMsgHeader.dc_entries_dict[self.dc_id]
            return BeaconMsgHeader.MSG_HEADER_SIZE
        else:
            return 0


# ----------------------------------------------------------------------------------------------------------------------- #
# Creates instance of BeaconMsgHeader, which provides the length of
# the BeaconMsg data and dc_id. Parses individual beacon messages, 
# stores the parsed data, and keeps track of whether a message is partial.
class BeaconMsg:
    def __init__(self):
        self.header = BeaconMsgHeader()
        self.data = []
        self.partial = False

    def parse(self, data: bytes):
        for byte in data:
            self.data.append(byte)
    
    def __str__(self):
        str_repr = f"\n\tBeaconMsgHeader> DC ID: {self.header.dc_id} | Flag D: {hex(self.header.flag_d)} | Flag E: {hex(self.header.flag_e)} | MSG Length: {hex(self.header.msg_length)}\n"
        str_repr += f"\t\tBeaconMsgData> {self.data}"
        return str_repr


# ----------------------------------------------------------------------------------------------------------------------- #
# Parses Beacon Headers.
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
        return f"\n\nBeaconHeader> Beacon Consecutive Number: {hex(self.beacon_consecutive_number)} | UHF Address: {hex(self.uhf_address)} | Flag A: {hex(self.flag_a)} | OBC Address: {hex(self.obc_address)} | Data ID: {hex(self.data_id)} | Flag B: {hex(self.flag_b)} | Flag C: {hex(self.flag_c)}"


# ----------------------------------------------------------------------------------------------------------------------- #
# Parses all beacons within a .bin file. Creates a new instance of
# BeaconHeader for each new beacon, and creates new instances of 
# BeaconMsg for each message within a beacon. Beacon messages are 
# stored in msg_list, and partial messages can be concatenated by 
# calling handle_partial_msg.
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

            # Update current file position
            current_file_pos = file.tell()
            
            # Get all messages from current beacon
            while current_file_pos < BeaconFile.BEACON_SIZE * current_beacon_number:
                # Create new message object for each message in the current beacon
                beacon_msg = BeaconMsg()

                # Parse the header for the message
                beacon_msg.header.parse(file.read(BeaconMsgHeader.MSG_HEADER_SIZE))
                
                # Update current file position
                current_file_pos = file.tell()

                if beacon_msg.header.dc_id == 'Unknown':
                    file.seek(BeaconFile.BEACON_SIZE * current_beacon_number)
                    current_file_pos = file.tell()
                    continue

                # If the message is split, just read until the end of the current beacon
                if (beacon_msg.header.msg_length + current_file_pos > (BeaconFile.BEACON_SIZE * current_beacon_number)):
                    beacon_msg.parse(file.read((BeaconFile.BEACON_SIZE * current_beacon_number) - current_file_pos))
                    beacon_msg.partial = True
                
                # Otherwise, read the full length of the beacon message
                else:
                    beacon_msg.parse(file.read(beacon_msg.header.msg_length))

                # Add the parsed message to the message list
                self.msg_list.append(beacon_msg)

                # Update current file position
                current_file_pos = file.tell()

            # Update current beacon number
            current_beacon_number += 1

    def handle_partial_msg(self):
        fixed_msg_list = []
        msg_index = 0
        msg_list_len = len(self.msg_list)
        while msg_index < msg_list_len:
            curr_msg = self.msg_list[msg_index]
            if curr_msg.partial:
                if msg_index + 1 < msg_list_len:
                    next_msg = self.msg_list[msg_index + 1]
                    curr_msg.data += next_msg.data
                    msg_index += 1
            fixed_msg_list.append(curr_msg)
            msg_index += 1
        self.msg_list = fixed_msg_list



# ----------------------------------------------------------------------------------------------------------------------- #
# Main function
if __name__ == "__main__":
    root = os.path.dirname(__file__)
    filepath = os.path.join(root, "raw_beacons.bin")
    beacons = BeaconFile(filepath)
    beacons.parse_file()
    beacons.handle_partial_msg()
    for msg in beacons.msg_list:
        print(msg)

