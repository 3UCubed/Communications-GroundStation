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
from itertools import islice


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
        str_repr = f"\nBeaconMsgHeader> DC ID: {self.header.dc_id} | Flag D: {hex(self.header.flag_d)} | Flag E: {hex(self.header.flag_e)} | MSG Length: {hex(self.header.msg_length)}\n"
        str_repr += "BeaconMsgData>\n" + "\n".join(f"{str(key) + ':':<40} {value}" for key, value in self.data.items())
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

    def label_data(self):
        labeled_data = {}

        for i, msg in enumerate(self.msg_list):
            if msg.header.dc_id == "OBC_0":
                labeled_data = BeaconFile.parse_obc_0(msg.data)
            elif msg.header.dc_id == "ADCS_0":
                labeled_data = BeaconFile.parse_adcs_0(msg.data)
            elif msg.header.dc_id == "ADCS_1":
                labeled_data = BeaconFile.parse_adcs_1(msg.data)
            elif msg.header.dc_id == "ADCS_2":
                labeled_data = BeaconFile.parse_adcs_2(msg.data)
            elif msg.header.dc_id == "EPS_0":
                labeled_data = BeaconFile.parse_eps_0(msg.data)
            elif msg.header.dc_id == "SSP_0" or msg.header.dc_id == "SSP_1" or msg.header.dc_id == "SSP_2":
                labeled_data = BeaconFile.parse_ssp(msg.data)
            elif msg.header.dc_id == "AOCS_CNTRL_TLM":
                labeled_data = BeaconFile.parse_aocs_cntrl_tlm(msg.data)
            elif msg.header.dc_id == "EPS_1":
                labeled_data = BeaconFile.parse_eps_1(msg.data)
            elif msg.header.dc_id == "EPS_2":
                labeled_data = BeaconFile.parse_eps_2(msg.data)
            elif msg.header.dc_id == "EPS_3":
                labeled_data = BeaconFile.parse_eps_3(msg.data)
            elif msg.header.dc_id == "EPS_4":
                labeled_data = BeaconFile.parse_eps_4(msg.data)
            elif msg.header.dc_id == "EPS_5":
                labeled_data = BeaconFile.parse_eps_5(msg.data)
            elif msg.header.dc_id == "EPS_6":
                labeled_data = BeaconFile.parse_eps_6(msg.data)
            elif msg.header.dc_id == "TaskStats":
                labeled_data = BeaconFile.parse_taskstats(msg.data)
            else:
                labeled_data = BeaconFile.parse_other(msg.data)

            self.msg_list[i].data = labeled_data

    @staticmethod
    def parse_other(data: bytes):
        labeled_data = {}
        for key, value in enumerate(data):
            labeled_data[key] = value
        return labeled_data

    @staticmethod
    def parse_obc_0(data: bytes):
        labeled_data = {}

        labeled_data['opMode'] = data[0]
        labeled_data['upTime'] = int.from_bytes(data[1:5], byteorder='little')
        labeled_data['totalResetCount'] = int.from_bytes(data[5:7], byteorder='little')
        labeled_data['resetReasonBitField'] = int.from_bytes(data[7:9], byteorder='little')
        labeled_data['payloadModesStatus'] = int.from_bytes(data[9:11], byteorder='little')

        return labeled_data


    @staticmethod
    def parse_adcs_0(data: bytes):
        labeled_data = {}
        shifted_data = []
        data_keys = [
            'magFieldVec_X', 'magFieldVec_Y', 'magFieldVec_Z',
            'coarseSunVec_X', 'coarseSunVec_Y', 'coarseSunVec_Z',
            'fineSunVec_X', 'fineSunVec_Y', 'fineSunVec_Z',
            'nadirVec_X', 'nadirVec_Y', 'nadirVec_Z',
            'angRateVec_X', 'angRateVec_Y', 'angRateVec_Z',
            'wheelSpeedArr_X', 'wheelSpeedArr_Y', 'wheelSpeedArr_Z'
        ]

        for i in range(0, len(data), 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little'))

        for key, value in zip(data_keys, shifted_data):
            labeled_data[key] = value
        
        return labeled_data
    
    @staticmethod
    def parse_adcs_1(data: bytes):
        labeled_data = {}
        shifted_data = []
        data_keys = [
            'estQSet_Q1', 'estQSet_Q2', 'estQSet_Q3',
            'estQSet_X', 'estQSet_Y', 'estQSet_Z'
        ]

        for i in range(0, len(data), 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little'))

        for key, value in zip(data_keys, shifted_data):
            labeled_data[key] = value
        
        return labeled_data
    
    @staticmethod
    def parse_adcs_2(data: bytes):
        labeled_data = {}
        byte_0 = data[0]
        byte_1 = data[1]
        byte_2 = data[2]
        byte_3 = data[3]
        byte_4 = data[4]
        byte_5 = data[5]

        # Bits 0-7
        # 01 00 10 11
        labeled_data['Attitude_Estimation_Mode'] = byte_0 & 0b1111  # 10 11
        labeled_data['Control_Mode'] = (byte_0 >> 4) & 0b1111       # 01 00    
        
        # Bits 8-15
        # 01 00 10 11
        labeled_data['ADCS_Run_Mode'] = byte_1 & 0b1                        # 1
        labeled_data['ASGP4_Mode'] = (byte_1 >> 1) & 0b1                    # 1
        labeled_data['CubeControl_Signal_Enabled'] = (byte_1 >> 2) & 0b1    # 0
        labeled_data['CubeControl_Motor_Enabled'] = (byte_1 >> 3) & 0b1     # 1
        labeled_data['CubeSense1_Enabled'] = (byte_1 >> 4) & 0b11           # 00
        labeled_data['CubeSense2_Enabled'] = (byte_1 >> 6) & 0b11           # 01

        # Bits 16-23
        # 01 00 10 11
        labeled_data['CubeWheel1_Enabled'] = byte_2 & 0b1                   # 1
        labeled_data['CubeWheel2_Enabled'] = (byte_2 >> 1) & 0b1            # 1
        labeled_data['CubeWheel3_Enabled'] = (byte_2 >> 2) & 0b1            # 0
        labeled_data['CubeStar_Enabled'] = (byte_2 >> 3) & 0b1              # 1
        labeled_data['GPS_Receiver_Enabled'] = (byte_2 >> 4) & 0b1          # 0
        labeled_data['GPS_LNA_Power_Enabled'] = (byte_2 >> 5) & 0b1         # 0
        labeled_data['Motor_Driver_Enabled'] = (byte_2 >> 6) & 0b1          # 1
        labeled_data['Sun_is_Above_Local_Horizon'] = (byte_2 >> 7) & 0b1    # 0

        # Bits 24-31
        # 01 00 10 11
        labeled_data['CubeSense1_Communications_Error'] = byte_3 & 0b1                  # 1
        labeled_data['CubeSense2_Communications_Error'] = (byte_3 >> 1) & 0b1           # 1
        labeled_data['CubeControl_Signal_Communications_Error'] = (byte_3 >> 2) & 0b1   # 0
        labeled_data['CubeControl_Motor_Communications_Error'] = (byte_3 >> 3) & 0b1    # 1
        labeled_data['CubeWheel1_Communications_Error'] = (byte_3 >> 4) & 0b1           # 0
        labeled_data['CubeWheel2_Communications_Error'] = (byte_3 >> 5) & 0b1           # 0
        labeled_data['CubeWheel3_Communications_Error'] = (byte_3 >> 6) & 0b1           # 1
        labeled_data['CubeStar_Communications_Error'] = (byte_3 >> 7) & 0b1             # 0

        # Bits 32-39
        # 01 00 10 11
        labeled_data['Magnetometer_Range_Error'] = byte_4 & 0b1                 # 1
        labeled_data['Cam1_SRAM_Overcurrent_Detected'] = (byte_4 >> 1) & 0b1    # 1
        labeled_data['Cam1_3V3_Overcurrent_Detected'] = (byte_4 >> 2) & 0b1     # 0
        labeled_data['Cam1_Sensor_Busy_Error'] = (byte_4 >> 3) & 0b1            # 1
        labeled_data['Cam1_Sensor_Detection_Error'] = (byte_4 >> 4) & 0b1       # 0
        labeled_data['Sun_Sensor_Range_Error'] = (byte_4 >> 5) & 0b1            # 0
        labeled_data['Cam2_SRAM_Overcurrent_Detected'] = (byte_4 >> 6) & 0b1    # 1
        labeled_data['Cam2_3V3_Overcurrent_Detected'] = (byte_4 >> 7) & 0b1     # 0

        # Bits 40-47
        # 01 00 10 11
        labeled_data['Cam2_Sensor_Busy_Error'] = byte_5 & 0b1                   # 1
        labeled_data['Cam2_Sensor_Detection_Error'] = (byte_5 >> 1) & 0b1       # 1
        labeled_data['Nadir_Sensor_Range_Error'] = (byte_5 >> 2) & 0b1          # 0
        labeled_data['Rate_Sensor_Range_Error'] = (byte_5 >> 3) & 0b1           # 1
        labeled_data['Wheel_Speed_Range_Error'] = (byte_5 >> 4) & 0b1           # 0
        labeled_data['Coarse_Sun_Sensor_Error'] = (byte_5 >> 5) & 0b1           # 0
        labeled_data['StarTracker_Match_Error'] = (byte_5 >> 6) & 0b1           # 1
        labeled_data['StarTracker_Overcurrent_Detected'] = (byte_5 >> 7) & 0b1  # 0

        return labeled_data


    @staticmethod
    def parse_eps_0(data: bytes):
        labeled_data = {}

        labeled_data['battEnergy'] = int.from_bytes(data[0:8], byteorder='little')
        labeled_data['battCharge'] = int.from_bytes(data[8:16], byteorder='little')
        labeled_data['battChargeCapacity'] = int.from_bytes(data[16:24], byteorder='little')
        labeled_data['battPercent'] = int.from_bytes(data[24:32], byteorder='little')
        labeled_data['battVoltage'] = int.from_bytes(data[32:36], byteorder='little')
        labeled_data['battCurrent'] = int.from_bytes(data[36:40], byteorder='little')
        labeled_data['battTemperature'] = int.from_bytes(data[40:44], byteorder='little')

        return labeled_data

    @staticmethod
    def parse_ssp(data: bytes):
        # All SSP's can be parsed exactly the same way
        labeled_data = {}
        shifted_data = []
        new_labels = ['sunDataMain', 'sunDataExt', 'tempMCU', 'tempMain', 'tempExt1', 'temptExt2']

        for i in range(0, len(data), 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little'))

        for key, value in zip(new_labels, shifted_data):
            labeled_data[key] = value
        
        return labeled_data
    
    @staticmethod
    def parse_aocs_cntrl_tlm(data: bytes):
        labeled_data = {}

        labeled_data['adcsErrFlags'] = int.from_bytes(data[0:2], byteorder='little')
        labeled_data['estAngRateNorm'] = int.from_bytes(data[2:6], byteorder='little')
        labeled_data['estAngRateVec_X'] = int.from_bytes(data[6:10], byteorder='little')
        labeled_data['estAngRateVec_Y'] = int.from_bytes(data[10:14], byteorder='little')
        labeled_data['estAngRateVec_Z'] = int.from_bytes(data[14:18], byteorder='little')
        labeled_data['estAttAngles_Roll'] = int.from_bytes(data[18:22], byteorder='little')
        labeled_data['estAttAngles_Pitch'] = int.from_bytes(data[22:26], byteorder='little')
        labeled_data['estAttAngles_Yaw'] = int.from_bytes(data[26:30], byteorder='little')
        labeled_data['measWheelSpeed_X'] = int.from_bytes(data[30:32], byteorder='little')
        labeled_data['measWheelSpeed_Y'] = int.from_bytes(data[32:34], byteorder='little')
        labeled_data['measWheelSpeed_Z'] = int.from_bytes(data[34:36], byteorder='little')

        return labeled_data
    
    @staticmethod
    def parse_eps_1(data: bytes):
        labeled_data = {}

        labeled_data['battCapacity'] = int.from_bytes(data[0:4], byteorder='little')
        labeled_data['battVoltage'] = int.from_bytes(data[4:8], byteorder='little')
        labeled_data['battCurrent'] = int.from_bytes(data[8:12], byteorder='little')
        labeled_data['battTemperature'] = int.from_bytes(data[12:16], byteorder='little')

        return labeled_data
    
    @staticmethod
    def parse_eps_2(data: bytes):
        labeled_data = {}
        shifted_data = []
        new_labels = [
            'VOLT_BRDSUP',
            'TEMP_MCU',
            'VIP_INPUT_Voltage',
            'VIP_INPUT_Current',
            'VIP_INPUT_Power',
            'STAT_CH_ON',
            'STAT_CH_OCF',
            'VIP_Voltage_VD0',
            'VIP_Current_VD0',
            'VIP_Voltage_VD4',
            'VIP_Current_VD4',
            'VIP_Voltage_VD6',
            'VIP_Current_VD6',
            'VIP_Voltage_VD7',
            'VIP_Current_VD7',
            'VIP_Voltage_VD8',
            'VIP_Current_VD8',
            'VIP_Voltage_VD9',
            'VIP_Current_VD9',
            'VIP_Voltage_VD10',
            'VIP_Current_VD10',
            'VIP_Voltage_VD11',
            'VIP_Current_VD11'
        ]

        for i in range(0, len(data), 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little'))

        for key, value in zip(new_labels, shifted_data):
            labeled_data[key] = value
        
        return labeled_data
    
    @staticmethod
    def parse_eps_3(data: bytes):
        labeled_data = {}
        shifted_data = []
        new_labels = [
            'VOLT_BRDSUP',
            'TEMP_MCU',
            'VIP_INPUT_Voltage',
            'VIP_INPUT_Current',
            'VIP_INPUT_Power',
            'STAT_BU',
            'VIP_BP_INPUT_Voltage_1',
            'VIP_BP_INPUT_Voltage_2',
            'VIP_BP_INPUT_Current_1',
            'VIP_BP_INPUT_Current_2',
            'VIP_BP_INPUT_Power_1',
            'VIP_BP_INPUT_Power_2',
            'STAT_BP_1',
            'STAT_BP_2',
            'VOLT_CELL1_1',
            'VOLT_CELL1_2',
            'VOLT_CELL2_1',
            'VOLT_CELL2_2',
            'VOLT_CELL3_1',
            'VOLT_CELL3_2',
            'VOLT_CELL4_1',
            'VOLT_CELL4_2',
            'BAT_TEMP1_1',
            'BAT_TEMP1_2',
            'BAT_TEMP2_1',
            'BAT_TEMP2_2',
            'BAT_TEMP3_1',
            'BAT_TEMP3_2',
        ]

        for i in range(0, len(data), 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little'))

        for key, value in zip(new_labels, shifted_data):
            labeled_data[key] = value 
        
        return labeled_data
    
    @staticmethod
    def parse_eps_4(data: bytes):
        labeled_data = {}
        shifted_data = []
        new_labels = [
            'VOLT_BRDSUP',
            'TEMP_MCU',
            'VIP_OUTPUT_Voltage',
            'VIP_OUTPUT_Current',
            'VIP_OUTPUT_Power',
            'VIP_CC_OUTPUT_Voltage_1',
            'VIP_CC_OUTPUT_Voltage_2',
            'VIP_CC_OUTPUT_Voltage_3',
            'VIP_CC_OUTPUT_Voltage_4',
            'VIP_CC_OUTPUT_Current_1',
            'VIP_CC_OUTPUT_Current_2',
            'VIP_CC_OUTPUT_Current_3',
            'VIP_CC_OUTPUT_Current_4',
            'VIP_CC_OUTPUT_Power_1',
            'VIP_CC_OUTPUT_Power_2',
            'VIP_CC_OUTPUT_Power_3',
            'VIP_CC_OUTPUT_Power_4',
            'CCx_VOLT_IN_MPPT_1',
            'CCx_VOLT_IN_MPPT_2',
            'CCx_VOLT_IN_MPPT_3',
            'CCx_VOLT_IN_MPPT_4',
            'CCx_CURR_IN_MPPT_1',
            'CCx_CURR_IN_MPPT_2',
            'CCx_CURR_IN_MPPT_3',
            'CCx_CURR_IN_MPPT_4',
            'CCx_VOLT_OU_MPPT_1',
            'CCx_VOLT_OU_MPPT_2',
            'CCx_VOLT_OU_MPPT_3',
            'CCx_VOLT_OU_MPPT_4',
            'CCx_CURR_OU_MPPT_1',
            'CCx_CURR_OU_MPPT_2',
            'CCx_CURR_OU_MPPT_3',
            'CCx_CURR_OU_MPPT_4'
        ]

        for i in range(0, len(data), 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little'))

        for key, value in zip(new_labels, shifted_data):
            labeled_data[key] = value 
        
        return labeled_data

    @staticmethod
    def parse_eps_5(data: bytes):
        labeled_data = {}

        labeled_data['MODE'] = data[0]
        labeled_data['RESET_CAUSE'] = data[1]
        labeled_data['UPTIME'] = int.from_bytes(data[2:6], byteorder='little')
        labeled_data['ERROR'] = int.from_bytes(data[6:8], byteorder='little')
        labeled_data['RC_CNT_PWRON'] = int.from_bytes(data[8:10], byteorder='little')
        labeled_data['RC_CNT_WDG'] = int.from_bytes(data[10:12], byteorder='little')
        labeled_data['RC_CNT_CMD'] = int.from_bytes(data[12:14], byteorder='little')
        labeled_data['RC_CNT_MCU'] = int.from_bytes(data[14:16], byteorder='little')
        labeled_data['RC_CNT_EMLOPO'] = int.from_bytes(data[16:18], byteorder='little')
        labeled_data['UNIX_TIME'] = int.from_bytes(data[18:22], byteorder='little')
        labeled_data['UNIX_YEAR'] = int.from_bytes(data[22:26], byteorder='little')
        labeled_data['UNIX_MONTH'] = int.from_bytes(data[26:30], byteorder='little')
        labeled_data['UNIX_DAY'] = int.from_bytes(data[30:34], byteorder='little')
        labeled_data['UNIX_HOUR'] = int.from_bytes(data[34:38], byteorder='little')
        labeled_data['UNIX_MINUTE'] = int.from_bytes(data[38:42], byteorder='little')
        labeled_data['UNIX_SECOND'] = int.from_bytes(data[42:46], byteorder='little')

        return labeled_data
    
    @staticmethod
    def parse_eps_6(data: bytes):
        labeled_data = {}
        shifted_data = []
        new_labels = [
            'STAT_CH_ON',
            'STAT_CH_OCF',
            'OCF_CNT_CH00',
            'OCF_CNT_CH04',
            'OCF_CNT_CH06',
            'OCF_CNT_CH07',
            'OCF_CNT_CH08',
            'OCF_CNT_CH09',
            'OCF_CNT_CH10',
            'OCF_CNT_CH11'
        ]

        for i in range(0, len(data), 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little'))

        for key, value in zip(new_labels, shifted_data):
            labeled_data[key] = value 
        
        return labeled_data
    
    @staticmethod
    def parse_taskstats(data: bytes):
        labeled_data = {}
        shifted_data = []
        new_labels = [
            'TASK_MONITOR_TASK',
            'TASK_MONITOR_EXEH_PERSISTOR',
            'TASK_MONITOR_APP_TASK',
            'TASK_MONITOR_SERVICES',
            'TASK_MONITOR_SD_MANAGER',
            'TASK_INSTRUMENTS',
            'TASK_MONITOR_S_X_BAND',
            'TASK_MONITOR_CUBEADCS',
            'TASK_MONITOR_CUBEADCS_FHANDL',
            'TASK_MONITOR_GNSS',
            'TASK_PAYLOAD_SCHEDULER',
            'TASK_TELEMETRY',
            'TASK_TELEMETRY_FILE_SINK',
            'TASK_MONITOR_SP',
            'TASK_MACDRV_DISPATCHER',
            'TASK_MACTL_DISPATCHER',
            'TASK_FWUPD_HANDLER',
            'TASK_ESSA_SP_HANDLER',
            'TASK_NVM',
            'TASK_DATACACHE',
            'TASK_ADCS_TLM',
            'TASK_CONOPS_PERIODIC_EV',
            'TASK_MONITOR_PAYLOAD_CTRL',
            'TASK_BEACONS',
            'TASK_EPS_CTRL',
            'TASK_EPS_I',
            'TASK_EPS_II',
            'TASK_EPS_M',
            'TASK_SYS_CLOCK',
            'TASK_MONITOR_ES_ADCS',
            'TASK_ACTUATOR_CONTROL_SERVICE',
            'TASK_SDS',
            'TASK_AOCS_CNTRL',
            'TASK_SXBAND_SCHED',
            'TASK_CRYPTO_SRV',
            'TASK_MONITOR_TASKS_NUMBER'
        ]

        for i in range(0, len(data), 2):
            shifted_data.append(int.from_bytes(data[i:i+2], byteorder='little'))

        for key, value in zip(islice(new_labels, len(shifted_data)), shifted_data):
            labeled_data[key] = value

        return labeled_data



            

# ----------------------------------------------------------------------------------------------------------------------- #
# Main function
if __name__ == "__main__":
    root = os.path.dirname(__file__)
    filepath = os.path.join(root, "raw_beacons.bin")
    beacons = BeaconFile(filepath)
    beacons.parse_file()
    beacons.handle_partial_msg()
    beacons.label_data()
    for msg in beacons.msg_list:
        print(msg)

