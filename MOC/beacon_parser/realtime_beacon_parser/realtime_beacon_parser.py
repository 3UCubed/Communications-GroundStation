import subprocess
import os
from struct import unpack_from

def execute(cmd):
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, universal_newlines=True)
    try:
        for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line
    except KeyboardInterrupt:
        print("Keyboard interrupt...")
        popen.terminate()
        popen.wait()
        popen.stdout.close()
        popen.wait()




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

class BeaconMsg:
    def __init__(self):
        self.header = BeaconMsgHeader()
        self.data = []
        self.partial = False

    def parse(self, data: bytes):
            
        for byte in data:
            self.data.append(byte)
        
        if self.header.dc_id == 0x00000011:
            print(self.data)

    
    def __str__(self):
        str_repr = f"\n\tBeaconMsgHeader> DC ID: {self.header.dc_id} | Flag D: {hex(self.header.flag_d)} | Flag E: {hex(self.header.flag_e)} | MSG Length: {hex(self.header.msg_length)}\n"
        str_repr += f"\t\tBeaconMsgData> {' '.join(f'{byte:02x}' for byte in self.data)}"
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
        return f"\n\nBeaconHeader> Beacon Consecutive Number: {hex(self.beacon_consecutive_number)} | UHF Address: {hex(self.uhf_address)} | Flag A: {hex(self.flag_a)} | OBC Address: {hex(self.obc_address)} | Data ID: {hex(self.data_id)} | Flag B: {hex(self.flag_b)} | Flag C: {hex(self.flag_c)}"




class Beacon:
    BEACON_SIZE = 77
    def __init__(self, data: bytes):
        self.beacon_header = BeaconHeader()
        self.msg_list = []
        self.data = data
        self.current_pos = 0

    def parse(self):
        header_data = self.data[:BeaconHeader.HEADER_SIZE]
        self.beacon_header.parse(header_data)
        self.current_pos = BeaconHeader.HEADER_SIZE

        while self.current_pos < Beacon.BEACON_SIZE - BeaconMsgHeader.MSG_HEADER_SIZE:
            msg = BeaconMsg()
            msg_header_data = self.data[self.current_pos:self.current_pos + BeaconMsgHeader.MSG_HEADER_SIZE]
            msg.header.parse(msg_header_data)
            self.current_pos += BeaconMsgHeader.MSG_HEADER_SIZE
            if self.current_pos + msg.header.msg_length > Beacon.BEACON_SIZE:
                msg_data = self.data[self.current_pos:Beacon.BEACON_SIZE]
                msg.parse(msg_data)
                msg.partial = True
            else:
                msg_data = self.data[self.current_pos:self.current_pos + msg.header.msg_length]
                msg.parse(msg_data)

            self.current_pos += msg.header.msg_length
            
            self.msg_list.append(msg)
            


    



if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    spacecomms_interface_path = os.path.join(root, "spacecomms_interface", "spacecomms_interface.py")
    beacon_listen_start_cmd = 3
    
    cmplt_msg_list = []
    partial_msg = None
    complete_msg = None

    for output_line in execute(["python3", str(spacecomms_interface_path), str(beacon_listen_start_cmd)]):
        byte_data = bytes.fromhex(output_line)

        # Create and parse new beacon
        new_beacon = Beacon(byte_data)
        new_beacon.parse()
        
        # Check if the previous message was partial
        if partial_msg is not None:
            # If so, set complete message to partial message and add the data of the new message
            complete_msg = partial_msg
            complete_msg.data += new_beacon.msg_list[0].data

            # Add the newly completed message to the message list
            cmplt_msg_list.append(complete_msg)
            print(cmplt_msg_list[-1])
            # Add all other complete messages to the message list
            for i in range(1, len(new_beacon.msg_list)):
                if new_beacon.msg_list[i].partial == False:
                    cmplt_msg_list.append(new_beacon.msg_list[i])
                    print(cmplt_msg_list[-1])

        # If previous message wasn't partial...
        else:
            # Add all complete messages to the list
            for i in range(0, len(new_beacon.msg_list)):
                if new_beacon.msg_list[i].partial == False:
                    cmplt_msg_list.append(new_beacon.msg_list[i])
                    print(cmplt_msg_list[-1])

        # If the final message in the beacon message list is partial...
        if new_beacon.msg_list[-1].partial == True:
            # Set partial_msg to the final message in the beacon message list
            partial_msg = new_beacon.msg_list[-1]

        # Otherwise, set partial_message to none
        else:
            partial_msg = None

        